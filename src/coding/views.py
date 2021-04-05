#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
----------------------------------------------------------------------------------------------------
* Project Name : SQL_memOJi
* File Name    : views.py
* Description  : 
* Create Time  : 2021-04-04 00:46:48
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


def exams_manage(request):
    '''Render exams-manage template'''

    return render(request, 'coding/exams-manage.html')


def questions_manage(request):
    '''Render questions-manage template'''

    return render(request, 'coding/questions-manage.html')


def coding(request):
    '''Render coding template'''

    return render(request, 'coding/coding.html')


def coding_editor(request):
    '''Render coding-editor template'''

    return render(request, 'coding/coding-editor.html')
