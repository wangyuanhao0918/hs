#!/bin/bash

HOST_NAME=`hostname`
if [[ $HOST_NAME =~ "saas-backend"* ]]; then
    CELERY=/workspace/py3-dj2/bin/celery
else
    CELERY=/Users/wangyuanhao/project/xwdc/venv/bin/celery
fi
PROJECT=hs
case "$1" in
  start)
    nohup $CELERY worker -A $PROJECT.celery --pool=solo --loglevel=info --logfile=./logs/celeryworker.log > celery_worker.out 2>&1 &
    if [[ $? -eq 0 ]]; then
        echo $! > celery_worker.pid
    fi
    nohup $CELERY beat -A $PROJECT.celery -l info --logfile=./logs/celerybeat.log > celery_beat.out 2>&1 &
    if [[ $? -eq 0 ]]; then
        echo $! > celery_beat.pid
    fi
    ;;
  stop)
    kill -9 `cat celery_worker.pid`
    kill -9 `cat celery_beat.pid`
    ;;
  restart)
    $0 stop
    $0 start
    ;;
  *)
    echo "USAGE: $0 {start|stop|restart}"
    exit 1
esac
exit 0

