# -*- encoding=utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
import sys
import socket
from celery import Celery

start_config = 'xwdc.settings'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', start_config)
if sys.platform == 'win32':
    # windows 配置 不然报错
    os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

app = Celery('xwdc')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
