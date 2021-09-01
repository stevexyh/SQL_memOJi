#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
----------------------------------------------------------------------------------------------------
* Project Name : SQL_memOJi
* File Name    : apis.py
* Description  : REST API
* Create Time  : 2021-09-01 23:20:52
* Version      : 1.0
* Author       : Steve X
* GitHub       : https://github.com/Steve-Xyh/SQL_memOJi
----------------------------------------------------------------------------------------------------
* Notice
- 
- 
----------------------------------------------------------------------------------------------------
'''


from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import serializers as srlz
from . import models


@api_view(['GET'])
def test_api(request):
    '''an API for test'''

    content = {
        'test key': 'TEST API',
    }

    return Response(data=content)


@api_view(['GET'])
def question_list(request):
    questions = models.Question.objects.all()
    serializer = srlz.QuestionSerializer(instance=questions, many=True)
    content = serializer.data

    return Response(data=content)
