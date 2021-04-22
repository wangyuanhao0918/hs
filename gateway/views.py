# Create your views here.
# -*- encoding=utf-8 -*-

import hashlib
import json
import time
from utils import Requests as requests
import importlib
from urllib.parse import urljoin
from django.http import JsonResponse, HttpResponseServerError, HttpResponseNotFound, HttpResponseBadRequest
from django_redis import get_redis_connection
import logging
from rest_framework.views import APIView
from gateway.tasks import write_log
from .router import routing_table, re_routing_list

logger = logging.getLogger(__name__)
METHOD_MAP = {
    'get': requests.get,
    'post': requests.post,
    'put': requests.put,
    'patch': requests.patch,
    'delete': requests.delete
}

redis_conn = get_redis_connection("default")


class GateWay(APIView):
    # comment this line to open the sign verification
    # authentication_classes = ()
    def __get_subpath(self, path):
        tail_slash = ''
        if path.endswith('/'):
            path = path[:-1]
            tail_slash = '/'
        path, key = path.rsplit('/', maxsplit=1)
        path += '/'
        return path, key, tail_slash

    def __load_class(self, class_path):
        pos = class_path.rfind('.')
        module_path = class_path[:pos]
        class_name = class_path[pos + 1:]
        mod = importlib.import_module(module_path)
        cls = getattr(mod, class_name)
        return cls

    def __dispatch(self, request):
        if request.method.lower() == 'get':
            data = request.GET
        else:
            data = request.data
        path = request.path.replace('/api', '')
        if not path:
            return HttpResponseNotFound()
        key = None
        path_dict = {}
        tail_slash = ''
        api_path = path
        upstream = ''
        if path in routing_table:
            upstream = routing_table[path]
        else:
            subpath, key, tail_slash = self.__get_subpath(path)
            if subpath in routing_table:
                upstream = routing_table[subpath]
                api_path = subpath
            else:
                for re_obj, call_addr in re_routing_list:
                    ret = re_obj.search(path)
                    if ret:
                        upstream = call_addr
                        path_dict = ret.groupdict()
                        break
        if not upstream:
            return HttpResponseNotFound()

        lpc = ''
        url = ''
        if upstream.startswith('LPC::'):
            lpc = upstream.replace('LPC::', '')
        elif routing_table[path].startswith('URL::'):
            url = upstream.replace('URL::', '')
            if key:
                url = urljoin(url, "/{0}{1}".format(key, tail_slash))
        else:
            return HttpResponseServerError()

        headers = {
            'Host': request.META['HTTP_HOST'],
            'User-Agent': request.META['HTTP_USER_AGENT'],
            'X-Real-IP': request.META['REMOTE_ADDR'],
            'Path': api_path,
            'Dev-Platform': request.META.get('HTTP_DEV_PLATFORM', None),
            'Dev-Model': request.META.get('HTTP_DEV_MODEL', None),
            'Dev-Version': request.META.get('HTTP_DEV_VERSION', None),
            'App-Version': request.META.get('HTTP_APP_VERSION', None),
            'App-Client': request.META.get('HTTP_APP_CLIENT', None),
            'App-Id': request.META.get('HTTP_X_AUTH_APPID', None),
            'Path_Dict': path_dict,
            'open_id': request.META.get('HTTP_AUTHORIZATION', None),
            'X-MUMWAY-TRACEID': request.META.get('HTTP_X_MUMWAY_TRACEID', None),
        }

        # 请求记录
        if not headers["X-MUMWAY-TRACEID"]:
            headers["X-MUMWAY-TRACEID"] = hashlib.md5(
                str(headers["Path"] + str(time.time())).encode('utf-8')
            ).hexdigest()
        redis_conn.set("X-MUMWAY-TRACEID", headers["X-MUMWAY-TRACEID"])

        if 'HTTP_X_AUTH_USERTOKEN' in request.META:
            headers['X-AUTH-USERTOKEN'] = request.META['HTTP_X_AUTH_USERTOKEN']
        for k, v in request.FILES.items():
            request.data.pop(k)
        if request.content_type and request.content_type.lower() == 'application/json':
            headers['Content-Type'] = request.content_type

        if lpc:
            need_instance = False
            if lpc.endswith('()'):
                need_instance = True
                lpc = lpc.replace('()', '')
            module = self.__load_class(lpc)
            try:
                logger.info(
                    f'{headers["X-MUMWAY-TRACEID"]} call_method {request.method.lower()} url {request.path} data {data}')
                call_method = request.method.lower()
                if call_method == 'get' and not key:
                    call_method = 'list'
                if need_instance:
                    method = getattr(module(), call_method)
                else:
                    method = getattr(module, call_method)
            except Exception as e:
                logger.error(
                    f'{headers["X-MUMWAY-TRACEID"]} 请求失败：\ncall_method {request.method.lower()}\n url {request.path} \n headers {headers} ;\n data {data} \n error {e} ')
                return HttpResponseBadRequest()
            try:
                res = method(headers=headers, data=data, files=request.FILES, key=key) or {}
            except Exception as e:
                logger.error('{3} {0} \n {1} \n{2}'.format(request.path,
                                                           json.dumps(data, ensure_ascii=False),
                                                           str(e),
                                                           headers["X-MUMWAY-TRACEID"]))
                return JsonResponse(status=200, data={'errcode': 50000, 'data': {}, 'errmsg': f'系统错误：{e}'})
            # 请求日志
            write_log.delay(
                traceid=headers["X-MUMWAY-TRACEID"],
                lower=request.method.lower(),
                path=request.path,
                data=json.dumps(data),
                res=res
            )
            return JsonResponse(data=res, status=200)
        if url:
            return METHOD_MAP[request.method.lower()](url, headers=headers, data=data, files=request.FILES)

    def get(self, request):
        return self.__dispatch(request)

    def post(self, request):
        return self.__dispatch(request)

    def put(self, request):
        return self.__dispatch(request)

    def patch(self, request):
        return self.__dispatch(request)

    def delete(self, request):
        return self.__dispatch(request)
