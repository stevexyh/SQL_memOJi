#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
----------------------------------------------------------------------------------------------------
* Project Name : SQL_memOJi
* File Name    : admin.py
* Description  : 
* Create Time  : 2021-04-04 00:46:26
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
from django.utils.translation import gettext_lazy as _
from . import models
from user.models import Classroom
from django import forms
# Register your models here.


# Fields: 'ques_id', 'ques_name', 'ques_set_id', 'ques_difficulty', 'ques_desc', 'ques_ans', 'initiator'
@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['ques_id', 'ques_name', 'ques_set_id', 'ques_difficulty', 'ques_desc', 'ques_ans', 'initiator']


# Fields: 'ques_set_id', 'ques_set_name', 'ques_set_desc', 'create_sql', 'initiator'
@admin.register(models.QuestionSet)
class QuestionSetAdmin(admin.ModelAdmin):
    list_display = ['ques_set_id', 'ques_set_name', 'ques_set_desc', 'db_name', 'create_sql', 'initiator']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["db_name"]
        else:
            return []


# Fields: 'paper_id', 'paper_name', 'publish_time', 'paper_desc', 'initiator', 'question',
@admin.register(models.Paper)
class PaperAdmin(admin.ModelAdmin):

    class QuestionInline(admin.TabularInline):
        model = models.Paper.question.through
    def get_queryset(self, request):
        # 接管查询请求
        results = super(PaperAdmin, self).get_queryset(request)
        identity = request.user.identity()
        if request.user.is_superuser:  # 超级用户可查看所有数据
            return results
        if identity == 'teacher' or identity == 'teacher_student':
            #TODO:(Seddon)设置公开字段 也可以看公开的试卷
            return models.Paper.objects.filter(initiator = request.user.teacher)
        else:
            return models.Paper.objects.none()

    list_display = [
        'paper_id', 'paper_name', 'paper_desc', 'initiator', 'publish_time',
    ]

    inlines = [QuestionInline]


# Fields: 'exam_id', 'exam_name', 'paper', 'start_time', 'end_time', 'publish_time', 'active', 'classroom'
@admin.register(models.Exam)
class ExamAdmin(admin.ModelAdmin):

    # class ClassroomInline(admin.TabularInline):
    #     model = models.Exam.classroom.through

    # inlines = [ClassroomInline]
    def get_queryset(self, request):
        # 接管查询请求
        results = super(ExamAdmin, self).get_queryset(request)
        identity = request.user.identity()
        if request.user.is_superuser:  # 超级用户可查看所有数据
            return results
        if identity == 'teacher' or identity == 'teacher_student':
            rooms = request.user.teacher.teach_room()
            return models.Exam.objects.filter(classroom__in = rooms).distinct()
        elif identity == 'student':
            return models.Exam.objects.none()
        else:
            return models.Exam.objects.none()

    def formfield_for_dbfield(self, field, **kwargs):
        login_user = kwargs['request'].user
        if not (login_user.is_superuser):
            if field.name == 'classroom':
                identity = login_user.identity()
                if identity == 'teacher' or identity == 'teacher_student':
                    exam_id = kwargs['request'].path.split('/')[4]
                    units = Classroom.objects.filter(teacher=login_user.teacher)
                    other_class = models.Exam.objects.get(exam_id=exam_id).classroom.all()
                    units = units | other_class
                    units = units.distinct()
                else:
                    units = Classroom.objects.none()
                return forms.ModelMultipleChoiceField (queryset=units,label="分配班级",help_text='按住 Ctrl 键(Mac 上的 Command 键) 来选择多个班级。如需多位老师多个班级同时考试，请使用管理员账号发布！')
        return super(ExamAdmin, self).formfield_for_dbfield(field, **kwargs)

    def classrooms(self,obj):
        return [bt.class_name for bt in obj.classroom.all()]
    classrooms.short_description = "分配班级"
    list_display = ['exam_id', 'exam_name', 'paper', 'start_time', 'end_time', 'publish_time', 'active', 'classrooms']


# Fields: 'exer_id', 'exer_name', 'paper', 'publish_time', 'active', 'classroom'
@admin.register(models.Exercise)
class ExerciseAdmin(admin.ModelAdmin):

    # class ClassroomInline(admin.TabularInline):
    #     model = models.Exercise.classroom.through

    # inlines = [ClassroomInline]
    def get_queryset(self, request):
        # 接管查询请求
        results = super(ExerciseAdmin, self).get_queryset(request)
        identity = request.user.identity()
        if request.user.is_superuser:  # 超级用户可查看所有数据
            return results
        if identity == 'teacher' or identity == 'teacher_student':
            rooms = request.user.teacher.teach_room()
            return models.Exercise.objects.filter(classroom__in = rooms).distinct()
        elif identity == 'student':
            return models.Exercise.objects.none()
        else:
            return models.Exercise.objects.none()
    def formfield_for_dbfield(self, field, **kwargs):
        login_user = kwargs['request'].user
        if not (login_user.is_superuser):
            if field.name == 'classroom':
                identity = login_user.identity()
                if identity == 'teacher' or identity == 'teacher_student':
                    #XXX(Seddon):这种URL截断的方法非常难看 暂时没找到好的方法
                    exer_id = kwargs['request'].path.split('/')[4]
                    units = Classroom.objects.filter(teacher=login_user.teacher)
                    other_class = models.Exercise.objects.get(exer_id=exer_id).classroom.all()
                    units = units | other_class
                    units = units.distinct()
                else:
                    units = Classroom.objects.none()
                return forms.ModelMultipleChoiceField (queryset=units,label="分配班级",help_text='按住 Ctrl 键(Mac 上的 Command 键) 来选择多个班级。如需多位老师多个班级同时练习，请使用管理员账号发布！')
        return super(ExerciseAdmin, self).formfield_for_dbfield(field, **kwargs)

    def classrooms(self,obj):
        return [bt.class_name for bt in obj.classroom.all()]
    classrooms.short_description = "分配班级"
    list_display = ['exer_id', 'exer_name', 'paper', 'publish_time', 'active', 'classrooms']


# Fields: 'rec_id', 'student', 'question', 'ans', 'ans_status', 'submit_time', 'submit_cnt'
@admin.register(models.QuesAnswerRec)
class QuesAnswerRecAdmin(admin.ModelAdmin):
    list_display = ['rec_id', 'user', 'question', 'ans', 'ans_status', 'submit_time', 'submit_cnt']


# Fields: 'rec_id', 'student', 'paper', 'start_time', 'end_time', 'score',
@admin.register(models.PaperAnswerRec)
class PaperAnswerRecAdmin(admin.ModelAdmin):
    # TODO:(Seddon) 源代码中限定学生无论如何都无法修改自己的试卷内容
    # 非admin权限控制
    # 双重保险！
    # 剩余 试卷公开字段、试卷作答、题库、题目、题目作答
    # 需要半天时间搞定与测试
    # 接下来阉割部分前端页面
    # 做图表
    # 做调度！
    def get_queryset(self, request):
        # 接管查询请求
        results = super(PaperAnswerRecAdmin, self).get_queryset(request)
        identity = request.user.identity()
        if request.user.is_superuser:  # 超级用户可查看所有数据
            return results
        if identity == 'teacher' or identity == 'teacher_student':
            students = request.user.teacher.teach_stu()
            return results.filter(student__in = students)
        elif identity == 'student':
            return results.filter(student = request.user.student)
        else:
            return results.none()
    list_display = ['rec_id', 'student', 'paper', 'start_time', 'end_time', 'score', ]
