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


from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from user.models import User


class UserInfoForm(ModelForm):
    '''For user/user-info.html'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TODO(Steve X): style for `select2`
        for field in self.fields.values():
            field.widget.attrs = {
                'class': 'form-control input-mask'
            }

    class Meta:
        model = User

        fields = [
            'school',
            'full_name',
            'username',
            'email',
            # 'class_id',
        ]

        error_messages = {
            'full_name': {'required': _("真实姓名不能为空"), },
            'username': {'required': _("用户名不能为空"), },
            'email': {'required': _("电子邮件不能为空"), },
            # 'class_id': {'required': _("班级ID不能为空"), },
        }
