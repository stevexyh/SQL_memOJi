#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
----------------------------------------------------------------------------------------------------
* Project Name : SQL_memOJi
* File Name    : forms.py
* Description  : Django Forms
* Create Time  : 2021-04-25 16:36:39
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
import coding.models


class QuesSetForm(ModelForm):
    '''For coding/questions-manage.html'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TODO(Steve X): style for `select2`
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control input-mask select2'
            })

    class Meta:
        model = coding.models.QuestionSet

        fields = [
            'initiator',
            'ques_set_name',
            'ques_set_desc',
            'create_sql',
        ]

        error_messages = {
            # 'xxx': {'required': _("xxx不能为空"), },
        }

        widgets = {
            'ques_set_desc': Textarea(attrs={'rows': 8}),
        }
