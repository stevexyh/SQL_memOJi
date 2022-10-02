#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
----------------------------------------------------------------------------------------------------
* Project Name : SQL_memOJi
* File Name    : models.py
* Description  : 
* Create Time  : 2021-04-04 00:46:35
* Version      : 1.0
* Author       : Steve X
* GitHub       : https://github.com/Steve-Xyh/SQL_memOJi
----------------------------------------------------------------------------------------------------
* Notice
- 
- 
----------------------------------------------------------------------------------------------------
'''


from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Avg
from user.models import Student
# Create your models here.


class QuestionSet(models.Model):
    '''
    QuestionSet Table
    | 字段名                 | 数据类型             | 非空  | Key | 默认值       |
    |-----------------------|---------------------|------|-----|-------------|
    | ques_set_id           | varchar             |      | PRI |             |
    | ques_set_name         | varchar             |      |     |             |
    | ques_set_desc         | varchar             |      |     |             |
    | db_name               | varchar             |      | UNI |             |
    | create_sql            | varchar             |      |     |             |
    | initiator             | varchar             |      | API |             |
    '''

    ques_set_id = models.AutoField(verbose_name=_('题库ID'), primary_key=True)
    ques_set_name = models.CharField(verbose_name=_('题库名称'), max_length=100)
    ques_set_desc = models.TextField(verbose_name=_('题库描述'), null=True, blank=True)
    db_name = models.CharField(verbose_name=_('数据库名称'), unique=True, max_length=100, default='null')
    create_sql = models.TextField(verbose_name=_('创建SQL'))
    initiator = models.ForeignKey(verbose_name=_('发起人'), to='user.Teacher', on_delete=models.SET_NULL, null=True)
    share = models.BooleanField(verbose_name=_('其他老师可查看'), default=False)

    class Meta:
        verbose_name = '题库'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.ques_set_id) + '-' + self.ques_set_name


# XXX(Steve X): many-to-many intermediary models
class Question(models.Model):
    '''
    Question Table
    | 字段名                 | 数据类型             | 非空  | Key | 默认值       |
    |-----------------------|---------------------|------|-----|-------------|
    | ques_id               | varchar             |      | PRI |             |
    | ques_name             | varchar             | NULL |     | 未命名       |
    | ques_set              | varchar             |      | FK  |             |
    | ques_difficulty       | int                 | NULL |     |             |
    | ques_desc             | varchar             |      |     |             |
    | ques_ans              | varchar             |      |     |             |
    | initiator             | varchar             |      | API |             |
    '''

    class Difficulty(models.IntegerChoices):
        '''Enumeration of question difficulty'''

        UNKNOWN = -1, _('未知')
        EASY = 0, _('简单')
        MEDIUM = 1, ('中等')
        HARD = 2, _('困难')

    ques_id = models.AutoField(verbose_name=_('题目ID'), primary_key=True)
    ques_name = models.CharField(verbose_name=_('题目名称'), max_length=100, null=True, default=_('未命名'))
    ques_set = models.ForeignKey(verbose_name=_('所属题库'), to=QuestionSet, on_delete=models.CASCADE)
    ques_difficulty = models.IntegerField(verbose_name=_('题目难度'), choices=Difficulty.choices, default=Difficulty.UNKNOWN)
    ques_desc = models.TextField(verbose_name=_('题目描述'))
    ques_ans = models.TextField(verbose_name=_('标准答案'))
    initiator = models.ForeignKey(verbose_name=_('发起人'), to='user.Teacher', on_delete=models.SET_NULL, null=True)
    share = models.BooleanField(verbose_name=_('其他老师可查看'), default=False)

    class Meta:
        verbose_name = '题目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.ques_id) + '-' + self.ques_name + '-' + self.ques_desc


# XXX(Steve X): many-to-many intermediary models
class Paper(models.Model):
    '''
    Paper Table
    | 字段名                 | 数据类型             | 非空  | Key | 默认值       |
    |-----------------------|---------------------|------|-----|-------------|
    | paper_id              | varchar             |      | PRI |             |
    | paper_name            | varchar             |      |     |             |
    | publish_time          | datetime            |      |     |             |
    | paper_desc            | varchar             | NULL |     |             |
    | initiator             | varchar             |      | API |             |
    | question              | varchar             |      | M2M |             |
    '''

    paper_id = models.AutoField(verbose_name=_('试卷ID'), primary_key=True)
    paper_name = models.CharField(verbose_name=_('试卷名称'), max_length=100)
    publish_time = models.DateTimeField(verbose_name=_('发布时间'), auto_now_add=True)
    paper_desc = models.TextField(verbose_name=_('试卷描述'), null=True, blank=True)
    initiator = models.ForeignKey(verbose_name=_('发起人'), to='user.Teacher', on_delete=models.SET_NULL, null=True)
    question = models.ManyToManyField(verbose_name=_('题目列表'),to=Question,through='PaperQuestion')
    share = models.BooleanField(verbose_name=_('其他老师可查看'), default=False)

    def total_score(self):
        questions = self.paperquestion_set.filter(paper=self)
        total_score = 0
        for question in questions:
            total_score += question.score
        return total_score
    total_score.short_description = '试卷总分'
    class Meta:
        verbose_name = '试卷'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.paper_id) + '-' + self.paper_name

class PaperQuestion(models.Model):
    #XXX(Seddon):应该就是级联删除CASCADE 具体有待商榷
    question = models.ForeignKey(verbose_name=_('题目列表'),to=Question,on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper,on_delete=models.CASCADE)
    score = models.IntegerField(verbose_name=_('分值'),default=10)

    def __str__(self):
        return str(self.paper)

    class Meta:
        verbose_name = '题目和分值'
        verbose_name_plural = verbose_name
        db_table = "Paper_Question_relationship"
        
class Exam(models.Model):
    '''
    Exam Table
    | 字段名                 | 数据类型             | 非空  | Key    | 默认值       |
    |-----------------------|---------------------|------|--------|-------------|
    | exam_id               | varchar             |      | PRI    |             |
    | exam_name             | varchar             |      |        | 未命名       |
    | paper                 | varchar             |      | FK     |             |
    | start_time            | datetime            |      |        |             |
    | end_time              | datetime            |      |        |             |
    | publish_time          | datetime            |      |        |             |
    | desc                  | varchar             | NULL |        |             |
    | active                | bool                |      |        | True        |
    | classroom             | varchar             |      | M2M    |             |
    '''

    exam_id = models.AutoField(verbose_name=_('考试ID'), primary_key=True)
    exam_name = models.CharField(verbose_name=_('考试名称'), max_length=100, default=_('未命名'))
    paper = models.ForeignKey(verbose_name=_('试卷'), to=Paper, on_delete=models.CASCADE)
    start_time = models.DateTimeField(verbose_name=_('开始时间'), default=None)
    end_time = models.DateTimeField(verbose_name=_('结束时间'), default=None)
    publish_time = models.DateTimeField(verbose_name=_('发布时间'), auto_now_add=True)
    desc = models.TextField(verbose_name=_('描述'), null=True, blank=True)
    active = models.BooleanField(verbose_name=_('发布'), default=False)
    classroom = models.ManyToManyField(verbose_name=_('分配班级'), to='user.Classroom')
    show_answer = models.BooleanField(verbose_name=_('在解析中公布答案'),default=False)
    def __str__(self):
        return str(self.exam_id) + str('-') + str(self.exam_name)

    class Meta:
        verbose_name = '考试'
        verbose_name_plural = verbose_name

    @property
    def is_over(self):
        return timezone.now() > self.end_time

    @property
    def first_ques(self):
        # query_result = .objects.filter(exam=self, status=True)
        questions = self.paper.paperquestion_set.filter(paper=self.paper)
        return questions.first().question.ques_id

    @property
    def finish_info(self):
        query_result = ExamAnswerRec.objects.filter(exam=self, status=True)
        have_finished = query_result.count()
        all_students =  Student.objects.filter(classroom__in=self.classroom.all()).count()
        unfinished = all_students - have_finished
        total_score = self.paper.total_score()
        # excellent >= 85%
        # good >= 70%
        # fair >= 60%
        # fail < 60%
        excellent = query_result.filter(score__gte=total_score * 0.85).count()
        good = query_result.filter(score__gte=total_score * 0.70).count() - excellent
        fair = query_result.filter(score__gte=total_score * 0.6).count() - excellent - good
        fail = query_result.filter(score__lt=total_score * 0.6).count()
        average_score = query_result.aggregate(average_score=Avg('score'))
        # query = ExerQuesAnswerRec.objects.filter(user=self.student.user,exer=self).aggregate(avg_submit=Avg('submit_cnt'))

        return have_finished,unfinished,excellent,good,fair,fail,all_students,average_score['average_score']

    
class Exercise(models.Model):
    '''
    Exercise Table
    | 字段名                 | 数据类型             | 非空  | Key    | 默认值       |
    |-----------------------|---------------------|------|--------|-------------|
    | exer_id               | varchar             |      | PRI    |             |
    | exer_name             | varchar             |      |        | 未命名       |
    | paper                 | varchar             |      | FK,UNI |             |
    | publish_time          | datetime            |      |        |             |
    | desc                  | varchar             | NULL |        |             |
    | active                | bool                |      |        | True        |
    | classroom             | varchar             |      | M2M    |             |
    '''

    exer_id = models.AutoField(verbose_name=_('练习ID'), primary_key=True)
    exer_name = models.CharField(verbose_name=_('练习名称'), max_length=100, default=_('未命名'))
    paper = models.ForeignKey(verbose_name=_('试卷'), to=Paper, on_delete=models.CASCADE)
    start_time = models.DateTimeField(verbose_name=_('开始时间'), default=None)
    end_time = models.DateTimeField(verbose_name=_('结束时间'), default=None)
    publish_time = models.DateTimeField(verbose_name=_('发布时间'), auto_now_add=True)
    desc = models.TextField(verbose_name=_('描述'), null=True, blank=True)
    active = models.BooleanField(verbose_name=_('发布'), default=False)
    classroom = models.ManyToManyField(verbose_name=_('分配班级'), to='user.Classroom')

    def __str__(self):
        return str(self.exer_id) + str('-') + str(self.exer_name)

    class Meta:
        verbose_name = '练习'
        verbose_name_plural = verbose_name

    @property
    def finish_info(self):
        query_result = ExerAnswerRec.objects.filter(exer=self, status=True)
        have_finished = query_result.count()
        all_students =  Student.objects.filter(classroom__in=self.classroom.all()).count()
        unfinished = all_students - have_finished
        total_score = self.paper.total_score()
        # excellent >= 85%
        # good >= 70%
        # fair >= 60%
        # fail < 60%
        excellent = query_result.filter(score__gte=total_score * 0.85).count()
        good = query_result.filter(score__gte=total_score * 0.70).count() - excellent
        fair = query_result.filter(score__gte=total_score * 0.6).count() - excellent - good
        fail = query_result.filter(score__lt=total_score * 0.6).count()
        average_score = query_result.aggregate(average_score=Avg('score'))
        return have_finished,unfinished,excellent,good,fair,fail,all_students,average_score['average_score']
    @property
    def is_over(self):
        return timezone.now() > self.end_time

    @property
    def first_ques(self):
        # query_result = .objects.filter(exam=self, status=True)
        questions = self.paper.paperquestion_set.filter(paper=self.paper)
        return questions.first().question.ques_id
        
# class QuesAnswerRec(models.Model):
#     '''
#     Question Answer Record Table
#     | 字段名                 | 数据类型             | 非空  | Key | 默认值       |
#     |-----------------------|---------------------|------|-----|-------------|
#     | rec_id                | varchar             |      | PRI |             |
#     | user                  | varchar             |      | API |             |
#     | question              | varchar             | NULL | FK  |             |
#     | ans                   | varchar             | NULL |     |             |
#     | ans_status            | int                 |      |     | -1          |
#     | submit_time           | datetime            |      |     |             |
#     | submit_cnt            | int                 |      |     | 0           |
#     '''

#     class AnsStatus(models.IntegerChoices):
#         '''Enumeration of answer status'''

#         UNKNOWN = -1, _('未知')
#         AC = 0, _('答案正确')
#         WA = 1, ('答案错误')
#         RE = 2, _('运行异常')
#         PD = 3,_('正在运行')

#     rec_id = models.AutoField(verbose_name=_('记录ID'), primary_key=True)
#     user = models.ForeignKey(verbose_name=_('用户'), to='user.User', on_delete=models.CASCADE)
#     question = models.ForeignKey(verbose_name=_('题目'), to=Question, null=True, on_delete=models.SET_NULL)
#     ans = models.TextField(verbose_name=_('最新答案'), null=True, blank=True)
#     ans_status = models.IntegerField(verbose_name=_('答案正确性'), choices=AnsStatus.choices, default=AnsStatus.UNKNOWN)
#     submit_time = models.DateTimeField(verbose_name=_('最后提交时间'), auto_now=True)
#     submit_cnt = models.IntegerField(verbose_name=_('提交次数'), default=0)

#     class Meta:
#         verbose_name = '题目作答记录(*)'
#         verbose_name_plural = verbose_name

# # TODO(Steve X): Exam & Exer record
# class PaperAnswerRec(models.Model):
#     '''
#     Paper Answer Record Table
#     | 字段名                 | 数据类型             | 非空  | Key | 默认值       |
#     |-----------------------|---------------------|------|-----|-------------|
#     | rec_id                | varchar             |      | PRI |             |
#     | student               | varchar             |      | API |             |
#     | paper                 | varchar             |      | FK  |             |
#     | start_time            | datetime            |      |     |             |
#     | end_time              | datetime            |      |     |             |
#     | score                 | int                 |      |     | 0           |
#     '''
#     class Recclass(models.IntegerChoices):
#         '''Enumeration of rec classes exam/exec'''

#         UNKNOWN = -1, _('未知')
#         EXAM = 0, _('考试')
#         EXEC = 1, ('练习')


#     rec_id = models.AutoField(verbose_name=_('记录ID'), primary_key=True)
#     student = models.ForeignKey(verbose_name=_('学生'), to='user.Student', on_delete=models.CASCADE)
#     paper = models.ForeignKey(verbose_name=_('试卷'), to=Paper, on_delete=models.DO_NOTHING)
#     start_time = models.DateTimeField(verbose_name=_('开始时间'))
#     end_time = models.DateTimeField(verbose_name=_('交卷时间'))
#     score = models.IntegerField(verbose_name=_('总成绩'), default=0)
#     #Seddon New Add
#     paper_class = models.IntegerField(verbose_name=_('试卷类型'), choices=Recclass.choices, default=Recclass.UNKNOWN)

#     class Meta:
#         verbose_name = '试卷作答记录(应该是没用了)'
#         verbose_name_plural = verbose_name

class ExamAnswerRec(models.Model):
    '''
    Paper Answer Record Table
    | 字段名                 | 数据类型             | 非空  | Key | 默认值       |
    |-----------------------|---------------------|------|-----|-------------|
    | rec_id                | varchar             |      | PRI |             |
    | student               | varchar             |      | API |             |
    | paper                 | varchar             |      | FK  |             |
    | start_time            | datetime            |      |     |             |
    | end_time              | datetime            |      |     |             |
    | score                 | int                 |      |     | 0           |
    '''

    rec_id = models.AutoField(verbose_name=_('考试记录ID'), primary_key=True)
    student = models.ForeignKey(verbose_name=_('学生'), to='user.Student', on_delete=models.CASCADE)
    exam = models.ForeignKey(verbose_name=_('考试'), to=Exam, on_delete=models.CASCADE)
    start_time = models.DateTimeField(verbose_name=_('开始时间'))
    end_time = models.DateTimeField(verbose_name=_('交卷时间'),null=True, blank=True)
    score = models.IntegerField(verbose_name=_('总成绩'), default=0,null=True, blank=True)
    status = models.BooleanField(verbose_name=_('提交状态'), default=False)
    mark_status = models.BooleanField(verbose_name=_('阅卷状态'), default=False)

    @property
    def per_submit(self):
        query = ExamQuesAnswerRec.objects.filter(user=self.student.user,exam=self).aggregate(avg_submit=Avg('submit_cnt'))
        if query['avg_submit'] is None:
            count = 0
        else:
            count = query['avg_submit']
        return count
    
    @property
    def wrong_count(self):
        wrong_qustions = ExamQuesAnswerRec.objects.filter(user=self.student.user,exam=self).exclude(ans_status=0).count()
        return wrong_qustions

    def __str__(self):
        return str(self.rec_id) + "-" + str(self.student) + "-" + str(self.exam)
    class Meta:
        verbose_name = '考试作答记录'
        verbose_name_plural = verbose_name


class ExerAnswerRec(models.Model):
    '''
    Paper Answer Record Table
    | 字段名                 | 数据类型             | 非空  | Key | 默认值       |
    |-----------------------|---------------------|------|-----|-------------|
    | rec_id                | varchar             |      | PRI |             |
    | student               | varchar             |      | API |             |
    | paper                 | varchar             |      | FK  |             |
    | start_time            | datetime            |      |     |             |
    | end_time              | datetime            |      |     |             |
    | score                 | int                 |      |     | 0           |
    '''

    rec_id = models.AutoField(verbose_name=_('练习记录ID'), primary_key=True)
    student = models.ForeignKey(verbose_name=_('学生'), to='user.Student', on_delete=models.CASCADE)
    exer = models.ForeignKey(verbose_name=_('练习'), to=Exercise, on_delete=models.CASCADE)
    start_time = models.DateTimeField(verbose_name=_('开始时间'))
    end_time = models.DateTimeField(verbose_name=_('交卷时间'),null=True, blank=True)
    score = models.IntegerField(verbose_name=_('总成绩'), default=0,null=True, blank=True)
    status = models.BooleanField(verbose_name=_('提交状态'), default=False)
    mark_status = models.BooleanField(verbose_name=_('阅卷状态'), default=False)

    @property
    def wrong_count(self):
        wrong_qustions = ExerQuesAnswerRec.objects.filter(user=self.student.user,exer=self).exclude(ans_status=0).count()
        return wrong_qustions

    @property
    def per_submit(self):
        query = ExerQuesAnswerRec.objects.filter(user=self.student.user,exer=self).aggregate(avg_submit=Avg('submit_cnt'))
        if query['avg_submit'] is None:
            count = 0
        else:
            count = query['avg_submit']
        return count

    def __str__(self):
        return str(self.rec_id) + "-" + str(self.student) + "-" + str(self.exer)

    class Meta:
        verbose_name = '练习作答记录'
        verbose_name_plural = verbose_name


class ExamQuesAnswerRec(models.Model):
    '''
    Exam Question Answer Record Table
    | 字段名                 | 数据类型             | 非空  | Key | 默认值       |
    |-----------------------|---------------------|------|-----|-------------|
    | rec_id                | varchar             |      | PRI |             |
    | user                  | varchar             |      | API |             |
    | exam                  | varchar             | NULL | FK  |             |
    | question              | varchar             | NULL | FK  |             |
    | ans                   | varchar             | NULL |     |             |
    | ans_status            | int                 |      |     | -1          |
    | score                 | int                 |      |     | 0           |
    | submit_time           | datetime            |      |     |             |
    | submit_cnt            | int                 |      |     | 0           |
    '''

    class AnsStatus(models.IntegerChoices):
        '''Enumeration of answer status'''

        UNKNOWN = -1, _('未知')
        AC = 0, _('答案正确')
        WA = 1, ('答案错误')
        RE = 2, _('运行异常')
        PD = 3,_('正在运行')

    rec_id = models.AutoField(verbose_name=_('记录ID'), primary_key=True)
    user = models.ForeignKey(verbose_name=_('用户'), to='user.User', on_delete=models.CASCADE)
    exam = models.ForeignKey(verbose_name=_('对应考试记录'), to=ExamAnswerRec,on_delete=models.CASCADE,null=True)
    question = models.ForeignKey(verbose_name=_('题目'), to=Question, null=True, on_delete=models.SET_NULL)
    ans = models.TextField(verbose_name=_('最新答案'), null=True, blank=True)
    ans_status = models.IntegerField(verbose_name=_('答案正确性'), choices=AnsStatus.choices, default=AnsStatus.UNKNOWN)
    score = models.IntegerField(verbose_name=_('本题得分'), default=0)
    submit_time = models.DateTimeField(verbose_name=_('最后提交时间'), auto_now=True)
    submit_cnt = models.IntegerField(verbose_name=_('提交次数'), default=0)

    def __str__(self):
        return str(self.rec_id) + "-" + str(self.user) + "-" + str(self.exam) + "-" + str(self.question)

    class Meta:
        verbose_name = '题目作答记录(考试)'
        verbose_name_plural = verbose_name

class ExerQuesAnswerRec(models.Model):
    '''
    Exer Question Answer Record Table
    | 字段名                 | 数据类型             | 非空  | Key | 默认值       |
    |-----------------------|---------------------|------|-----|-------------|
    | rec_id                | varchar             |      | PRI |             |
    | user                  | varchar             |      | API |             |
    | erer                  | varchar             | NULL | FK  |             |
    | question              | varchar             | NULL | FK  |             |
    | ans                   | varchar             | NULL |     |             |
    | ans_status            | int                 |      |     | -1          |
    | score                 | int                 |      |     | 0           |
    | submit_time           | datetime            |      |     |             |
    | submit_cnt            | int                 |      |     | 0           |
    '''

    class AnsStatus(models.IntegerChoices):
        '''Enumeration of answer status'''

        UNKNOWN = -1, _('未知')
        AC = 0, _('答案正确')
        WA = 1, ('答案错误')
        RE = 2, _('运行异常')
        PD = 3,_('正在运行')

    rec_id = models.AutoField(verbose_name=_('记录ID'), primary_key=True)
    user = models.ForeignKey(verbose_name=_('用户'), to='user.User', on_delete=models.CASCADE)
    exer = models.ForeignKey(verbose_name=_('对应练习记录'), to=ExerAnswerRec,on_delete=models.CASCADE,null=True)
    question = models.ForeignKey(verbose_name=_('题目'), to=Question, null=True, on_delete=models.SET_NULL)
    ans = models.TextField(verbose_name=_('最新答案'), null=True, blank=True)
    ans_status = models.IntegerField(verbose_name=_('答案正确性'), choices=AnsStatus.choices, default=AnsStatus.UNKNOWN)
    score = models.IntegerField(verbose_name=_('本题得分'), default=0)
    submit_time = models.DateTimeField(verbose_name=_('最后提交时间'), auto_now=True)
    submit_cnt = models.IntegerField(verbose_name=_('提交次数'), default=0)

    def __str__(self):
        return str(self.rec_id) + "-" + str(self.user) + "-" + str(self.exer) + "-" + str(self.question)

    class Meta:
        verbose_name = '题目作答记录(练习)'
        verbose_name_plural = verbose_name
