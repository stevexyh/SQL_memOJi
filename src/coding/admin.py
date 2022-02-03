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
from user.models import Classroom ,Student, Teacher, User
from django import forms
# Register your models here.


# Fields: 'ques_id', 'ques_name', 'ques_set_id', 'ques_difficulty', 'ques_desc', 'ques_ans', 'initiator'
@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request,obj=None):
        if request.user.is_superuser:
            return True
        else:
            if obj:
                if obj.initiator == request.user.teacher:
                    return True
                else:
                    return False
        return False


    def has_change_permission(self, request,obj=None):
        if request.user.is_superuser:
            return True
        else:
            if obj:
                if obj.initiator == request.user.teacher:
                    return True
                else:
                    return False
        return False

    def get_readonly_fields(self,request,obj=None):
        if request.user.is_superuser:
            return []
        else:
            if obj:
                # 之后就不可编辑
                return ['initiator']
            else:
                return []

    def get_queryset(self, request):
        # 接管查询请求
        results = super(QuestionAdmin, self).get_queryset(request)
        identity = request.user.identity()
        if request.user.is_superuser:  # 超级用户可查看所有数据
            return results
        if identity == 'teacher' or identity == 'teacher_student':
            my_questions = models.Question.objects.filter(initiator = request.user.teacher)
            share_questions = models.Question.objects.filter(share = True)
            return (my_questions | share_questions).distinct()
        else:
            return models.Question.objects.none()

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if not (request.user.is_superuser):
            if db_field.name == 'initiator':
                identity = request.user.identity()
                if identity == 'teacher' or identity == 'teacher_student':
                    kwargs['queryset'] = Teacher.objects.filter(user=request.user)
                else:
                    kwargs['queryset'] = Teacher.objects.none()
            if db_field.name == 'ques_set':
                identity = request.user.identity()
                if identity == 'teacher' or identity == 'teacher_student':
                    kwargs['queryset'] = models.QuestionSet.objects.filter(initiator=request.user.teacher)
                else:
                    kwargs['queryset'] = models.QuestionSet.objects.none()
        return super(QuestionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    list_display = ['ques_id', 'ques_name', 'ques_set_id', 'ques_difficulty', 'ques_desc', 'ques_ans', 'initiator', 'share']


# Fields: 'ques_set_id', 'ques_set_name', 'ques_set_desc', 'create_sql', 'initiator'
@admin.register(models.QuestionSet)
class QuestionSetAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request,obj=None):
        if request.user.is_superuser:
            return True
        else:
            if obj:
                if obj.initiator == request.user.teacher:
                    return True
                else:
                    return False
        return False

    def has_change_permission(self, request,obj=None):
        if request.user.is_superuser:
            return True
        else:
            if obj:
                if obj.initiator == request.user.teacher:
                    return True
                else:
                    return False
        return False

    def get_readonly_fields(self,request,obj=None):
        if request.user.is_superuser:
            return ['db_name']
        else:
            if obj:
                # 之后就不可编辑
                return ['db_name','initiator']
            else:
                return []

    def get_queryset(self, request):
        # 接管查询请求
        results = super(QuestionSetAdmin, self).get_queryset(request)
        identity = request.user.identity()
        if request.user.is_superuser:  # 超级用户可查看所有数据
            return results
        if identity == 'teacher' or identity == 'teacher_student':
            my_set = models.QuestionSet.objects.filter(initiator = request.user.teacher)
            share_set = models.QuestionSet.objects.filter(share = True)
            return (my_set | share_set).distinct()
        else:
            return models.QuestionSet.objects.none()

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if not (request.user.is_superuser):
            if db_field.name == 'initiator':
                identity = request.user.identity()
                if identity == 'teacher' or identity == 'teacher_student':
                    kwargs['queryset'] = Teacher.objects.filter(user=request.user)
                else:
                    kwargs['queryset'] = Teacher.objects.none()
        return super(QuestionSetAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    list_display = ['ques_set_id', 'ques_set_name', 'ques_set_desc', 'db_name', 'create_sql', 'initiator', 'share']


# Fields: 'paper_id', 'paper_name', 'publish_time', 'paper_desc', 'initiator', 'question',
@admin.register(models.Paper)
class PaperAdmin(admin.ModelAdmin):
    class PaperQuestionInline(admin.TabularInline):
        model = models.PaperQuestion
    inlines = [
        PaperQuestionInline
    ]
    # class QuestionInline(admin.TabularInline):
    #     model = models.Paper.question.through


    # def has_add_permission(self, request,obj=None):
    #     return False
    
    def has_delete_permission(self, request,obj=None):
        if request.user.is_superuser:
            return True
        else:
            if obj:
                if obj.initiator == request.user.teacher:
                    return True
                else:
                    return False
        return False


    def has_change_permission(self, request,obj=None):
        if request.user.is_superuser:
            return True
        else:
            if obj:
                if obj.initiator == request.user.teacher:
                    return True
                else:
                    return False
        return False

    def get_readonly_fields(self,request,obj=None):
        if request.user.is_superuser:
            return []
        else:
            if obj:
                return ['initiator']
            else:
                return []

    def get_queryset(self, request):
        # 接管查询请求
        results = super(PaperAdmin, self).get_queryset(request)
        identity = request.user.identity()
        if request.user.is_superuser:  # 超级用户可查看所有数据
            return results
        if identity == 'teacher' or identity == 'teacher_student':
            #TODO:(Seddon)设置公开字段 也可以看公开的试卷
            my_paper = models.Paper.objects.filter(initiator = request.user.teacher)
            share_paper = models.Paper.objects.filter(share = True)
            return (my_paper | share_paper).distinct()
        else:
            return models.Paper.objects.none()

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if not (request.user.is_superuser):
            if db_field.name == 'initiator':
                identity = request.user.identity()
                if identity == 'teacher' or identity == 'teacher_student':
                    kwargs['queryset'] = Teacher.objects.filter(user=request.user)
                else:
                    kwargs['queryset'] = Teacher.objects.none()
        return super(PaperAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_dbfield(self, field, **kwargs):
        login_user = kwargs['request'].user
        if not (login_user.is_superuser):
            if field.name == 'question':
                identity = login_user.identity()
                if identity == 'teacher' or identity == 'teacher_student':
                    paper_id = kwargs['request'].path.split('/')[4]
                    units = models.Question.objects.filter(initiator=login_user.teacher)
                    if paper_id.isdigit():
                        other_question = models.Paper.objects.get(paper_id=paper_id).question.all()
                        share_question = models.Question.objects.filter(share=True)
                        units = units | other_question
                        units = units | share_question
                        units = units.distinct()
                    else:
                        share_question = models.Question.objects.filter(share=True)
                        units = units | share_question
                        units = units.distinct()
                else:
                    units = models.Question.objects.none()
                return forms.ModelMultipleChoiceField (queryset=units,label="题目列表",help_text='按住 Ctrl 键(Mac 上的 Command 键) 来选择多个题目。如需添加其他教师的题目，请联系相关老师公开或使用管理员账号发布！')
        return super(PaperAdmin,self).formfield_for_dbfield(field, **kwargs)

    # def get_readonly_fields(self,request,obj=None):
    #     if request.user.is_superuser:
    #         return []
    #     else:
    #         if obj:
    #             # 之后就不可编辑
    #             return ['student', 'paper']
    #         else:
    #             return ['initiator']
    list_display = [
        'paper_id', 'paper_name', 'paper_desc', 'initiator', 'publish_time', 'share'
    ]

    # inlines = [QuestionInline]


# Fields: 'exam_id', 'exam_name', 'paper', 'start_time', 'end_time', 'publish_time', 'active', 'classroom'
@admin.register(models.Exam)
class ExamAdmin(admin.ModelAdmin):

    # class ClassroomInline(admin.TabularInline):
    #     model = models.Exam.classroom.through

    # inlines = [ClassroomInline]
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if not (request.user.is_superuser):
            identity = request.user.identity()
            if db_field.name == 'paper':
                if identity == 'teacher' or identity == 'teacher_student':
                    use_paper = models.Paper.objects.filter(initiator=request.user.teacher) | models.Paper.objects.filter(share=True)
                    kwargs['queryset'] = use_paper.distinct()
                else:
                    kwargs['queryset'] = models.Paper.objects.none()
        return super(ExamAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

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
                    if exam_id.isdigit():
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
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if not (request.user.is_superuser):
            identity = request.user.identity()
            if db_field.name == 'paper':
                if identity == 'teacher' or identity == 'teacher_student':
                    use_paper = models.Paper.objects.filter(initiator=request.user.teacher) | models.Paper.objects.filter(share=True)
                    kwargs['queryset'] = use_paper.distinct()
                else:
                    kwargs['queryset'] = models.Paper.objects.none()
        return super(ExerciseAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


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
                    if exer_id.isdigit():
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
    # list_filter = ['question']
    def has_delete_permission(self, request,obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_change_permission(self, request,obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if not (request.user.is_superuser):
            identity = request.user.identity()
            # print(identity)
            if db_field.name == 'user':
                if identity == 'teacher' or identity == 'teacher_student':
                    students = request.user.teacher.teach_stu()
                    query_stu = User.objects.filter(email__in=students)
                    kwargs['queryset'] = query_stu
                else:
                    kwargs['queryset'] = Student.objects.none()
            if db_field.name == 'question':
                if identity == 'teacher' or identity == 'teacher_student':
                    use_questions = models.Question.objects.filter(initiator=request.user.teacher) | models.Question.objects.filter(share=True)
                    kwargs['queryset'] = use_questions.distinct()
                else:
                    kwargs['queryset'] = models.Question.objects.none()
        return super(QuesAnswerRecAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        # 接管查询请求
        results = super(QuesAnswerRecAdmin, self).get_queryset(request)
        identity = request.user.identity()
        if request.user.is_superuser:  # 超级用户可查看所有数据
            return results
        if identity == 'teacher' or identity == 'teacher_student':
            students = request.user.teacher.teach_stu()
            query_stu = User.objects.filter(email__in=students)
            # return results.filter(email__in = students.user)
            return results.filter(user__in = query_stu)
        elif identity == 'student':
            return results.filter(user = request.user)
        else:
            return results.none()
    list_display = ['rec_id', 'user', 'question', 'ans', 'ans_status', 'submit_time', 'submit_cnt']

# Fields: 'rec_id', 'student', 'paper', 'start_time', 'end_time', 'score',
@admin.register(models.PaperAnswerRec)
class PaperAnswerRecAdmin(admin.ModelAdmin):
    # TODO:(Seddon) 源代码中限定学生无论如何都无法修改自己的试卷内容
    # 接下来阉割部分前端页面
    # 做图表
    # 做调度！
    def has_delete_permission(self, request,obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_change_permission(self, request,obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

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

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if not (request.user.is_superuser):
            identity = request.user.identity()
            # print(identity)
            if db_field.name == 'student':
                if identity == 'teacher' or identity == 'teacher_student':
                    kwargs['queryset'] = request.user.teacher.teach_stu()
                    print(request.user.teacher.teach_stu())
                else:
                    kwargs['queryset'] = Student.objects.none()
            if db_field.name == 'paper':
                if identity == 'teacher' or identity == 'teacher_student':
                    use_paper = models.Paper.objects.filter(initiator=request.user.teacher) | models.Paper.objects.filter(share=True)
                    kwargs['queryset'] = use_paper.distinct()
                else:
                    kwargs['queryset'] = models.Paper.objects.none()
        return super(PaperAnswerRecAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


    def get_readonly_fields(self,request,obj=None):
        if request.user.is_superuser:
            return []
        else:
            if obj:
                # 之后就不可编辑
                return ['student', 'paper']
            else:
                return []
    list_display = ['rec_id', 'student', 'paper', 'start_time', 'end_time', 'score', 'paper_class']

@admin.register(models.ExamAnswerRec)
class ExamAnswerRecAdmin(admin.ModelAdmin):
    # def has_delete_permission(self, request,obj=None):
    #     if request.user.is_superuser:
    #         return True
    #     else:
    #         return False

    # def has_change_permission(self, request,obj=None):
    #     if request.user.is_superuser:
    #         return True
    #     else:
    #         return False

    # def get_queryset(self, request):
    #     # 接管查询请求
    #     results = super(PaperAnswerRecAdmin, self).get_queryset(request)
    #     identity = request.user.identity()
    #     if request.user.is_superuser:  # 超级用户可查看所有数据
    #         return results
    #     if identity == 'teacher' or identity == 'teacher_student':
    #         students = request.user.teacher.teach_stu()
    #         return results.filter(student__in = students)
    #     elif identity == 'student':
    #         return results.filter(student = request.user.student)
    #     else:
    #         return results.none()

    # def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
    #     if not (request.user.is_superuser):
    #         identity = request.user.identity()
    #         # print(identity)
    #         if db_field.name == 'student':
    #             if identity == 'teacher' or identity == 'teacher_student':
    #                 kwargs['queryset'] = request.user.teacher.teach_stu()
    #                 print(request.user.teacher.teach_stu())
    #             else:
    #                 kwargs['queryset'] = Student.objects.none()
    #         if db_field.name == 'paper':
    #             if identity == 'teacher' or identity == 'teacher_student':
    #                 use_paper = models.Paper.objects.filter(initiator=request.user.teacher) | models.Paper.objects.filter(share=True)
    #                 kwargs['queryset'] = use_paper.distinct()
    #             else:
    #                 kwargs['queryset'] = models.Paper.objects.none()
    #     return super(PaperAnswerRecAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


    # def get_readonly_fields(self,request,obj=None):
    #     if request.user.is_superuser:
    #         return []
    #     else:
    #         if obj:
    #             # 之后就不可编辑
    #             return ['student', 'paper']
    #         else:
    #             return []
    list_display = ['rec_id', 'student', 'exam', 'start_time', 'end_time', 'score']


@admin.register(models.ExerAnswerRec)
class ExerAnswerRecAdmin(admin.ModelAdmin):
    # def has_delete_permission(self, request,obj=None):
    #     if request.user.is_superuser:
    #         return True
    #     else:
    #         return False

    # def has_change_permission(self, request,obj=None):
    #     if request.user.is_superuser:
    #         return True
    #     else:
    #         return False

    # def get_queryset(self, request):
    #     # 接管查询请求
    #     results = super(PaperAnswerRecAdmin, self).get_queryset(request)
    #     identity = request.user.identity()
    #     if request.user.is_superuser:  # 超级用户可查看所有数据
    #         return results
    #     if identity == 'teacher' or identity == 'teacher_student':
    #         students = request.user.teacher.teach_stu()
    #         return results.filter(student__in = students)
    #     elif identity == 'student':
    #         return results.filter(student = request.user.student)
    #     else:
    #         return results.none()

    # def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
    #     if not (request.user.is_superuser):
    #         identity = request.user.identity()
    #         # print(identity)
    #         if db_field.name == 'student':
    #             if identity == 'teacher' or identity == 'teacher_student':
    #                 kwargs['queryset'] = request.user.teacher.teach_stu()
    #                 print(request.user.teacher.teach_stu())
    #             else:
    #                 kwargs['queryset'] = Student.objects.none()
    #         if db_field.name == 'paper':
    #             if identity == 'teacher' or identity == 'teacher_student':
    #                 use_paper = models.Paper.objects.filter(initiator=request.user.teacher) | models.Paper.objects.filter(share=True)
    #                 kwargs['queryset'] = use_paper.distinct()
    #             else:
    #                 kwargs['queryset'] = models.Paper.objects.none()
    #     return super(PaperAnswerRecAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


    # def get_readonly_fields(self,request,obj=None):
    #     if request.user.is_superuser:
    #         return []
    #     else:
    #         if obj:
    #             # 之后就不可编辑
    #             return ['student', 'paper']
    #         else:
    #             return []
    list_display = ['rec_id', 'student', 'exer', 'start_time', 'end_time', 'score']