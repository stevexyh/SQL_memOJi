#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
----------------------------------------------------------------------------------------------------
* Project Name : SQL_memOJi
* File Name    : views.py
* Description  : 
* Create Time  : 2021-04-04 00:46:48
* Version      : 1.0
* Author       : Steve X
* GitHub       : https://github.com/Steve-Xyh/SQL_memOJi
----------------------------------------------------------------------------------------------------
* Notice
- 
- 
----------------------------------------------------------------------------------------------------
'''


import pymysql,datetime
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect  
from django.urls import Resolver404, reverse
from django.views import View
from django.contrib import auth
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.db.models import Sum
from prettytable import PrettyTable
from coding import forms
from coding import models
from utils import token as tk
from utils import sql_check
from django.db.models import Q
from django.utils import timezone
from django.db.models import Avg
from .tasks import sql_check_celery
# Create your views here.


def exams_manage(request):
    '''Render exams-manage template'''

    exam_form = forms.ExamForm(auto_id='id_exam_%s')
    exer_form = forms.ExerciseForm(auto_id='id_exer_%s')

    exams_list = models.Exam.objects.order_by('publish_time')
    exer_list = models.Exercise.objects.order_by('publish_time')
    next_exam = exams_list.first()

    content = {
        'exam_form': exam_form,
        'exer_form': exer_form,
        'exams_list': exams_list,
        'exer_list': exer_list,
        'next_exam': next_exam,
    }

    return render(request, 'coding/exams-manage.html', context=content)


def exam_add(request):
    '''Add exams in exams-manage page'''

    exam_form = forms.ExamForm(request.POST)

    if exam_form.is_valid():
        exam_form.save()

    return redirect('coding:exams-manage')


def exer_add(request):
    '''Add exercises in exams-manage page'''

    exer_form = forms.ExerciseForm(request.POST)

    if exer_form.is_valid():
        exer_form.save()

    return redirect('coding:exams-manage')

#------------------------------------Questions Manage Page-----------------------------------#


def questions_manage_base(request):
    '''Render questions-manage-base template'''

    ques_set_form = forms.QuesSetForm(auto_id='id_qset_%s')
    question_form = forms.QuestionForm(auto_id='id_ques_%s')
    paper_form = forms.PaperForm(auto_id='id_paper_%s')

    question_list = models.Question.objects.all()
    ques_set_list = models.QuestionSet.objects.all()
    paper_list = models.Paper.objects.all()

    content = {
        'ques_set_form': ques_set_form,
        'question_form': question_form,
        'paper_form': paper_form,
        'question_list': question_list,
        'ques_set_list': ques_set_list,
        'paper_list': paper_list,
    }

    return render(request, 'coding/questions-manage-base.html', context=content)
# XXX(Seddon Shen):need to modify the user control logic more
def questions_manage(request):
    '''Render questions-manage template'''

    ques_set_form = forms.QuesSetForm(auto_id='id_qset_%s')
    question_form = forms.QuestionForm(auto_id='id_ques_%s')
    paper_form = forms.PaperForm(auto_id='id_paper_%s')
    question_list = models.Question.objects.filter(initiator_id=request.user.email)
    ques_set_list = models.QuestionSet.objects.filter(initiator_id=request.user.email)
    paper_list = models.Paper.objects.filter(initiator_id=request.user.email)

    questions_cnt = models.Question.objects.filter(initiator_id=request.user.email).count()
    # print(questions_cnt)
    # print(question_list.values())



    content = {
        'ques_set_form': ques_set_form,
        'question_form': question_form,
        'paper_form': paper_form,
        'question_list': question_list,
        'ques_set_list': ques_set_list,
        'paper_list': paper_list,
        'questions_cnt': questions_cnt
    }

    return render(request, 'coding/questions-manage.html', context=content)


# XXX(Steve X): database grants for teachers
def ques_set_add(request):
    '''Add question set in questions-manage page'''

    ques_set_form = forms.QuesSetForm(request.POST)
    host = tk.get_conf('mysql', 'host')
    port = int(tk.get_conf('mysql', 'port'))
    user = tk.get_conf('mysql', 'user')
    passwd = tk.get_conf('mysql', 'password')

    db = pymysql.Connect(host=host, port=port, user=user, passwd=passwd)
    cur = db.cursor()
    qset_db_name = f'qset_{request.POST.get("db_name")}'
    create_sql = request.POST.get('create_sql').replace('\n', '').replace('\\n', '')
    create_sql_list = create_sql.split(';')

    # print(create_sql)
    # print(type(create_sql))
    # print('-'*40)
    # print(create_sql_list)

    try:
        cur.execute(f"""create database {qset_db_name};""")
        cur.execute(f"""use {qset_db_name};""")

        for sql in create_sql_list:
            cur.execute(sql)

        db.commit()
        if ques_set_form.is_valid():
            ques_set_form.save()

        # FIXME(Steve X): db_name 重名问题
        qset = models.QuestionSet.objects.get(db_name=ques_set_form.cleaned_data.get('db_name'))
        qset.db_name = qset_db_name
        qset.save()
    except Exception as exc:
        cur.execute(f"""drop database if exists {qset_db_name}""")
        db.rollback()
        print(exc)

    cur.close()
    db.close()

    return redirect('coding:questions-manage')


def question_add(request):
    '''Add question in questions-manage page'''

    question_form = forms.QuestionForm(request.POST)

    if question_form.is_valid():
        question_form.save()

    return redirect('coding:questions-manage')


# FIXME(Steve X): date time picker
def paper_add(request):
    '''Add paper in questions-manage page'''

    paper_form = forms.PaperForm(request.POST)

    if paper_form.is_valid():
        paper_form.save()
    else:
        print(paper_form.errors)

    return redirect('coding:questions-manage')
#--------------------------------------------END---------------------------------------------#


def coding(request):
    '''Render coding template'''
    conditions = {
        'classroom' : request.user.student.classroom,
        'active' : True
    }
    exams_list = models.Exam.objects.order_by('publish_time').filter(**conditions)
    exer_list = models.Exercise.objects.order_by('publish_time').filter(**conditions)
    have_finished = models.ExamAnswerRec.objects.filter(student=request.user.student,status = True)
    have_finished_exam_id = []
    for element in have_finished:
        have_finished_exam_id.append(element.exam.exam_id)
    unfinished = exams_list.exclude(exam_id__in=have_finished_exam_id)
    have_finished = models.Exam.objects.order_by('publish_time').filter(exam_id__in=have_finished_exam_id)
    next_exam = unfinished.first()
    content = {
        'exams_list': unfinished,
        'finished' : have_finished,
        'exer_list': exer_list,
        'next_exam': next_exam,
    }

    return render(request, 'coding/coding.html', context=content)


class CodingEditor(View):
    '''Render coding-editor template'''
    # 今天读了一下审题逻辑 Seddon 2021/12/30
    def get_info(self, request, event_type, event_id, ques_id):
        # print("test----------",event_type)
        try:
            question = models.Question.objects.get(ques_id=ques_id)
            qset = question.ques_set
            if event_type == 'exam':
                # print("Exam")
                event = models.Exam.objects.get(exam_id=event_id)
                event_name = event.exam_name
                # print("Event_name:",event_name)
            else:
                # print("Exercise")
                event = models.Exercise.objects.get(exer_id=event_id)
                event_name = event.exer_name
            # print("Question:",question,"Qset:",qset)
        except Exception as exc:
            print(exc)
            raise Resolver404
        # Previous & next question id
        prev_question = event.paper.question.filter(ques_id__lt=ques_id).order_by('-ques_id').first()
        next_question = event.paper.question.filter(ques_id__gt=ques_id).order_by('ques_id').first()
        now_paperquestion = models.PaperQuestion.objects.get(Q(question=question) & Q(paper=event.paper))
        host = tk.get_conf('mysql', 'host')
        port = int(tk.get_conf('mysql', 'port'))
        user = tk.get_conf('mysql', 'user')
        passwd = tk.get_conf('mysql', 'password')
        print(host,port,user,passwd)
        db = pymysql.Connect(host=host, port=port, user=user, passwd=passwd)
        cur = db.cursor()
        # print(db.__dict__)
        # print(cur.__dict__)
        # Create PrettyTable for `show tables;`
        pt_db_tables = PrettyTable(['Tables in this database'])
        pt_db_tables.align = 'l'
        cur.execute(f'''use qset_{qset.db_name};''')
        print("use qset_",qset.db_name)
        cur.execute(f'''show tables;''')
        tables = [tb[0] for tb in cur.fetchall()]
        pt_db_tables.add_rows([[tb] for tb in tables])
        # Create PrettyTable for `desc <table_name>;`
        tables_desc = [str(pt_db_tables)]
        for tb in tables:
            cur.execute(f'''desc {tb};''')
            pt_table_desc = PrettyTable(['Field', 'Type'])
            pt_table_desc.align = 'l'
            pt_table_desc.add_rows([row[:2] for row in cur.fetchall()])
            tables_desc.append('\n' + tb)
            tables_desc.append(str(pt_table_desc))
        db_desc = '\n'.join(tables_desc)
        cur.close()
        db.close()
        content = {
            'event': event,
            'event_id': event_id,
            'event_type': event_type,
            'event_name': event_name,
            'question': question,
            'paperquestion':now_paperquestion,
            'db_desc': db_desc,
            'prev_question': prev_question if prev_question else None,
            'next_question': next_question if next_question else None,
        }
        # 判断一下是否是用户首次做这个题 去查表
        cur_user = request.user
        if cur_user.is_authenticated:
            if event_type == 'exam':
                exam = models.Exam.objects.get(pk=event_id)    
                examrec = models.ExamAnswerRec.objects.filter(student=cur_user.student, exam=exam).first()
                rec = models.ExamQuesAnswerRec.objects.filter(user=cur_user, question=question, exam=examrec).first()
            elif event_type == 'exer':
                exer = models.Exercise.objects.get(pk=event_id)
                exerrec = models.ExerAnswerRec.objects.filter(student=cur_user.student, exer=exer).first()
                rec = models.ExerQuesAnswerRec.objects.filter(user=cur_user, question=question, exer=exerrec).first()
            else:
                raise Resolver404
            if rec:
                correct = rec.ans_status
                if correct == 0 :
                    correct_bool = True
                elif correct == 1:
                    correct_bool = False
                elif correct == 2:
                    correct_bool = 'error'
                else:
                    correct_bool = 'pending'
                ans_status_color = {
                    True: 'success',
                    False: 'danger',
                    'error': 'warning',
                    'pending': 'warning',
                }.get(correct_bool)
                content.update({
                    'correct': correct_bool,
                    'ans_status_color': ans_status_color,
                    'submit_ans': rec.ans,
                })
        return content

    def get(self, request, event_type, event_id, ques_id):
        '''Show info'''
        # try:
        #     if event_type == 'exam':
        #         print(request.user.student.classroom.exam_set.all().get(exam_id=event_id))
        #     elif event_type == 'exer':
        #         print(request.user.student.classroom.exercise_set.all().get(exer_id=event_id))
        #     else:
        #         raise Resolver404
        # except:
        #     raise Resolver404
        print("Debuging......")
        cur_user = request.user
        if event_type == 'exam':
            try:
               cur_user.student.classroom.exam_set.get(pk = event_id) 
            except Exception as exc:
                content = {
                    'err_code': '403',
                    'err_message': _('没有权限'),
                }
                return render(request, 'error.html', context=content)   
            exam = models.Exam.objects.get(pk=event_id)
            rec = models.ExamAnswerRec.objects.filter(student=cur_user.student, exam=exam).first()
            if exam.end_time < timezone.now():
                content = {
                    'err_code': '403',
                    'err_message': _('已截止'),
                }
                return render(request, 'error.html', context=content)
            if rec is not  None:
                if rec.status == True:
                    content = {
                        'err_code': '403',
                        'err_message': _('已交卷，无法查看'),
                    }
                    return render(request, 'error.html', context=content)
        elif event_type == 'exer':
            try:
               cur_user.student.classroom.exercise_set.get(pk = event_id) 
            except Exception as exc:
                content = {
                    'err_code': '403',
                    'err_message': _('没有权限'),
                }
                return render(request, 'error.html', context=content)   
            exer = models.Exercise.objects.get(pk=event_id)
            rec = models.ExerAnswerRec.objects.filter(student=cur_user.student, exer=exer).first()
            if exer.end_time < timezone.now():
                content = {
                    'err_code': '403',
                    'err_message': _('已截止'),
                }
                return render(request, 'error.html', context=content)
        else:
            raise Resolver404
        content = self.get_info(request, event_type, event_id, ques_id)
        if event_type == 'exam':
            first_ques_id = exam.first_ques
        else:
            first_ques_id = exer.first_ques
        if int(ques_id) == int(first_ques_id):
            if cur_user.is_authenticated:
                if event_type == 'exam':
                    # print('是考试')
                    # exam = models.Exam.objects.get(pk=event_id)
                    # rec = models.ExamAnswerRec.objects.filter(student=cur_user.student, exam=exam).first()
                    if rec is None:
                        models.ExamAnswerRec.objects.create(
                            student = cur_user.student,
                            exam = exam,
                            start_time = timezone.now(),
                            status = False,
                            mark_status = False
                        )
                else:
                    # exer = models.Exercise.objects.get(pk=event_id)
                    # rec = models.ExerAnswerRec.objects.filter(student=cur_user.student, exer=exer).first()
                    if rec is None:
                        models.ExerAnswerRec.objects.create(
                            student=cur_user.student,
                            exer=exer,
                            start_time = timezone.now(),
                            status = False,
                            mark_status = False
                        )
        return render(request, 'coding/coding-editor.html', context=content)

    def post(self, request, event_type, event_id, ques_id):
        '''Submit SQL'''
        # 如果是考试的话，交卷之后禁用POST
        # 如果是练习的话，交卷之后需等判卷完毕后才可以重新提交
        content = self.get_info(request, event_type, event_id, ques_id)
        cur_user = request.user
        if event_type == 'exam':
            try:
               cur_user.student.classroom.exam_set.get(pk = event_id) 
            except Exception as exc:
                content = {
                    'err_code': '403',
                    'err_message': _('没有权限'),
                }
                return render(request, 'error.html', context=content)   
            exam = models.Exam.objects.get(pk=event_id)
            if exam.end_time < timezone.now():
                content = {
                    'err_code': '403',
                    'err_message': _('已截止'),
                }
                return render(request, 'error.html', context=content)
            rec = models.ExamAnswerRec.objects.filter(student=cur_user.student, exam=exam).first()
            # print(rec.__dict__)
            if rec.status == True:
                content = {
                    'err_code': '403',
                    'err_message': _('已交卷，无法继续提交'),
                }
                return render(request, 'error.html', context=content)
        elif event_type == 'exer':
            try:
               cur_user.student.classroom.exercise_set.get(pk = event_id) 
            except Exception as exc:
                content = {
                    'err_code': '403',
                    'err_message': _('没有权限'),
                }
                return render(request, 'error.html', context=content)   
            exer = models.Exercise.objects.get(pk=event_id)
            if exer.end_time < timezone.now():
                content = {
                    'err_code': '403',
                    'err_message': _('已截止'),
                }
                return render(request, 'error.html', context=content)
            rec = models.ExerAnswerRec.objects.filter(student=cur_user.student, exer=exer).first()
            if rec.status == True and rec.mark_status == False:
                content = {
                    'err_code': '403',
                    'err_message': _('正在判卷，请在完成判卷后继续进行练习'),
                }
                return render(request, 'error.html', context=content)
        else:
            raise Resolver404


        # FIXME(Steve X): Monaco Editor 输入内容换行会消失
        if request.POST.get('movement') == 'submit':
            # print('提交成功')
            if cur_user.is_authenticated:
                if event_type == 'exam':
                    # print('是考试')
                    exam = models.Exam.objects.get(pk=event_id)
                    rec = models.ExamAnswerRec.objects.filter(student=cur_user.student, exam=exam).first()
                    if rec:
                        per_question = models.ExamQuesAnswerRec.objects.filter(user=cur_user,exam=rec)
                        if rec.status == False:
                            rec.end_time = timezone.now()
                            rec.status = True
                            rec.score = 0
                            # rec.mark_status = False
                            rec.save()
                        # print("已存在记录")
                else:
                    # print("是练习")
                    exer = models.Exercise.objects.get(pk=event_id)
                    rec = models.ExerAnswerRec.objects.filter(student=cur_user.student, exer=exer).first()
                    if rec:
                        per_question = models.ExerQuesAnswerRec.objects.filter(user=cur_user,exer=rec)
                        rec.end_time = timezone.now()
                        rec.status = True
                        rec.mark_status = False
                        rec.score = 0
                        rec.save()
                        # print("已存在记录")
            url = reverse('coding:coding')
            return HttpResponseRedirect(url)
            # return render(request, 'coding/coding-editor.html', context=content)
        submit_ans = request.POST.get('submit_ans')
        
        # print("输入的答案:",submit_ans)
        question = content.get('question')
        qset = question.ques_set
        # print("数据比对:",qset.db_name,question.ques_ans,submit_ans)
        correct = 'pending'
        ans_status = models.ExamQuesAnswerRec.AnsStatus.PD
        ans_status_color = 'warning'
        # Question-Answer record
        # print(event_type)
        if cur_user.is_authenticated:
            if event_type == 'exam':
                event = models.Exam.objects.get(exam_id=event_id)
                examrec = models.ExamAnswerRec.objects.filter(student=cur_user.student, exam=event).first()
                rec = models.ExamQuesAnswerRec.objects.filter(user=cur_user, question=question, exam=examrec).first()
            elif event_type == 'exer':
                event = models.Exercise.objects.get(exer_id=event_id)
                exerrec = models.ExerAnswerRec.objects.filter(student=cur_user.student, exer=event).first()
                rec = models.ExerQuesAnswerRec.objects.filter(user=cur_user, question=question, exer=exerrec).first()
            else:
                raise Resolver404
            now_paperquestion = models.PaperQuestion.objects.get(Q(question=question) & Q(paper=event.paper))
            if rec:
                rec.ans_status = ans_status
                rec.submit_cnt += 1
                rec.ans = submit_ans
                rec.score = 0
                rec.save()
            else:
                if event_type == 'exam':
                    rec = models.ExamQuesAnswerRec.objects.create(
                        user=cur_user,
                        question=question,
                        ans=submit_ans,
                        ans_status=ans_status,
                        submit_cnt=1,
                        exam=examrec,
                        score=0
                    )
                elif event_type == 'exer':
                    rec = models.ExerQuesAnswerRec.objects.create(
                        user=cur_user,
                        question=question,
                        ans=submit_ans,
                        ans_status=ans_status,
                        submit_cnt=1,
                        exer=exerrec,
                        score=0
                    )
                else:
                    raise Resolver404
        db_name_qset = 'qset_'+qset.db_name
        print('提交任务')
        sql_check_celery.delay(db_nm=db_name_qset, ans_sql=question.ques_ans, stud_sql=submit_ans, event_type=event_type, rec_id=rec.rec_id, score=now_paperquestion.score)
        content.update({
            'correct': correct,
            'ans_status_color': ans_status_color,
            'submit_ans': submit_ans,
        })
        url = reverse('coding:coding-editor', kwargs={'event_type': event_type,'event_id':event_id,'ques_id':ques_id})
        return HttpResponseRedirect(url)


def statistics(request):
    '''Render statistics template'''
    exer_active = models.Exercise.objects.filter(active=True).count()
    identity = request.user.identity()
    year = timezone.now() - datetime.timedelta(days=730) # 365 * 2    
    if request.user.is_superuser :
        exam_objects = models.Exam.objects.filter(publish_time__gte=year)
        exer_objects = models.Exercise.objects.filter(publish_time__gte=year)
    elif identity == 'teacher' or identity == 'teacher_student':
        rooms = request.user.teacher.teach_room()
        exam_objects = models.Exam.objects.filter(classroom__in = rooms, publish_time__gte=year).distinct()
        exer_objects = models.Exercise.objects.filter(classroom__in = rooms, publish_time__gte=year).distinct()
    else:
        exam_objects = models.Exam.objects.none()
        exer_objects = models.Exercise.objects.none()
        raise Resolver404

    content = {
        'exam_objects' : exam_objects,
        'exer_objects' : exer_objects,
    }

    return render(request, 'coding/statistics.html', context=content)


class PaperDetails(View):
    '''Exer/Exam analysis'''
    def get(self, request, event_type, event_id):
        cur_user = request.user
        if cur_user.is_authenticated:
            if event_type == 'exam':
                event = models.ExamAnswerRec.objects.get(pk=event_id)
                questions = models.ExamQuesAnswerRec.objects.filter(user=request.user,exam=event)
                event_set = event.exam
            elif event_type == 'exer':
                event = models.ExerAnswerRec.objects.get(pk=event_id)
                questions = models.ExerQuesAnswerRec.objects.filter(user=request.user,exer=event)
                event_set = event.exer
            else:
                raise Resolver404
        content = {
            'event' : event_set,
            'event_type' : event_type,
            'questions': questions,
        }
        return render(request, 'coding/analysis.html', context=content)


class ExamExerTeacherDetails(View):
    '''Exer/Exam analysis'''
    def get(self, request, event_type, event_id):
        cur_user = request.user
        if cur_user.is_authenticated:
            if event_type == 'exam':
                event = models.Exam.objects.get(pk=event_id)
                event_answer = models.ExamAnswerRec.objects.filter(exam=event,status=True)
                questions = models.ExamQuesAnswerRec.objects.filter(exam__in=event_answer)
            elif event_type == 'exer':
                event = models.Exercise.objects.get(pk=event_id)
                event_answer = models.ExerAnswerRec.objects.filter(exer=event,status=True)
                questions = models.ExerQuesAnswerRec.objects.filter(exer__in=event_answer)
            else:
                raise Resolver404
            classrooms = event.classroom.all()
            can_see = False
            if cur_user.is_superuser:
                can_see = True
            else:
                for classroom in classrooms:
                    if classroom.teacher == cur_user.teacher:
                        can_see = True
            if can_see:
                if event.finish_info[6] == 0:
                    finish_rate = 0 
                else:
                    finish_rate = (event.finish_info[0]/event.finish_info[6]) * 100
                    
                average_score = event.finish_info[7]
                avg_submit = questions.aggregate(avg_submit=Avg('submit_cnt'))['avg_submit']
                sum_students = 0
                if avg_submit is None:
                    avg_submit = 0  
                for classroom in event.classroom.all():
                    sum_students += classroom.students_count
                per_question = []
                per_avg_submit = []
                per_avg_acrate = []
                per_avg_finishrate = []
                for question in event.paper.question.all():
                    query = questions.filter(question=question)
                    avg_submit = query.aggregate(avg_submit=Avg('submit_cnt'))['avg_submit']
                    if avg_submit is None:
                        avg_submit = 0
                    if query.count() == 0:
                        per_avg_acrate.append(0)
                    else:
                        per_avg_acrate.append((query.filter(ans_status=0).count() / query.count()) * 100)
                    if sum_students == 0:
                        per_avg_finishrate.append(0)
                    else:
                        per_avg_finishrate.append((query.filter(ans_status=0).count() / sum_students) * 100)
                    per_avg_submit.append(int(avg_submit))
                    per_question.append(str(question.ques_id) + '-' + question.ques_name)
            else:
                raise Resolver404
        else:
                raise Resolver404
        content = {
            'event': event,
            'finish_rate' : finish_rate,
            'average_score': average_score,
            'avg_submit' : avg_submit,
            'per_avg_submit': per_avg_submit,
            'per_avg_acrate' : per_avg_acrate,
            'per_question' : per_question,
            'per_avg_finishrate' : per_avg_finishrate
        }
        return render(request, 'coding/teacher-analysis.html', context=content)
