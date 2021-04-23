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
    | create_sql            | varchar             |      |     |             |
    '''

    class Meta:
        verbose_name = '题库'
        verbose_name_plural = verbose_name


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
    '''

    class Meta:
        verbose_name = '题目'
        verbose_name_plural = verbose_name


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
    '''

    class Meta:
        verbose_name = '试卷'
        verbose_name_plural = verbose_name


class AnswerRec(models.Model):
    '''
    AnswerRec Table
    | 字段名                 | 数据类型             | 非空  | Key | 默认值       |
    |-----------------------|---------------------|------|-----|-------------|
    | email                 | varchar             |      | API |             |
    | ques_id               | varchar             |      | FK  |             |
    | ans_status            | bool                |      |     | False       |
    | submit_cnt            | int                 |      |     | 0           |
    '''

    class Meta:
        verbose_name = '作答记录'
        verbose_name_plural = verbose_name
