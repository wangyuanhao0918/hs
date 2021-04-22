#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# @Time : 2021/3/23 上午11:02 
# @Author : yuanhao-wang
# @Filename : params_check.py

import datetime


class Resp(object):
    """
    返回封装
    """
    err_code_dict = {
        # 其他
        11199: "其他错误",

        # 参数
        11101: "参数不完整",
        11102: "参数错误",

        # 数据库
        11111: "数据不存在或已被删除",
        11112: "未知的数据库错误",

        # 文案
        11121: "",
    }

    @classmethod
    def data(cls, errcode=0, errmsg="ok", data={}):
        ret = {
            "errcode": errcode,
            "errmsg": errmsg,
            "data": data
        }

        if ret["errcode"] == 0:
            return ret

        if errcode not in cls.err_code_dict:
            ret["errcode"] = 11199
        ret["errmsg"] = "{0}({1})".format(cls.err_code_dict[ret["errcode"]], errmsg)

        return ret

    @classmethod
    def backend_error(cls, error_name='', class_name='', error_info=None):
        """
        业务层错误日志格式
        :param error_name: 错误名称
        :param class_name: 类名称
        :param error_info: 错误信息
        :param params_info 参数
        :return: 错误名称:类名称 ERROR 错误信息
        """
        return f"{error_name}-{class_name} 错误信息:{error_info}"

    @classmethod
    def logger_info(cls, info_name, class_name, info):
        """
        日志格式
        :param info_name: 名称
        :param class_name: 类名称
        :param info: 信息
        :return: 名称:类名称 ERROR 信息
        """
        return f"{info_name}:{class_name} INFO:{info}"

    @classmethod
    def params_check(cls, data, params):
        """
        字段校验方法
        :param params: (参数名,参数类型,是否必填,解密)
        :return: code, error_msg, res_data
        """
        error_msg = []
        code = 0
        res_data = {}

        for p in params:
            p_name = p[0]
            p_type = p[1]
            try:
                must_have = p[2]
            except:
                must_have = True

            res = data.get(p_name, None)
            if res is None and must_have:
                error_msg.append('{0} 字段不可为空!'.format(p_name))
                continue
            elif not must_have:
                if res:
                    pass
                else:
                    res_data[p_name] = None
                    continue

            if p_type is int:
                if res == '':
                    pass
                else:
                    try:
                        res = int(res)
                    except:
                        error_msg.append('{0} 字段类型为 int!'.format(p_name))
                        continue
            elif p_type is str:
                if not isinstance(res, str):
                    res = str(res)
            elif p_type is list:
                if not isinstance(res, list):
                    error_msg.append('{0} 字段类型为 list!'.format(p_name))
                    continue
            elif p_type is dict:
                if not isinstance(res, dict):
                    error_msg.append('{0} 字段类型为 dict!'.format(p_name))
                    continue
            elif p_type == 'datetime':
                res = str(res)
                try:
                    datetime.datetime.strptime(res, "%Y-%m-%d %H:%M:%S")
                except:
                    error_msg.append('{0} 字段类型为时间类型 %Y-%m-%d %H:%M:%S !'.format(p_name))
                    continue
            else:
                pass
            res_data[p_name] = res

        if error_msg:
            code = 11102
            error_msg = "|".join(error_msg)

        return code, error_msg, res_data
