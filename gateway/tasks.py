#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# @Time : 2021/3/31 下午5:57 
# @Author : yuanhao-wang
# @Filename : tasks.py
from hs.celery import app
import datetime

@app.task
def write_log(traceid, lower, path, data, res):
    """
    写入日志
    """
    log_dir = './logs/hs/'
    now_dt = datetime.datetime.now()
    log_filename = f'hs_req{now_dt.strftime("%Y-%m-%d")}.log'
    with open(log_dir + log_filename, "a") as e:
        log_info = "Request：{0} {1} >>: {2} {3} \n  Params: {4} \n  Response：{5} \n".format(
            traceid,
            now_dt.strftime("%Y-%m-%d %H:%M:%S"),
            lower,
            path,
            data,
            res
        )
        e.write(log_info)
