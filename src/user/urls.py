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

from django.urls import path, include
from . import views

app_name = 'user'
urlpatterns = [
    path('', views.base, name='base'),
    path('base/', views.base, name='base'),
]
