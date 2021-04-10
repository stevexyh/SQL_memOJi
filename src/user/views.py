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
from user.models import User

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


class AuthRegister(View):
    '''Render auth-register template in CBV'''

    def get(self, request):
        return render(request, 'user/auth-register.html')

    # TODO(Steve X): Finish frontend validation for every tab on click 'next'
    def post(self, request):
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        school_name = request.POST.get('school_name')
        class_id = request.POST.get('class_id')
        full_name = request.POST.get('full_name')
        internal_id = request.POST.get('internal_id')

        msg = ''
        if User.objects.filter(username=username):
            msg = _('此用户名已存在, 请更换另一个或求助管理员')
            fail = True
        elif User.objects.filter(email=email):
            msg = _('此邮箱已注册, 请更换另一个或求助管理员')
            fail = True
        elif password1 != password2:
            msg = _('两次密码输入不一致')
            fail = True
        else:
            try:
                new_user = User.objects.create_user(username=username, password=password2, email=email)
                new_user.school_name = school_name
                new_user.class_id = class_id
                new_user.full_name = full_name
                new_user.internal_id = internal_id

                new_user.save()
                fail = False
            except Exception as exc:
                msg = _('注册异常: ') + str(exc)
                fail = True
                print(exc)

        content = {
            'fail': fail,
            'msg': msg,
        }

        return render(request, 'user/auth-register-done.html', context=content)


def auth_register_done(request):
    '''Render auth-register-done template'''

    return render(request, 'user/auth-register-done.html')
#--------------------------------------------END---------------------------------------------#


#--------------------------------------Management Pages--------------------------------------#
def class_manage(request):
    '''Render class-manage template'''

    return render(request, 'user/class-manage.html')


def class_details(request):
    '''Render class-details template'''

    return render(request, 'user/class-details.html')


class UserInfo(View):
    '''Render user-info template'''

    RBF = '# TODO(Steve X): REMOVE BEFORE FLIGHT'

    def get(self, request):
        not_login = _('未登录')
        null = 'NULL'

        user = request.user

        full_name = user.full_name if user.is_authenticated else not_login
        username = user.username if user.is_authenticated else not_login
        email = user.email if user.is_authenticated else not_login
        school_name = user.school_name if user.is_authenticated else not_login  # TODO(Steve X): REMOVE BEFORE FLIGHT
        college_name = user.college_name if user.is_authenticated else not_login
        internal_id = user.internal_id if user.is_authenticated else not_login
        class_id = user.class_id if user.is_authenticated else not_login  # TODO(Steve X): REMOVE BEFORE FLIGHT
        priority = user.get_priority_display() if user.is_authenticated else not_login
        join_status = user.is_authenticated and user.join_status != User.JoinStatus.OUT_OF_LIST or user.is_superuser
        teacher_name = self.RBF

        content = {
            'full_name': full_name,
            'username': username,
            'email': email,
            'school_name': school_name,
            'college_name': college_name,
            'internal_id': internal_id,
            'class_id': class_id,
            'priority': priority,
            'join_status': join_status,
            'join_status_display': _('认证') if join_status else _('未认证'),
            'join_status_color': 'success' if join_status else 'warning',
            'teacher_name': teacher_name,
        }

        for k in content:
            content[k] = content[k] if content[k] != '' else f'{k}: {null}'

        return render(request, 'user/user-info.html', context=content)

    def post(self, request):
        # TODO(Steve X): edit user info
        pass
#--------------------------------------------END---------------------------------------------#
