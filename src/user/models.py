#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
----------------------------------------------------------------------------------------------------
* Project Name : SQL_memOJi
* File Name    : models.py
* Description  :
* Create Time  : 2021-04-04 00:43:08
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
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.


class User(AbstractUser):
    '''
    User Table
    | 字段名                 | 数据类型             | 非空  | Key | 默认值       |
    |-----------------------|---------------------|------|-----|-------------|
    | email                 | varchar             |      | PRI |             |
    | password              | varchar             |      |     |             |
    | priority              | int                 |      |     | 0           |
    | school_name           | varchar             |      | FK  | 西北工业大学  |
    | full_name             | varchar             |      |     |             |
    | internal_id           | varchar             |      | UNI |             |
    | college_name          | varchar             |      |     |             |
    | class_id              | varchar             |      | FK  |             |
    | join_status           | int                 |      |     | 0           |
    | register_time         | datetime            |      |     |             |
    '''

    class UserType(models.IntegerChoices):
        '''Enumeration of user priority'''

        STUDENT = 0, _('学生')
        TEACHER = 1, ('教师')
        ADMIN = 2, _('管理员')

    class JoinStatus(models.IntegerChoices):
        '''Enumeration of user join_status'''

        OUT_OF_LIST = 0, _('名单之外')
        UNJOINED = 1, _('未加入')
        JOINED = 2, _('已加入')
        ADMIN = 3, _('管理员')

    # username is defined in AbstractUser.username
    # password is defined in AbstractBaseUser.password
    # register_time is defined in AbstractUser.date_joined

    # TODO(Steve X): REMOVE BEFORE FLIGHT(primary_key -> uuid)
    email = models.EmailField(verbose_name=_('电子邮件'), primary_key=True)
    priority = models.IntegerField(verbose_name=_('权限等级'), choices=UserType.choices, default=0)

    # TODO(Steve X): REMOVE BEFORE FLIGHT(CharField -> ForeignKey)
    school_name = models.CharField(verbose_name=_('学校全称'), max_length=50, default=_('西北工业大学'))
    full_name = models.CharField(verbose_name=_('真实姓名'), max_length=30)
    internal_id = models.CharField(verbose_name=_('学工号'), max_length=30, unique=True)
    college_name = models.CharField(verbose_name=_('学院全称'), max_length=150, blank=True)
    class_id = models.CharField(verbose_name=_('班级ID'), max_length=30)  # TODO(Steve X): REMOVE BEFORE FLIGHT(CharField -> ForeignKey)
    join_status = models.IntegerField(verbose_name=_('加入状态'), choices=JoinStatus.choices, default=0)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name', 'internal_id']
