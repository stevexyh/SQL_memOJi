#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
----------------------------------------------------------------------------------------------------
* Project Name : SQL_memOJi
* File Name    : admin.py
* Description  : 
* Create Time  : 2021-04-04 00:46:26
* Version      : 1.0
* Author       : Steve X
* GitHub       : https://github.com/Steve-Xyh/SQL_memOJi
----------------------------------------------------------------------------------------------------
* Notice
- 
- 
----------------------------------------------------------------------------------------------------
'''


from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models


# Register your models here.


# Fields: 'ques_id', 'ques_name', 'ques_set_id', 'ques_difficulty', 'ques_desc', 'ques_ans', 'initiator'
@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['ques_id', 'ques_name', 'ques_set_id', 'ques_difficulty', 'ques_desc', 'ques_ans', 'initiator']


# Fields: 'ques_set_id', 'ques_set_name', 'ques_set_desc', 'create_sql', 'initiator'
@admin.register(models.QuestionSet)
class QuestionSetAdmin(admin.ModelAdmin):
    list_display = ['ques_set_id', 'ques_set_name', 'ques_set_desc', 'create_sql', 'initiator']


# Fields: 'paper_id', 'paper_name', 'paper_type', 'publish_time', 'start_time', 'end_time', 'paper_active',
# Fields: 'paper_desc', 'initiator', 'classroom', 'question'
@admin.register(models.Paper)
class PaperAdmin(admin.ModelAdmin):

    class ClassroomInline(admin.TabularInline):
        model = models.Paper.classroom.through

    class QuestionInline(admin.TabularInline):
        model = models.Paper.question.through

    list_display = [
        'paper_id', 'paper_name', 'paper_type', 'publish_time', 'start_time',
        'end_time', 'paper_active', 'paper_desc', 'initiator',
    ]

    inlines = [ClassroomInline, QuestionInline]


# Fields: 'rec_id', 'student', 'question', 'ans_status', 'submit_cnt'
@admin.register(models.QuesAnswerRec)
class QuesAnswerRecAdmin(admin.ModelAdmin):
    list_display = ['rec_id', 'student', 'question', 'ans_status', 'submit_cnt']


# Fields: 'rec_id', 'student', 'paper', 'start_time', 'end_time', 'score',
@admin.register(models.PaperAnswerRec)
class PaperAnswerRecAdmin(admin.ModelAdmin):
    list_display = ['rec_id', 'student', 'paper', 'start_time', 'end_time', 'score', ]
