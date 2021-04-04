#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
----------------------------------------------------------------------------------------------------
* Project Name : SQL_memOJi
* File Name    : urls.py
* Description  : 
* Create Time  : 2021-04-04 15:45:56
* Version      : 1.0
* Author       : Steve X
* GitHub       : https://github.com/Steve-Xyh/SQL_memOJi
----------------------------------------------------------------------------------------------------
* Notice
- 
- 
----------------------------------------------------------------------------------------------------
'''

from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    # Global Pages
    path('', views.index, name='index'),
    path('base/', views.base, name='base'),
    path('blank/', views.blank, name='blank'),

    # Auth Pages
    path('auth-base/', views.auth_base, name='auth-base'),
    path('auth-login/', views.auth_login, name='auth-login'),
    path('auth-recoverpw/', views.auth_recoverpw, name='auth-recoverpw'),
    path('auth-register/', views.auth_register, name='auth-register'),

    # Management Pages
    path('class-manage/', views.class_manage, name='class-manage'),
    path('class-details/', views.class_details, name='class-details'),
    path('user-info/', views.user_info, name='user-info'),
]
