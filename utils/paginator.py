#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# @Time : 2021/3/23 下午1:21 
# @Author : yuanhao-wang
# @Filename : paginator.py
from django.core.paginator import Paginator


class PaginatorProcess(object):
    """
    分页处理
    """

    @classmethod
    def paginator(cls, page, size, data_obj):

        if page <= 0:
            page = 1
        if size <= 0:
            size = 10

        paginator = Paginator(data_obj, size)
        all_count = paginator.count
        all_page = paginator.num_pages

        res = {
            "all_count": all_count,
            "all_page": all_page,
            "page": page,
            "size": size,
            "data": [],
        }

        if page > all_page:
            pass
        else:
            res['data'] = paginator.page(page)

        return res
