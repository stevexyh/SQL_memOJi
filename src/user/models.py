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


class School(models.Model):
    '''
    School Table
    | 字段名                 | 数据类型             | 非空  | Key | 默认值       |
    |-----------------------|---------------------|------|-----|-------------|
    | school_id             | varchar             |      | PRI |             |
    | school_name           | varchar             |      | UNI |             |
    | school_name_en        | varchar             |      | UNI |             |
    | school_abbr           | varchar             |      | UNI | NPU         |
    '''

    school_id = models.AutoField(verbose_name=_('学校ID'), primary_key=True)
    school_name = models.CharField(verbose_name=_('学校全称'), max_length=150, unique=True, default=_('西北工业大学'))
    school_name_en = models.CharField(verbose_name=_('学校英文全称'), max_length=150, unique=True, default='Northwestern Polytechnical University')
    school_abbr = models.CharField(verbose_name=_('学校英文缩写'), max_length=50, unique=True, default='NPU')

    def __str__(self):
        return str(self.school_name)

    class Meta:
        verbose_name = '学校'
        verbose_name_plural = verbose_name


class User(AbstractUser):
    '''
    User Table
    | 字段名                 | 数据类型             | 非空  | Key | 默认值       |
    |-----------------------|---------------------|------|-----|-------------|
    | email                 | varchar             |      | PRI |             |
    | password              | varchar             |      |     |             |
    | priority              | int                 |      |     | 0           |
    | school                | varchar             |      | FK  | 西北工业大学  |
    | full_name             | varchar             |      |     |             |
    | internal_id           | varchar             |      | UNI |             |
    | college_name          | varchar             |      |     | 计算机学院   |
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

    # TODO(Steve X): REMOVE BEFORE FLIGHT(primary_key -> uuid)
    # user_id = models.AutoField(verbose_name=_('用户ID'), primary_key=True)
    # username is defined in AbstractUser.username
    # password is defined in AbstractBaseUser.password
    # register_time is defined in AbstractUser.date_joined

    email = models.EmailField(verbose_name=_('电子邮件'), primary_key=True)
    priority = models.IntegerField(verbose_name=_('权限等级'), choices=UserType.choices, default=0)

    school = models.ForeignKey(verbose_name=_('学校'), to=School, on_delete=models.SET_NULL, default=None, null=True, blank=False)
    full_name = models.CharField(verbose_name=_('真实姓名'), max_length=30)
    internal_id = models.CharField(verbose_name=_('学工号'), max_length=30, unique=True)
    college_name = models.CharField(verbose_name=_('学院全称'), max_length=150, blank=True,default=_('计算机学院'))
    join_status = models.IntegerField(verbose_name=_('加入状态'), choices=JoinStatus.choices, default=0)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name', 'internal_id']

    def __str__(self):
        return str(self.internal_id + '-' + self.full_name)

    def identity(self):
        is_student = hasattr(self, 'student') and self.student is not None
        is_teacher = hasattr(self, 'teacher') and self.teacher is not None
        if is_student and is_teacher:
            return 'teacher_student'
        elif is_student:
            return 'student'
        elif is_teacher:
            return 'teacher'
        else:
            return 'unknown'

class Teacher(models.Model):
    '''
    Teacher Table
    | 字段名                 | 数据类型             | 非空  | Key | 默认值       |
    |-----------------------|---------------------|------|-----|-------------|
    | user                  | varchar             |      | FK  |             |
    '''

    user = models.OneToOneField(to=User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return str(self.user)

    def teach_room(self):
        rooms = Classroom.objects.filter(teacher=self)
        return rooms
    def teach_stu(self):
        rooms = self.teach_room()
        students = Student.objects.filter(classroom__in = rooms)
        # query_stu = User.objects.filter(email__in=students)
        return students

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name


class Classroom(models.Model):
    '''
    Classroom Table
    | 字段名                 | 数据类型             | 非空  | Key  | 默认值      |
    |-----------------------|---------------------|------|------|------------|
    | class_id              | varchar             |      | PRI  |            |
    | school                | varchar             |      | FK   |            |
    | class_name            | varchar             |      |      |            |
    | teacher               | varchar             |      | FK   |            |
    | class_desc            | varchar             |      | NULL |            |
    | active                | bool                |      |      | True       |
    '''
    # | stud_list             | varchar(Python.List)|      |      |            |


    class_id = models.AutoField(verbose_name=_('班级ID'), primary_key=True)
    school = models.ForeignKey(verbose_name=_('学校'), to=School, on_delete=models.SET_NULL, default=None, null=True, blank=False)
    class_name = models.CharField(verbose_name=_('班级名称'), max_length=150)
    teacher = models.ForeignKey(verbose_name=_('负责教师'), to=Teacher, on_delete=models.SET_NULL, default=None, null=True, blank=False)
    class_desc = models.CharField(verbose_name=_('班级描述'), max_length=200, null=True, blank=True)
    active = models.BooleanField(verbose_name=_('有效状态'), default=True)
    # stud_list = models.CharField(verbose_name=_('学生列表'), max_length=2000, null=True, blank=True)

    def __str__(self):
        return str(self.class_name)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("user:class-details", kwargs={"class_id": self.class_id})

    # 装饰器property
    @property
    def students_count(self):
        # class-manage page students number
        detail = Classroom.objects.get(pk=self.class_id)
        count = detail.student_set.count()
        return count


    class Meta:
        verbose_name = '班级'
        verbose_name_plural = verbose_name


class Student(models.Model):
    '''
    Student Table
    | 字段名                 | 数据类型             | 非空  | Key | 默认值       |
    |-----------------------|---------------------|------|-----|-------------|
    | user                  | varchar             |      | FK  |             |
    | classroom             | varchar             |      | FK  |             |
    | join_status           | int                 |      |     | 0           |
    '''

    user = models.OneToOneField(to=User, on_delete=models.CASCADE, primary_key=True)
    classroom = models.ForeignKey(verbose_name=_('班级'), to=Classroom, on_delete=models.SET_NULL, default=None, null=True, blank=False)
    join_status = models.BooleanField(verbose_name=_('加入状态'), default=False)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = '学生'
        verbose_name_plural = verbose_name
