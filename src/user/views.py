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


from django.shortcuts import render, redirect
from django.views import View
from django.contrib import auth
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.db.models import Sum
from user.models import Student, User, Classroom
from user.forms import UserInfoForm, StudentForm, ClassroomForm
from coding.models import Exam, Exercise, QuesAnswerRec, Question, QuestionSet, ExerAnswerRec, ExamAnswerRec, ExamQuesAnswerRec, ExerQuesAnswerRec
import datetime
from django.utils import timezone
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseForbidden
import json
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
    # print("在首页")
    if request.user.is_authenticated:
        if request.user.is_superuser:
            content = {
                'err_code': '403',
                'err_message': _('没有权限,请开通学生身份'),
            }
            return render(request, 'error.html', context=content)
        else:
            identity = request.user.identity()
            if identity == 'student' or identity == 'teacher_student':
                exam_result = request.user.student.classroom.exam_set.all()
                exer_result = request.user.student.classroom.exercise_set.all()
                exam_cnt = exam_result.count()
                exam_active = exam_result.filter(active=True).count()
                exer_cnt = exer_result.count()
                exer_active = exer_result.filter(active=True).count()
                answer_query_exer = ExerQuesAnswerRec.objects.filter(user=request.user)
                answer_query_exam = ExamQuesAnswerRec.objects.filter(user=request.user)
                submit_cnt = 0
                if answer_query_exer.aggregate(Sum('submit_cnt'))['submit_cnt__sum'] is not None:
                    submit_cnt += answer_query_exer.aggregate(Sum('submit_cnt'))['submit_cnt__sum'] 
                if answer_query_exam.aggregate(Sum('submit_cnt'))['submit_cnt__sum'] is not None:
                    submit_cnt += answer_query_exam.aggregate(Sum('submit_cnt'))['submit_cnt__sum'] 
                question_list = Question.objects.filter(ques_id__in=answer_query_exam.values('question')) | Question.objects.filter(ques_id__in=answer_query_exer.values('question'))
                question_rec = question_list.distinct()
                ques_easy = question_rec.filter(ques_difficulty=0).count()
                ques_middle = question_rec.filter(ques_difficulty=1).count()
                ques_difficult = question_rec.filter(ques_difficulty=2).count()
                ques_cnt = question_rec.count()
                ac_cnt = answer_query_exer.filter(ans_status=0).count() + answer_query_exam.filter(ans_status=0).count()
                # FIXME(Seddon):实际上是七日内提交
                monday = timezone.now() - datetime.timedelta(days=7)
                mouth = timezone.now() - datetime.timedelta(days=30)    
                week_submit = answer_query_exer.filter(submit_time__gte=monday).count() + answer_query_exam.filter(submit_time__gte=monday).count()
                mouth_submit = answer_query_exer.filter(submit_time__gte=mouth).count() + answer_query_exam.filter(submit_time__gte=mouth).count()
                exam_cont = ExamAnswerRec.objects.filter(student=request.user.student, status=True).count()
                exam_labels_query = ExamAnswerRec.objects.filter(student=request.user.student, status=True)
                exam_labels = []
                exam_data = []
                for label in exam_labels_query:
                    exam_labels.append(str(label.exam.exam_id) + '-' + label.exam.exam_name)
                    exam_data.append(label.score)
                exer_cont = ExerAnswerRec.objects.filter(student=request.user.student, status=True).count()
                exer_labels_query = ExerAnswerRec.objects.filter(student=request.user.student, status=True)
                exer_labels = []
                exer_data = []
                for label in exer_labels_query:
                    exer_labels.append(str(label.exer.exer_id) + '-' + label.exer.exer_name)
                    exer_data.append(label.score)
                content = {
                    'exam_cnt': exam_cnt,
                    'exam_active': exam_active,
                    'exer_cnt': exer_cnt,
                    'exer_active': exer_active,
                    'submit_cnt': submit_cnt,
                    'ques_easy':ques_easy,
                    'ques_middle':ques_middle,
                    'ques_difficult':ques_difficult,
                    'ques_cnt':ques_cnt,
                    'ac_cnt':ac_cnt,
                    'week_submit':week_submit,
                    'mouth_submit':mouth_submit,
                    'exam_cont':exam_cont,
                    'exam_labels':exam_labels,
                    'exam_data':exam_data,
                    'exer_cont':exer_cont,
                    'exer_labels':exer_labels,
                    'exer_data':exer_data,
                    'exam_info':exam_labels_query,
                    'exer_info':exer_labels_query
                }
                return render(request, 'index.html', context=content)
    content = {
        'err_code': '403',
        'err_message': _('没有权限,请开通学生身份'),
    }
    return render(request, 'error.html', context=content)

def e404(request, exception=None):
    '''Render 404 err page'''

    content = {
        'err_code': '404',
        'err_message': _('页面不存在'),
    }

    return render(request, 'error.html', context=content)


def e500(request):
    '''Render 500 err page'''

    content = {
        'err_code': '500',
        'err_message': _('服务器错误'),
    }

    return render(request, 'error.html', context=content)
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
        fail = True
        if User.objects.filter(username=username):
            msg = _('此用户名已存在, 请更换另一个或求助管理员')
        elif User.objects.filter(email=email):
            msg = _('此邮箱已注册, 请更换另一个或求助管理员')
        elif User.objects.filter(internal_id=internal_id):
            msg = _('此学工号已注册, 请更换另一个或求助管理员')
        elif password1 != password2:
            msg = _('两次密码输入不一致')
        else:
            try:
                with transaction.atomic():
                    new_user = User.objects.create_user(username=username, password=password2, email=email)
                    new_user.school_name = school_name
                    new_user.class_id = class_id
                    new_user.full_name = full_name
                    new_user.internal_id = internal_id
                    new_user.priority = User.UserType.STUDENT

                    user_student = Student.objects.create(user=new_user)
                    user_student.save()
                    new_user.save()
                    fail = False
            except Exception as exc:
                msg = _('注册异常: ') + str(exc)
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
class ClassManage(View):
    '''Render class-manage template'''
    def get(self, request):
        key = request.user.is_authenticated & request.user.is_superuser
        print(request.user.is_authenticated)
        if request.user.is_authenticated == False:
            content = {
                'err_code': '403',
                'err_message': _('没有权限'),
            }
            return render(request, 'error.html', context=content)
        else:
            identity = request.user.identity()
            if request.user.is_superuser or identity =='teacher' or identity == 'teacher_student':
                # XXX(Seddon Shen): 使用反向查询_set()去找学生 需注意全部字段小写
                if request.user.is_superuser:
                    class_list = Classroom.objects.all()
                else:
                    class_list = Classroom.objects.filter(teacher=request.user.teacher)

                content = {
                    'class_list': class_list,
                }
                return render(request, 'user/class-manage.html', context=content)
            else:
                content = {
                    'err_code': '403',
                    'err_message': _('没有权限'),
                }
                return render(request, 'error.html', context=content)


class ClassDetails(View):
    '''Render class-details template'''

    def get(self, request, class_id):
        if request.user.is_authenticated:
            classroom = Classroom.objects.get(class_id=class_id)
            exam_list = classroom.exam_set.all()
            exer_list = classroom.exercise_set.all()
            # print(classroom.exam_set.all())
            # print(classroom.exercise_set.all())
            # print(classroom.student_set.all())
            # for student in classroom.student_set.all():
            #     print(student.examanswerrec_set.all())
            # print(ExamAnswerRec.objects.filter(student__in=classroom.student_set.all()))
            exam_detail = ExamAnswerRec.objects.filter(student__in=classroom.student_set.all())
            exer_detail = ExerAnswerRec.objects.filter(student__in=classroom.student_set.all())
            for exam in exam_list:
                exam_answer_detail = ExamQuesAnswerRec.objects.filter(exam__in=exam_detail.filter(exam=exam))
                exam_infoset = exam_detail.filter(exam=exam)
                exam.start_cnt=exam_infoset.count()
                exam.finish_cnt=exam_infoset.filter(status=True).count()
                if classroom.student_set.count() == 0:
                    exam.per_finish_rate = 0
                else:
                    per_finish_rate = (exam.finish_cnt / classroom.student_set.count()) * 100
                    exam.per_finish_rate = round(per_finish_rate,2)

                if exam_answer_detail.count() == 0:
                    exam.per_acrate = 0
                else:
                    per_acrate = (exam_answer_detail.filter(ans_status=0).count() / exam_answer_detail.count()) * 100
                    exam.per_acrate = round(per_acrate,2)
            for exer in exer_list:
                exer_answer_detail = ExerQuesAnswerRec.objects.filter(exer__in=exer_detail.filter(exer=exer))
                exer_infoset = exer_detail.filter(exer=exer)
                exer.start_cnt=exer_infoset.count()
                exer.finish_cnt=exer_infoset.filter(status=True).count()
                if classroom.student_set.count() == 0:
                    exer.per_finish_rate = 0
                else:
                    per_finish_rate = (exer.finish_cnt / classroom.student_set.count()) * 100
                    exer.per_finish_rate = round(per_finish_rate,2)

                if exer_answer_detail.count() == 0:
                    exer.per_acrate = 0
                else:
                    per_acrate = (exer_answer_detail.filter(ans_status=0).count() / exer_answer_detail.count()) * 100
                    exer.per_acrate = round(per_acrate,2)

            if request.user.is_superuser:
                content = {
                    'classroom': classroom,
                    'exam_list' : exam_list,
                    'exer_list' : exer_list
                }
                return render(request, 'user/class-details.html', context=content)
            else:
                if request.user.identity() == 'teacher_student' or request.user.identity() == 'teacher':
                    if request.user.teacher == classroom.teacher:
                        content = {
                            'classroom' : classroom,
                            'exam_list' : exam_list,
                            'exer_list' : exer_list
                        }
                    return render(request, 'user/class-details.html', context=content)
        content = {
            'err_code': '403',
            'err_message': _('没有权限'),
        }
        return render(request, 'error.html', context=content)

class UserInfo(View):
    '''Render user-info template'''

    RBF = '# TODO(Steve X): REMOVE BEFORE FLIGHT'

    def get(self, request):
        not_login = _('未登录')
        null = 'NULL'
        user = request.user
        is_student = user.is_authenticated and user.priority == User.UserType.STUDENT
        full_name = user.full_name if user.is_authenticated else not_login
        username = user.username if user.is_authenticated else not_login
        email = user.email if user.is_authenticated else not_login
        school = user.school if user.is_authenticated else not_login
        college_name = user.college_name if user.is_authenticated else not_login
        internal_id = user.internal_id if user.is_authenticated else not_login
        classroom = user.student.classroom if is_student else False
        priority = user.get_priority_display() if user.is_authenticated else not_login
        join_status = user.is_authenticated and user.join_status != User.JoinStatus.OUT_OF_LIST or user.is_superuser
        info_form = UserInfoForm(instance=user) if user.is_authenticated else None
        student_form = StudentForm(instance=user.student) if is_student else None

        content = {
            'full_name': full_name,
            'username': username,
            'email': email,
            'school': school,
            'college_name': college_name,
            'internal_id': internal_id,
            'classroom': classroom,
            'priority': priority,
            'join_status': join_status,
            'join_status_display': _('认证') if join_status else _('未认证'),
            'join_status_color': 'success' if join_status else 'warning',
            'info_form': info_form,
            'student_form': student_form,
        }

        # print(content)
        for k in content:
            content[k] = content[k] if content[k] != '' else f'{k}: {null}'

        return render(request, 'user/user-info.html', context=content)

    # FIXME(Steve X): can't edit email, switch primary key to uuid
    def post(self, request):
        user = request.user
        is_student = user.is_authenticated and user.priority == User.UserType.STUDENT

        info_form = UserInfoForm(request.POST, instance=user) if user.is_authenticated else None
        student_form = StudentForm(request.POST, instance=user.student) if is_student else None

        if info_form and info_form.is_valid():
            info_form.save()

        if student_form and student_form.is_valid():
            student_form.save()

        return redirect('/user-info')


class ClassEventDetails(View):
    '''Render class-event-details template'''
    def get(self, request, class_id, event_type,event_id):
        if request.user.is_authenticated:
            classroom = Classroom.objects.get(class_id=class_id)
            if event_type == 'exam':
                event = Exam.objects.get(exam_id=event_id)
                event_detail = ExamAnswerRec.objects.filter(exam=event,student__in=classroom.student_set.all())
                event_answer_detail = ExamQuesAnswerRec.objects.filter(exam__in=event_detail)
            elif event_type == 'exer':
                event = Exercise.objects.get(exer_id=event_id)
                event_detail = ExerAnswerRec.objects.filter(student__in=classroom.student_set.all(),exer=event)
                event_answer_detail = ExerQuesAnswerRec.objects.filter(exer__in=event_detail)
            else:
                event = Exam.objects.none()
                event_detail = ExamAnswerRec.objects.none()
                event_answer_detail = ExamAnswerRec.objects.none()
            questions = event.paper.question.all()
            questions_cnt = questions.count()
            for question in questions:
                question_answer_detail = event_answer_detail.filter(question=question)
                question.finish_cnt = question_answer_detail.count()
                if classroom.student_set.count() == 0:
                    question.per_finish_rate = 0
                else:
                    per_finish_rate = (question.finish_cnt / classroom.student_set.count()) * 100
                    question.per_finish_rate = round(per_finish_rate,2)
                if question.finish_cnt == 0:
                    question.per_acrate = 0
                else:
                    per_acrate = (question_answer_detail.filter(ans_status=0).count() / question.finish_cnt) * 100
                    question.per_acrate = round(per_acrate,2)
            unfinished = classroom.student_set.exclude(user__in=event_answer_detail.values('user'))
            for student in unfinished:
                finish_cnt = event_answer_detail.filter(user=student.user)
                student.unfinished_list = questions.exclude(ques_id__in=finish_cnt.values('question'))
                finish_cnt = finish_cnt.count()
                student.unfinish_cnt = questions_cnt - finish_cnt
            error_list = event_answer_detail.exclude(ans_status=0)
            error = classroom.student_set.filter(user__in=error_list.values('user'))
            for student in error:
                student.error_cnt = error_list.filter(user=student.user).count()
                student.error_list = error_list.filter(user=student.user).values('question')
                student.error_list = questions.filter(ques_id__in=student.error_list)
            if request.user.is_superuser:
                content = {
                    'classroom': classroom,
                    'questions' : questions,
                    'student_unfinish' : unfinished,
                    'student_error' : error,
                }
                return render(request, 'user/class-event-details.html', context=content)
            else:
                if request.user.identity() == 'teacher_student' or request.user.identity() == 'teacher':
                    if request.user.teacher == classroom.teacher:
                        content = {
                            'classroom' : classroom,
                            'questions' : questions,
                            'student_unfinish' : unfinished,
                            'student_error' : error,
                        }
                    return render(request, 'user/class-event-details.html', context=content)
        content = {
            'err_code': '403',
            'err_message': _('没有权限'),
        }
        return render(request, 'error.html', context=content)

#--------------------------------------------END---------------------------------------------#
