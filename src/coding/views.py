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


import pymysql
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import auth
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from coding import forms
from coding import models
from utils import token as tk

# Create your views here.


def exams_manage(request):
    '''Render exams-manage template'''

    exams_list = models.Exam.objects.order_by('publish_time')
    exer_list = models.Exercise.objects.order_by('publish_time')
    next_exam = exams_list.first()

    content = {
        'exams_list': exams_list,
        'exer_list': exer_list,
        'next_exam': next_exam,
    }

    return render(request, 'coding/exams-manage.html', context=content)


#------------------------------------Questions Manage Page-----------------------------------#
def questions_manage_base(request):
    '''Render questions-manage-base template'''

    ques_set_form = forms.QuesSetForm(auto_id='id_qset_%s')
    question_form = forms.QuestionForm(auto_id='id_ques_%s')
    paper_form = forms.PaperForm(auto_id='id_paper_%s')

    question_list = models.Question.objects.all()
    ques_set_list = models.QuestionSet.objects.all()
    paper_list = models.Paper.objects.all()

    content = {
        'ques_set_form': ques_set_form,
        'question_form': question_form,
        'paper_form': paper_form,
        'question_list': question_list,
        'ques_set_list': ques_set_list,
        'paper_list': paper_list,
    }

    return render(request, 'coding/questions-manage-base.html', context=content)


def questions_manage(request):
    '''Render questions-manage template'''

    ques_set_form = forms.QuesSetForm(auto_id='id_qset_%s')
    question_form = forms.QuestionForm(auto_id='id_ques_%s')
    paper_form = forms.PaperForm(auto_id='id_paper_%s')

    question_list = models.Question.objects.all()
    ques_set_list = models.QuestionSet.objects.all()
    paper_list = models.Paper.objects.all()

    content = {
        'ques_set_form': ques_set_form,
        'question_form': question_form,
        'paper_form': paper_form,
        'question_list': question_list,
        'ques_set_list': ques_set_list,
        'paper_list': paper_list,
    }

    return render(request, 'coding/questions-manage.html', context=content)


# XXX(Steve X): database grants for teachers
def ques_set_add(request):
    '''Add question set in questions-manage page'''

    ques_set_form = forms.QuesSetForm(request.POST)
    host = tk.get_conf('mysql', 'host')
    port = int(tk.get_conf('mysql', 'port'))
    user = tk.get_conf('mysql', 'user')
    passwd = tk.get_conf('mysql', 'password')

    db = pymysql.Connect(host=host, port=port, user=user, passwd=passwd)
    cur = db.cursor()
    ques_set_name = request.POST.get('ques_set_name')
    qset_db_name = f'qset_{ques_set_name}'
    create_sql = request.POST.get('create_sql').replace('\n', '').replace('\\n', '')
    create_sql_list = create_sql.split(';')

    print(create_sql)
    print(type(create_sql))
    print('-'*40)
    print(create_sql_list)

    try:
        cur.execute(f"""create database {qset_db_name};""")
        cur.execute(f"""use {qset_db_name};""")

        for sql in create_sql_list:
            cur.execute(sql)

        db.commit()
        if ques_set_form.is_valid():
            ques_set_form.save()
    except Exception as exc:
        cur.execute(f"""drop database if exists {qset_db_name}""")
        db.rollback()
        print(exc)

    cur.close()
    db.close()

    return redirect('coding:questions-manage')


def question_add(request):
    '''Add question in questions-manage page'''

    question_form = forms.QuestionForm(request.POST)

    if question_form.is_valid():
        question_form.save()

    return redirect('coding:questions-manage')


# FIXME(Steve X): date time picker
def paper_add(request):
    '''Add paper in questions-manage page'''

    paper_form = forms.PaperForm(request.POST)

    if paper_form.is_valid():
        paper_form.save()
    else:
        print(paper_form.errors)

    return redirect('coding:questions-manage')
#--------------------------------------------END---------------------------------------------#


def coding(request):
    '''Render coding template'''

    exams_list = models.Exam.objects.order_by('publish_time')
    exer_list = models.Exercise.objects.order_by('publish_time')
    next_exam = exams_list.first()

    content = {
        'exams_list': exams_list,
        'exer_list': exer_list,
        'next_exam': next_exam,
    }

    return render(request, 'coding/coding.html', context=content)


def coding_editor(request, event_type, event_id, ques_id):
    '''Render coding-editor template'''

    question = models.Question.objects.get(ques_id=ques_id)

    if event_type == 'exam':
        event = models.Exam.objects.get(exam_id=event_id)
        event_name = event.exam_name
    elif event_type == 'exer':
        event = models.Exercise.objects.get(exer_id=event_id)
        event_name = event.exer_name
    else:
        # TODO(Steve X): 404 page
        return render(request, 'coding/coding.html')

    desc = '''
+----------------------------+
| Tables_in_qset_0507testsql |
+----------------------------+
| employee                   |
| v                          |
+----------------------------+
    '''

    content = {
        'event_type': event_type,
        'event': event,
        'event_name': event_name,
        'question': question,
        'desc': desc,
    }

    return render(request, 'coding/coding-editor.html', context=content)


def statistics(request):
    '''Render statistics template'''

    return render(request, 'coding/statistics.html')
