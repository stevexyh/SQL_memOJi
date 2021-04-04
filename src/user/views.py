#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
----------------------------------------------------------------------------------------------------
* Project Name : SQL_memOJi
* File Name    : views.py
* Description  : 
* Create Time  : 2021-04-04 00:43:27
* Version      : 1.0
* Author       : Steve X
* GitHub       : https://github.com/Steve-Xyh/SQL_memOJi
----------------------------------------------------------------------------------------------------
* Notice
- 
- 
----------------------------------------------------------------------------------------------------
'''


from django.shortcuts import render

# Create your views here.


#----------------------------------------Global Pages----------------------------------------#
def base(request):
    '''Render base template'''

    return render(request, 'base.html')


def blank(request):
    '''Render blank template'''

    return render(request, 'pages-starter.html')


def index(request):
    '''Render index template'''

    return render(request, 'index.html')
#--------------------------------------------END---------------------------------------------#


#-----------------------------------------Auth Pages-----------------------------------------#
def auth_base(request):
    '''Render auth-base template'''

    return render(request, 'user/auth-base.html')


def auth_login(request):
    '''Render auth-login template'''

    return render(request, 'user/auth-login.html')


def auth_recoverpw(request):
    '''Render auth-recoverpw template'''

    return render(request, 'user/auth-recoverpw.html')


def auth_register(request):
    '''Render auth-register template'''

    return render(request, 'user/auth-register.html')
#--------------------------------------------END---------------------------------------------#


#--------------------------------------Management Pages--------------------------------------#
def class_manage(request):
    '''Render class-manage template'''

    return render(request, 'user/class-manage.html')


def class_details(request):
    '''Render class-details template'''

    return render(request, 'user/class-details.html')


def user_info(request):
    '''Render user-info template'''

    return render(request, 'user/user-info.html')
#--------------------------------------------END---------------------------------------------#
