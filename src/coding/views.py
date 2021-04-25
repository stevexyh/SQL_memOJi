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


from django.shortcuts import render, redirect
from django.views import View
from django.contrib import auth
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from coding import forms

# Create your views here.


def exams_manage(request):
    '''Render exams-manage template'''

    return render(request, 'coding/exams-manage.html')


#------------------------------------Questions Manage Page-----------------------------------#
def questions_manage(request):
    '''Render questions-manage template'''

    ques_set_form = forms.QuesSetForm()
    question_form = forms.QuestionForm()

    content = {
        'ques_set_form': ques_set_form,
        'question_form': question_form,
    }

    return render(request, 'coding/questions-manage.html', context=content)


def ques_set_add(request):
    '''Add question set in questions-manage page'''

    ques_set_form = forms.QuesSetForm(request.POST)

    if ques_set_form.is_valid():
        ques_set_form.save()

    return redirect('coding:questions-manage')


def question_add(request):
    '''Add question in questions-manage page'''

    question_form = forms.QuestionForm(request.POST)

    if question_form.is_valid():
        question_form.save()

    return redirect('coding:questions-manage')
#--------------------------------------------END---------------------------------------------#


def coding(request):
    '''Render coding template'''

    return render(request, 'coding/coding.html')


def coding_editor(request):
    '''Render coding-editor template'''

    return render(request, 'coding/coding-editor.html')


def statistics(request):
    '''Render statistics template'''

    return render(request, 'coding/statistics.html')
