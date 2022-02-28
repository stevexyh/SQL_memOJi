# coding/tasks.py
import os, time
from django.template.loader import render_to_string
from django.conf import settings
from celery import shared_task
from utils import sql_check
from coding import models
from django.db.models import Sum

@shared_task
def sql_check_celery(db_nm, ans_sql, stud_sql, event_type, rec_id, score):
    print("sql_checking........rec_id:",rec_id)
    try:
        stud_sql = '#' if stud_sql == '' else stud_sql
        correct = sql_check.ans_check(db_nm=db_nm, ans_sql=ans_sql, stud_sql=stud_sql)
    except Exception as e:
        print(e)
        correct = 'error'
    ans_status = {
        True: models.ExamQuesAnswerRec.AnsStatus.AC,
        False: models.ExamQuesAnswerRec.AnsStatus.WA,
        'error': models.ExamQuesAnswerRec.AnsStatus.RE,
        'pending' : models.ExamQuesAnswerRec.AnsStatus.PD
    }.get(correct)
    ans_status_color = {
        True: 'success',
        False: 'danger',
        'error': 'warning',
        'pending': 'warning',
    }.get(correct)

    if event_type == 'exam':
        rec = models.ExamQuesAnswerRec.objects.get(rec_id=rec_id)
        answer_paper = rec.exam
    elif event_type == 'exer':
        rec = models.ExerQuesAnswerRec.objects.get(rec_id=rec_id)
        answer_paper = rec.exer
    else:
        rec = models.ExamQuesAnswerRec.none()
        answer_paper = models.ExamAnswerRec.none()
    if ans_status == 0:
        final_score = score
    else:
        final_score = 0
        #XXX:(Seddon)把一道正确的题再交错，到底是按正确的还是错误的分数，有待商榷            
    if rec:
        rec.ans_status = ans_status
        rec.submit_cnt += 1
        rec.ans = stud_sql
        rec.score = final_score
        rec.save()

@shared_task
def mark_paper():
    print('------- 正在阅卷 -------')
    exam_answer_paper = models.ExamAnswerRec.objects.filter(status=True,mark_status=False)
    print('在tasks中阅卷2')
    for paper in exam_answer_paper:
        print("待阅卷:",paper)
        questions_rec = models.ExamQuesAnswerRec.objects.filter(exam=paper)
        if questions_rec.filter(ans_status=3).count() == 0:
            paper.score = questions_rec.aggregate(Sum('score'))['score__sum']
            paper.mark_status = True
            paper.save()

    exer_answer_paper = models.ExerAnswerRec.objects.filter(status=True,mark_status=False)
    for paper in exer_answer_paper:
        print("待阅卷:",paper)
        questions_rec = models.ExerQuesAnswerRec.objects.filter(exer=paper)
        if questions_rec.filter(ans_status=3).count() == 0:
            paper.score = questions_rec.aggregate(Sum('score'))['score__sum']
            paper.mark_status = True
            paper.save()
