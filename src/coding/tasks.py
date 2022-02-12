# coding/tasks.py
import os, time
from django.template.loader import render_to_string
from django.conf import settings
from celery import shared_task
from utils import sql_check
@shared_task
def sql_check_celery(db_nm, ans_sql, stud_sql):
    print(db_nm,ans_sql,stud_sql)
    correct = sql_check.ans_check(db_nm=db_nm, ans_sql=ans_sql, stud_sql=stud_sql)
    time.sleep(5)
    print(correct)
    print("Hello world!Test From Seddon!!!!")
