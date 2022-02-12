# coding:utf-8
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab,timedelta
# 指定Django默认配置文件模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SQL_memOJi.settings')

# 为我们的项目myproject创建一个Celery实例。这里不指定broker容易出现错误。
app = Celery('SQL_memOJi', broker='redis://127.0.0.1:6379/0')

# 这里指定从django的settings.py里读取celery配置
app.config_from_object('django.conf:settings')

# 自动从所有已注册的django app中加载任务
app.autodiscover_tasks()
app.conf.update(
    CELERYBEAT_SCHEDULE={
        'mark_paper': {
            'task': 'coding.tasks.mark_paper',
            'schedule': timedelta(seconds=20), 
            'args': (),
        }
    }
)
# 用于测试的异步任务
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
# celery -A SQL_memOJi worker -l info
# celery -A SQL_memOJi beat
