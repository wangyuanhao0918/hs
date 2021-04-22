#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# @Time : 2021/4/21 下午4:20 
# @Author : yuanhao-wang
# @Filename : user_loging.py

from utils.params_check import Resp
from utils import Logging as logger


class UserLoging(Resp):
    """
    用户登录
    """

    def list(self, headers, data, files=None, key=None):
        params = (
            ('page', int),
            ('size', int),
        )
        code, error_msg, res_data = self.params_check(data=data, params=params)
        if code != 0:
            return self.data(errcode=code, errmsg=error_msg)

        return self.data(data=data)

    def post(self, headers, data, files=None, key=None):
        params = (
            ('page', int),
            ('size', int),
        )
        code, error_msg, res_data = self.params_check(data=data, params=params)
        if code != 0:
            return self.data(errcode=code, errmsg=error_msg)

        return self.data(data=data)
