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
from django.views import View
from django.contrib import auth
from django.utils.translation import gettext_lazy as _

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


class AuthLogin(View):
    '''Render auth-login template in CBV'''

    def get(self, request):
        return render(request, 'user/auth-login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        success = bool(user)
        msg = _('登录成功') if success else _('用户名或密码错误')
        content = {
            'user': user,
            'success': success,
            'msg': msg,
        }

        if not success:
            return render(request, 'user/auth-login.html', context=content, status=401)

        auth.login(request, user=user)
        return render(request, 'user/auth-status.html', context=content)


def auth_logout(request):
    '''Log out user'''

    user = request.session.get('username')
    auth.logout(request)
    content = {
        'user': user,
        'msg': _('登出成功'),
    }
    return render(request, 'user/auth-login.html', context=content)


def auth_status(request):
    '''Render auth-status template'''

    return render(request, 'user/auth-status.html')


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
