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
#XXX(Seddon):默认按照中国时区
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self,obj)

def calendar(request):
    '''Render calendar template'''
    identity = request.user.identity()
    print(identity)
    if request.user.is_superuser:  # 超级用户可查看所有数据
        conditions = {
            'active' : True
        }
        exams_list = Exam.objects.order_by('publish_time').filter(**conditions)
        exer_list = Exercise.objects.order_by('publish_time').filter(**conditions)
    elif identity == 'teacher':
        conditions = {
            'classroom__in' : request.user.teacher.teach_room(),
            'active' : True
        }
        exams_list = Exam.objects.order_by('publish_time').filter(**conditions)
        exer_list = Exercise.objects.order_by('publish_time').filter(**conditions)
    elif identity == 'teacher_student':
        conditions_teacher = {
            'classroom__in' : request.user.teacher.teach_room(),
            'active' : True
        }
        conditions_student = {
            'classroom' : request.user.student.classroom,
            'active' : True
        }
        exams_list_teacher = Exam.objects.order_by('publish_time').filter(**conditions_teacher)
        exer_list_teacher = Exercise.objects.order_by('publish_time').filter(**conditions_teacher)
        exams_list_student = Exam.objects.order_by('publish_time').filter(**conditions_student)
        exer_list_student = Exercise.objects.order_by('publish_time').filter(**conditions_student)
        exams_list = exams_list_teacher | exams_list_student
        exer_list  = exer_list_teacher  | exer_list_student
    elif identity == 'student':
        conditions = {
            'classroom' : request.user.student.classroom,
            'active' : True
        }
        exams_list = Exam.objects.order_by('publish_time').filter(**conditions)
        exer_list = Exercise.objects.order_by('publish_time').filter(**conditions)
    else:
        exams_list = Exam.objects.none()
        exer_list = Exercise.objects.none()

    content = {
        'exams_list': exams_list,
        'exer_list': exer_list,
    }
    calc_list = []
    # {% url 'coding:coding-editor' 'exam' exam.exam_id exam.first_ques %}
    for exam in exams_list:
        calc_list.append({'title':exam.exam_name,'start':exam.start_time + datetime.timedelta(hours=8),'end':exam.end_time + datetime.timedelta(hours=8), 'url':"/coding/coding-editor/exam/" + str(exam.exam_id )+  "/" + str(exam.first_ques)})
    for exer in exer_list:
        # calc_list.append({'title':exer.exer_name,'start':exer.publish_time + datetime.timedelta(hours=8)})
        calc_list.append({'title':exer.exer_name,'start':exer.start_time + datetime.timedelta(hours=8),'end':exer.end_time + datetime.timedelta(hours=8), 'url':"/coding/coding-editor/exer/" + str(exer.exer_id )+  "/" + str(exer.first_ques)})
    return render(request, 'iCalendar/calendar.html', {'spots':json.dumps(calc_list,cls=DateEncoder)})