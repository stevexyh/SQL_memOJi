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


from django.shortcuts import render

# Create your views here.
from user.models import Student, User, Classroom
from coding.models import Exam,Exercise

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
    return render(request, 'iCalendar/calendar.html')
