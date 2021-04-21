import json
import requests
from django_redis import get_redis_connection
import logging

redis_conn = get_redis_connection("default")


class Requests(object):
    """
    封装requests模块
    """
    codes = requests.codes
    Session = requests.Session

    @classmethod
    def handle_req(self, method, url, **kwargs):
        req = getattr(requests, method)
        if not req:
            return json.dumps({"errcode": 10000, "errmsg": "不支持的请求"})
        headers_dict = kwargs.get("headers", dict())
        if not headers_dict.get("X-MUMWAY-TRACEID"):
            headers_dict["X-MUMWAY-TRACEID"] = redis_conn.get("X-MUMWAY-TRACEID")

        kwargs["headers"] = headers_dict
        return req(url, **kwargs)

    @classmethod
    def get(self, url, params=None, **kwargs):
        return self.handle_req("get", url, params=params, **kwargs)

    @classmethod
    def post(self, url, data=None, json=None, **kwargs):
        return self.handle_req("post", url, data=data, json=json, **kwargs)

    @classmethod
    def put(self, url, data=None, **kwargs):
        return self.handle_req("put", url, data=data, **kwargs)

    @classmethod
    def delete(self, url, **kwargs):
        return self.handle_req("delete", url, **kwargs)

    @classmethod
    def options(self, url, **kwargs):
        return self.handle_req("options", url, **kwargs)

    @classmethod
    def patch(self, url, data=None, **kwargs):
        return self.handle_req("patch", url, data=data, **kwargs)


class Logging(object):
    """
    封装 Logging
    """

    @classmethod
    def __logging_info(
            cls, method, log_name,
            class_name, log_info,
            traceid, params):
        """
        返回值格式
        """
        if log_name:
            log_name = f"{log_name}:"
        if traceid:
            traceid = f"请求唯一编号:{traceid} "
        return f"{traceid}{log_name}{class_name} PARAMS:{params} {method.upper()}:{log_info}"

    @classmethod
    def __logging_init(
            cls, method, log_name,
            class_name, log_info, params,
            **kwargs):
        """
        封装
        """
        logger = getattr(logging.getLogger(__name__), method)
        traceid = kwargs.get('X-MUMWAY-TRACEID', '')
        if not logger:
            raise ValueError(f'日志错误 logger.{method} 参数异常')

        info = cls.__logging_info(
            method=method, log_name=log_name,
            class_name=class_name, log_info=log_info,
            traceid=traceid, params=params)

        return logger(info)

    @classmethod
    def error(cls, log_info, log_name="",
              class_name="", params=None,
              **kwargs):
        """
        error
        :param log_name: 日志名称
        :param class_name: 模块名称
        :param log_info: 日志内容
        :param params: 请求参数
        :param kwargs: headers
        :return:
        """
        return cls.__logging_init(
            method="error", log_name=log_name,
            class_name=class_name, log_info=log_info,
            params=params, **kwargs)

    @classmethod
    def info(cls, log_info, log_name="",
             class_name="", params=None,
             **kwargs):
        """
        info
        :param log_name: 日志名称
        :param class_name: 模块名称
        :param log_info: 日志内容
        :param params: 请求参数
        :param kwargs: headers
        :return:
        """
        return cls.__logging_init(
            method="info", log_name=log_name,
            class_name=class_name, log_info=log_info,
            params=params, **kwargs)

    @classmethod
    def warning(cls, log_info, log_name="",
                class_name="", params=None,
                **kwargs):
        """
        warning
        :param log_name: 日志名称
        :param class_name: 模块名称
        :param log_info: 日志内容
        :param params: 请求参数
        :param kwargs: headers
        :return:
        """
        return cls.__logging_init(
            method="warning", log_name=log_name,
            class_name=class_name, log_info=log_info,
            params=params, **kwargs)

    @classmethod
    def debug(cls, log_info, log_name="",
              class_name="", params=None,
              **kwargs):
        """
        warning
        :param log_name: 日志名称
        :param class_name: 模块名称
        :param log_info: 日志内容
        :param params: 请求参数
        :param kwargs: headers
        :return:
        """
        return cls.__logging_init(
            method="debug", log_name=log_name,
            class_name=class_name, log_info=log_info,
            params=params, **kwargs)
