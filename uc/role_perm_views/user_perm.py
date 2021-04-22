#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# @Time : 2021/4/21 下午4:54 
# @Author : yuanhao-wang
# @Filename : user_perm.py
from utils.params_check import Resp


class UserPerm(Resp):
    """
    用户权限
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
