#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
----------------------------------------------------------------------------------------------------
* Project Name : SQL_memOJi
* File Name    : views.py
* Description  : 
* Create Time  : 2021-04-04 00:48:04
* Version      : 1.0
* Author       : Steve X
* GitHub       : https://github.com/Steve-Xyh/SQL_memOJi
----------------------------------------------------------------------------------------------------
* Notice
- 
- 
----------------------------------------------------------------------------------------------------
'''

import json
from django.shortcuts import render
import datetime
from user.models import Student, User, Classroom
from coding.models import Exam,Exercise
#XXX(Seddon):默认按照中国市区
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self,obj)

def calendar(request):
    '''Render calendar template'''
    conditions = {
        'classroom' : request.user.student.classroom,
        'active' : True
    }
    exams_list = Exam.objects.order_by('publish_time').filter(**conditions)
    exer_list = Exercise.objects.order_by('publish_time').filter(**conditions)
    content = {
        'exams_list': exams_list,
        'exer_list': exer_list,
    }
    calc_list = []
    for exam in exams_list:
        calc_list.append({'title':exam.exam_name,'start':exam.start_time + datetime.timedelta(hours=8),'end':exam.end_time + datetime.timedelta(hours=8)})
    for exer in exer_list:
        calc_list.append({'title':exer.exer_name,'start':exer.publish_time + datetime.timedelta(hours=8)})
    return render(request, 'iCalendar/calendar.html', {'spots':json.dumps(calc_list,cls=DateEncoder)})
