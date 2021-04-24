#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
----------------------------------------------------------------------------------------------------
* Project Name : SQL_memOJi
* File Name    : models.py
* Description  : 
* Create Time  : 2021-04-04 00:46:35
* Version      : 1.0
* Author       : Steve X
* GitHub       : https://github.com/Steve-Xyh/SQL_memOJi
----------------------------------------------------------------------------------------------------
* Notice
- 
- 
----------------------------------------------------------------------------------------------------
'''


import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.


class QuestionSet(models.Model):
    '''
    QuestionSet Table
    | 字段名                 | 数据类型             | 非空  | Key | 默认值       |
    |-----------------------|---------------------|------|-----|-------------|
    | ques_set_id           | varchar             |      | PRI |             |
    | ques_set_name         | varchar             |      |     |             |
    | ques_set_desc         | varchar             |      |     |             |
    | create_sql            | varchar             |      |     |             |
    | initiator             | varchar             |      | API |             |
    '''

    ques_set_id = models.AutoField(verbose_name=_('题库ID'), primary_key=True)
    ques_set_name = models.CharField(verbose_name=_('题库名称'), max_length=100)
    ques_set_desc = models.TextField(verbose_name=_('题库描述'))
    create_sql = models.TextField(verbose_name=_('创建SQL'))
    initiator = models.ForeignKey(verbose_name=_('发起人'), to='user.Teacher', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = '题库'
        verbose_name_plural = verbose_name


# XXX(Steve X): many-to-many intermediary models
class Question(models.Model):
    '''
    Question Table
    | 字段名                 | 数据类型             | 非空  | Key | 默认值       |
    |-----------------------|---------------------|------|-----|-------------|
    | ques_id               | varchar             |      | PRI |             |
    | ques_name             | varchar             | NULL |     |             |
    | ques_set_id           | varchar             |      | FK  |             |
    | ques_difficulty       | int                 | NULL |     |             |
    | ques_desc             | varchar             | NULL |     |             |
    | ques_ans              | varchar             |      |     |             |
    | initiator             | varchar             |      | API |             |
    '''

    class Difficulty(models.IntegerChoices):
        '''Enumeration of question difficulty'''

        UNKNOWN = -1, _('未知')
        EASY = 0, _('简单')
        MEDIUM = 1, ('中等')
        HARD = 2, _('困难')

    ques_id = models.AutoField(verbose_name=_('题目ID'), primary_key=True)
    ques_name = models.CharField(verbose_name=_('题目名称'), max_length=100, null=True, default=_('未命名题目'))
    ques_set = models.ForeignKey(verbose_name=_('所属题库'), to=QuestionSet, on_delete=models.CASCADE)
    ques_difficulty = models.IntegerField(verbose_name=_('题目难度'), choices=Difficulty.choices, default=Difficulty.UNKNOWN)
    ques_desc = models.TextField(verbose_name=_('题目描述'))
    ques_ans = models.TextField(verbose_name=_('标准答案'))
    initiator = models.ForeignKey(verbose_name=_('发起人'), to='user.Teacher', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = '题目'
        verbose_name_plural = verbose_name


# XXX(Steve X): many-to-many intermediary models
class Paper(models.Model):
    '''
    Paper Table
    | 字段名                 | 数据类型             | 非空  | Key | 默认值       |
    |-----------------------|---------------------|------|-----|-------------|
    | paper_id              | varchar             |      | PRI |             |
    | paper_name            | varchar             |      |     |             |
    | paper_type            | int                 |      |     |             |
    | publish_time          | datetime            |      |     |             |
    | start_time            | datetime            |      |     |             |
    | end_time              | datetime            |      |     |             |
    | paper_active          | bool                |      |     | True        |
    | paper_desc            | varchar             |      |     |             |
    | initiator             | varchar             |      | API |             |
    | classroom             | varchar             |      | M2M |             |
    | question              | varchar             |      | M2M |             |
    '''

    class PaperType(models.IntegerChoices):
        '''Enumeration of paper type'''

        EXERCISE = 0, _('练习')
        EXAM = 1, ('考试')

    paper_id = models.AutoField(verbose_name=_('试卷ID'), primary_key=True)
    paper_name = models.CharField(verbose_name=_('试卷名称'), max_length=100)
    paper_type = models.IntegerField(verbose_name=_('试卷类型'), choices=PaperType.choices)
    publish_time = models.DateTimeField(verbose_name=_('发布时间'))
    start_time = models.DateTimeField(verbose_name=_('开始时间'))
    end_time = models.DateTimeField(verbose_name=_('结束时间'))
    paper_active = models.BooleanField(verbose_name=_('发布状态'), default=False)
    paper_desc = models.TextField(verbose_name=_('试卷描述'), null=True)
    initiator = models.ForeignKey(verbose_name=_('发起人'), to='user.Teacher', on_delete=models.SET_NULL, null=True)
    classroom = models.ManyToManyField(verbose_name=_('分配班级'), to='user.Classroom')
    question = models.ManyToManyField(verbose_name=_('题目列表'), to=Question)

    def __init__(self):
        super().__init__()
        self.publish_time = datetime.datetime.now()

    class Meta:
        verbose_name = '试卷'
        verbose_name_plural = verbose_name


class QuesAnswerRec(models.Model):
    '''
    Question Answer Record Table
    | 字段名                 | 数据类型             | 非空  | Key | 默认值       |
    |-----------------------|---------------------|------|-----|-------------|
    | rec_id                | varchar             |      | PRI |             |
    | student               | varchar             |      | API |             |
    | question              | varchar             |      | FK  |             |
    | ans_status            | bool                |      |     | False       |
    | submit_cnt            | int                 |      |     | 0           |
    '''

    rec_id = models.AutoField(verbose_name=_('记录ID'), primary_key=True)
    student = models.ForeignKey(verbose_name=_('学生'), to='user.Student', on_delete=models.CASCADE)
    question = models.ForeignKey(verbose_name=_('题目'), to=Question, on_delete=models.DO_NOTHING)
    ans_status = models.BooleanField(verbose_name=_('答案正确性'), default=False)
    submit_cnt = models.IntegerField(verbose_name=_('提交次数'), default=0)

    class Meta:
        verbose_name = '题目作答记录'
        verbose_name_plural = verbose_name


class PaperAnswerRec(models.Model):
    '''
    Paper Answer Record Table
    | 字段名                 | 数据类型             | 非空  | Key | 默认值       |
    |-----------------------|---------------------|------|-----|-------------|
    | rec_id                | varchar             |      | PRI |             |
    | student               | varchar             |      | API |             |
    | paper                 | varchar             |      | FK  |             |
    | start_time            | datetime            |      |     |             |
    | end_time              | datetime            |      |     |             |
    | score                 | int                 |      |     | 0           |
    '''

    rec_id = models.AutoField(verbose_name=_('记录ID'), primary_key=True)
    student = models.ForeignKey(verbose_name=_('学生'), to='user.Student', on_delete=models.CASCADE)
    paper = models.ForeignKey(verbose_name=_('题目'), to=Paper, on_delete=models.DO_NOTHING)
    start_time = models.DateTimeField(verbose_name=_('开始时间'))
    end_time = models.DateTimeField(verbose_name=_('交卷时间'))
    score = models.IntegerField(verbose_name=_('总成绩'), default=0)

    class Meta:
        verbose_name = '试卷作答记录'
        verbose_name_plural = verbose_name
