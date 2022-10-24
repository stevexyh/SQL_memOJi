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
    error_text = "None"
    try:
        stud_sql = '#' if stud_sql == '' else stud_sql
        # print("ans:",ans_sql,"stud:",stud_sql)
        correct = sql_check.ans_check(db_nm=db_nm, ans_sql=ans_sql, stud_sql=stud_sql)
    except Exception as e:
        print(e)
        # print("sql_checking........rec_id1-0-1:",rec_id)
        error_text = e
        correct = 'error'
    # print("sql_checking........rec_id1-1:",rec_id)
    ans_status = {
        True: models.ExamQuesAnswerRec.AnsStatus.AC,
        False: models.ExamQuesAnswerRec.AnsStatus.WA,
        'error': models.ExamQuesAnswerRec.AnsStatus.RE,
        'pending' : models.ExamQuesAnswerRec.AnsStatus.PD
    }.get(correct)
    # print("sql_checking........rec_id2:",rec_id)
    ans_status_color = {
        True: 'success',
        False: 'danger',
        'error': 'warning',
        'pending': 'warning',
    }.get(correct)
    # print("sql_checking........rec_id3:",rec_id)

    if event_type == 'exam':
        rec = models.ExamQuesAnswerRec.objects.get(rec_id=rec_id)
        answer_paper = rec.exam
    elif event_type == 'exer':
        rec = models.ExerQuesAnswerRec.objects.get(rec_id=rec_id)
        answer_paper = rec.exer
    else:
        rec = models.ExamQuesAnswerRec.none()
        answer_paper = models.ExamAnswerRec.none()
    # print("sql_checking........rec_id3:",rec_id)
    if ans_status == 0:
        final_score = score
    else:
        final_score = 0
        #XXX:(Seddon)把一道正确的题再交错，到底是按正确的还是错误的分数，有待商榷
    # print(rec)
    # print("sql_checking........rec_id4:",rec_id)
    # print("ans_status:",ans_status,"over")
    # print("correct:",correct,"correct_over")
    if rec:
        rec.ans_status = ans_status
        rec.submit_cnt += 1
        rec.ans = stud_sql
        rec.score = final_score
        rec.error_info = error_text
        rec.save()
    # print("sql_checking........rec_id5:",rec_id)

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
