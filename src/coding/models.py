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
    | db_name               | varchar             |      | UNI |             |
    | create_sql            | varchar             |      |     |             |
    | initiator             | varchar             |      | API |             |
    '''

    ques_set_id = models.AutoField(verbose_name=_('题库ID'), primary_key=True)
    ques_set_name = models.CharField(verbose_name=_('题库名称'), max_length=100)
    ques_set_desc = models.TextField(verbose_name=_('题库描述'), null=True, blank=True)
    db_name = models.CharField(verbose_name=_('数据库名称'), unique=True, max_length=100, default='null')
    create_sql = models.TextField(verbose_name=_('创建SQL'))
    initiator = models.ForeignKey(verbose_name=_('发起人'), to='user.Teacher', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = '题库'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.ques_set_id) + '-' + self.ques_set_name


# XXX(Steve X): many-to-many intermediary models
class Question(models.Model):
    '''
    Question Table
    | 字段名                 | 数据类型             | 非空  | Key | 默认值       |
    |-----------------------|---------------------|------|-----|-------------|
    | ques_id               | varchar             |      | PRI |             |
    | ques_name             | varchar             | NULL |     | 未命名       |
    | ques_set              | varchar             |      | FK  |             |
    | ques_difficulty       | int                 | NULL |     |             |
    | ques_desc             | varchar             |      |     |             |
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
    ques_name = models.CharField(verbose_name=_('题目名称'), max_length=100, null=True, default=_('未命名'))
    ques_set = models.ForeignKey(verbose_name=_('所属题库'), to=QuestionSet, on_delete=models.CASCADE)
    ques_difficulty = models.IntegerField(verbose_name=_('题目难度'), choices=Difficulty.choices, default=Difficulty.UNKNOWN)
    ques_desc = models.TextField(verbose_name=_('题目描述'))
    ques_ans = models.TextField(verbose_name=_('标准答案'))
    initiator = models.ForeignKey(verbose_name=_('发起人'), to='user.Teacher', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = '题目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.ques_id) + '-' + self.ques_name


# XXX(Steve X): many-to-many intermediary models
class Paper(models.Model):
    '''
    Paper Table
    | 字段名                 | 数据类型             | 非空  | Key | 默认值       |
    |-----------------------|---------------------|------|-----|-------------|
    | paper_id              | varchar             |      | PRI |             |
    | paper_name            | varchar             |      |     |             |
    | publish_time          | datetime            |      |     |             |
    | paper_desc            | varchar             | NULL |     |             |
    | initiator             | varchar             |      | API |             |
    | question              | varchar             |      | M2M |             |
    '''

    paper_id = models.AutoField(verbose_name=_('试卷ID'), primary_key=True)
    paper_name = models.CharField(verbose_name=_('试卷名称'), max_length=100)
    publish_time = models.DateTimeField(verbose_name=_('发布时间'), auto_now_add=True)
    paper_desc = models.TextField(verbose_name=_('试卷描述'), null=True, blank=True)
    initiator = models.ForeignKey(verbose_name=_('发起人'), to='user.Teacher', on_delete=models.SET_NULL, null=True)
    question = models.ManyToManyField(verbose_name=_('题目列表'), to=Question)

    class Meta:
        verbose_name = '试卷'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.paper_id) + '-' + self.paper_name


class Exam(models.Model):
    '''
    Exam Table
    | 字段名                 | 数据类型             | 非空  | Key    | 默认值       |
    |-----------------------|---------------------|------|--------|-------------|
    | exam_id               | varchar             |      | PRI    |             |
    | exam_name             | varchar             |      |        | 未命名       |
    | paper                 | varchar             |      | FK     |             |
    | start_time            | datetime            |      |        |             |
    | end_time              | datetime            |      |        |             |
    | publish_time          | datetime            |      |        |             |
    | desc                  | varchar             | NULL |        |             |
    | active                | bool                |      |        | True        |
    | classroom             | varchar             |      | M2M    |             |
    '''

    exam_id = models.AutoField(verbose_name=_('考试ID'), primary_key=True)
    exam_name = models.CharField(verbose_name=_('考试名称'), max_length=100, default=_('未命名'))
    paper = models.ForeignKey(verbose_name=_('试卷'), to=Paper, on_delete=models.CASCADE)
    start_time = models.DateTimeField(verbose_name=_('开始时间'), default=None)
    end_time = models.DateTimeField(verbose_name=_('结束时间'), default=None)
    publish_time = models.DateTimeField(verbose_name=_('发布时间'), auto_now_add=True)
    desc = models.TextField(verbose_name=_('描述'), null=True, blank=True)
    active = models.BooleanField(verbose_name=_('发布状态'), default=False)
    classroom = models.ManyToManyField(verbose_name=_('分配班级'), to='user.Classroom')

    def __str__(self):
        return str(self.paper)

    class Meta:
        verbose_name = '考试'
        verbose_name_plural = verbose_name


class Exercise(models.Model):
    '''
    Exercise Table
    | 字段名                 | 数据类型             | 非空  | Key    | 默认值       |
    |-----------------------|---------------------|------|--------|-------------|
    | exer_id               | varchar             |      | PRI    |             |
    | exer_name             | varchar             |      |        | 未命名       |
    | paper                 | varchar             |      | FK,UNI |             |
    | publish_time          | datetime            |      |        |             |
    | desc                  | varchar             | NULL |        |             |
    | active                | bool                |      |        | True        |
    | classroom             | varchar             |      | M2M    |             |
    '''

    exer_id = models.AutoField(verbose_name=_('练习ID'), primary_key=True)
    exer_name = models.CharField(verbose_name=_('练习名称'), max_length=100, default=_('未命名'))
    paper = models.ForeignKey(verbose_name=_('试卷'), to=Paper, on_delete=models.CASCADE)
    publish_time = models.DateTimeField(verbose_name=_('发布时间'), auto_now_add=True)
    desc = models.TextField(verbose_name=_('描述'), null=True, blank=True)
    active = models.BooleanField(verbose_name=_('发布状态'), default=False)
    classroom = models.ManyToManyField(verbose_name=_('分配班级'), to='user.Classroom')

    def __str__(self):
        return str(self.paper)

    class Meta:
        verbose_name = '练习'
        verbose_name_plural = verbose_name


class QuesAnswerRec(models.Model):
    '''
    Question Answer Record Table
    | 字段名                 | 数据类型             | 非空  | Key | 默认值       |
    |-----------------------|---------------------|------|-----|-------------|
    | rec_id                | varchar             |      | PRI |             |
    | user                  | varchar             |      | API |             |
    | question              | varchar             |      | FK  |             |
    | ans_status            | int                 |      |     | -1          |
    | submit_cnt            | int                 |      |     | 0           |
    '''

    class AnsStatus(models.IntegerChoices):
        '''Enumeration of answer status'''

        UNKNOWN = -1, _('未知')
        AC = 0, _('答案正确')
        WA = 1, ('答案错误')
        RE = 2, _('运行异常')

    rec_id = models.AutoField(verbose_name=_('记录ID'), primary_key=True)
    user = models.ForeignKey(verbose_name=_('用户'), to='user.User', on_delete=models.CASCADE)
    question = models.ForeignKey(verbose_name=_('题目'), to=Question, on_delete=models.DO_NOTHING)
    ans_status = models.IntegerField(verbose_name=_('答案正确性'), choices=AnsStatus.choices, default=AnsStatus.UNKNOWN)
    submit_cnt = models.IntegerField(verbose_name=_('提交次数'), default=0)

    class Meta:
        verbose_name = '题目作答记录'
        verbose_name_plural = verbose_name


# TODO(Steve X): Exam & Exer record
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
    paper = models.ForeignKey(verbose_name=_('试卷'), to=Paper, on_delete=models.DO_NOTHING)
    start_time = models.DateTimeField(verbose_name=_('开始时间'))
    end_time = models.DateTimeField(verbose_name=_('交卷时间'))
    score = models.IntegerField(verbose_name=_('总成绩'), default=0)

    class Meta:
        verbose_name = '试卷作答记录'
        verbose_name_plural = verbose_name
