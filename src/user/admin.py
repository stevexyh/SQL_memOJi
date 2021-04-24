#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
----------------------------------------------------------------------------------------------------
* Project Name : SQL_memOJi
* File Name    : admin.py
* Description  :
* Create Time  : 2021-04-04 00:42:50
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
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from . import models


admin.site.site_header = 'memOJi管理后台'
admin.site.site_title = 'memOJi'


# Register your models here.


# Fields: 'email', 'password', 'priority', 'school', 'full_name', 'internal_id', 'college_name', 'join_status'
@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    '''Views displayed in admin backends'''

    list_display = ['username', 'internal_id', 'email', 'priority', 'school', 'full_name', 'college_name', 'join_status']
    list_filter = ['priority', 'is_staff', 'is_superuser', 'is_active']
    ordering = ['username']
    search_fields = list_display

    fieldsets = (
        (_('帐号信息'), {'fields': (
            'username',
            'password',
            'priority'
        )}),
        (_('个人信息'), {'fields': (
            'full_name',
            'email',
            'internal_id',
            'school',
            'college_name',
            'join_status'
        )}),
        (_('权限'), {'fields': ('is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions')}),
        (_('重要日期'), {'fields': ('last_login', 'date_joined')})
    )

    add_fieldsets = (
        (_('帐号信息'), {'fields': (
            'username',
            'password1',
            'password2',
            'priority'
        )}),
        (_('个人信息'), {'fields': (
            'full_name',
            'email',
            'internal_id',
            'school',
            'college_name',
            'join_status'
        )}),
    )

    list_per_page = 30
    show_full_result_count = False


@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['user']


# Fields: 'user', 'classroom', 'join_status'
@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'classroom', 'join_status']


# Fields: 'school_id', 'school_name', 'school_name_en', 'school_abbr'
@admin.register(models.School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['school_id', 'school_name', 'school_name_en', 'school_abbr']


# Fields: 'class_id', 'school_id', 'class_name', 'teacher_name', 'class_desc', 'stud_list'
@admin.register(models.Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['class_id', 'school', 'class_name', 'teacher', 'class_desc', 'stud_list']
