#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
----------------------------------------------------------------------------------------------------
* Project Name : SQL_memOJi
* File Name    : forms.py
* Description  : Django Forms
* Create Time  : 2021-04-22 15:37:02
* Version      : 1.0
* Author       : Steve X
* GitHub       : https://github.com/Steve-Xyh/SQL_memOJi
----------------------------------------------------------------------------------------------------
* Notice
-
-
----------------------------------------------------------------------------------------------------
'''


from django.forms import ModelForm, Textarea
from django.utils.translation import gettext_lazy as _
import user.models


class UserInfoForm(ModelForm):
    '''For user/user-info.html'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control input-mask select2'
            })

    class Meta:
        model = user.models.User

        fields = [
            'full_name',
            'username',
            'email',
        ]

        error_messages = {
            'full_name': {'required': _("真实姓名不能为空"), },
            'username': {'required': _("用户名不能为空"), },
            'email': {'required': _("电子邮件不能为空"), },
        }


class StudentForm(ModelForm):
    '''For user/user-info.html'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TODO(Steve X): style for `select2`
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control input-mask select2'
            })

    class Meta:
        model = user.models.Student

        fields = [
            'classroom',
        ]

        error_messages = {
            'classroom': {'required': _("班级不能为空"), },
        }


class ClassroomForm(ModelForm):
    '''For user/class-manage.html & class-details.html'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TODO(Steve X): style for `select2`
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control input-mask select2'
            })

    class Meta:
        model = user.models.Classroom

        fields = [
            'teacher',
            'class_name',
            'class_desc',
        ]

        error_messages = {
            'classroom': {'required': _("班级不能为空"), },
            'teacher': {'required': _("负责教师不能为空"), },
        }

        widgets = {
            'class_desc': Textarea(attrs={'rows': 8}),
        }
