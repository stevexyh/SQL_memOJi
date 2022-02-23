# Generated by Django 3.1.7 on 2022-02-23 03:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('exam_id', models.AutoField(primary_key=True, serialize=False, verbose_name='考试ID')),
                ('exam_name', models.CharField(default='未命名', max_length=100, verbose_name='考试名称')),
                ('start_time', models.DateTimeField(default=None, verbose_name='开始时间')),
                ('end_time', models.DateTimeField(default=None, verbose_name='结束时间')),
                ('publish_time', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='描述')),
                ('active', models.BooleanField(default=False, verbose_name='发布状态')),
                # ('show_answer', models.BooleanField(default=False, verbose_name='在解析中公布答案')),
                ('classroom', models.ManyToManyField(to='user.Classroom', verbose_name='分配班级')),
            ],
            options={
                'verbose_name': '考试',
                'verbose_name_plural': '考试',
            },
        ),
        migrations.CreateModel(
            name='ExamAnswerRec',
            fields=[
                ('rec_id', models.AutoField(primary_key=True, serialize=False, verbose_name='考试记录ID')),
                ('start_time', models.DateTimeField(verbose_name='开始时间')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='交卷时间')),
                ('score', models.IntegerField(blank=True, default=0, null=True, verbose_name='总成绩')),
                ('status', models.BooleanField(default=False, verbose_name='提交状态')),
                ('mark_status', models.BooleanField(default=False, verbose_name='阅卷状态')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='coding.exam', verbose_name='考试')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.student', verbose_name='学生')),
            ],
            options={
                'verbose_name': '考试作答记录',
                'verbose_name_plural': '考试作答记录',
            },
        ),
        migrations.CreateModel(
            name='ExerAnswerRec',
            fields=[
                ('rec_id', models.AutoField(primary_key=True, serialize=False, verbose_name='练习记录ID')),
                ('start_time', models.DateTimeField(verbose_name='开始时间')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='交卷时间')),
                ('score', models.IntegerField(blank=True, default=0, null=True, verbose_name='总成绩')),
                ('status', models.BooleanField(default=False, verbose_name='提交状态')),
                ('mark_status', models.BooleanField(default=False, verbose_name='阅卷状态')),
            ],
            options={
                'verbose_name': '练习作答记录',
                'verbose_name_plural': '练习作答记录',
            },
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('paper_id', models.AutoField(primary_key=True, serialize=False, verbose_name='试卷ID')),
                ('paper_name', models.CharField(max_length=100, verbose_name='试卷名称')),
                ('publish_time', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('paper_desc', models.TextField(blank=True, null=True, verbose_name='试卷描述')),
                ('share', models.BooleanField(default=False, verbose_name='其他老师可查看')),
                ('initiator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.teacher', verbose_name='发起人')),
            ],
            options={
                'verbose_name': '试卷',
                'verbose_name_plural': '试卷',
            },
        ),
        migrations.CreateModel(
            name='QuestionSet',
            fields=[
                ('ques_set_id', models.AutoField(primary_key=True, serialize=False, verbose_name='题库ID')),
                ('ques_set_name', models.CharField(max_length=100, verbose_name='题库名称')),
                ('ques_set_desc', models.TextField(blank=True, null=True, verbose_name='题库描述')),
                ('db_name', models.CharField(default='null', max_length=100, unique=True, verbose_name='数据库名称')),
                ('create_sql', models.TextField(verbose_name='创建SQL')),
                ('share', models.BooleanField(default=False, verbose_name='其他老师可查看')),
                ('initiator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.teacher', verbose_name='发起人')),
            ],
            options={
                'verbose_name': '题库',
                'verbose_name_plural': '题库',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('ques_id', models.AutoField(primary_key=True, serialize=False, verbose_name='题目ID')),
                ('ques_name', models.CharField(default='未命名', max_length=100, null=True, verbose_name='题目名称')),
                ('ques_difficulty', models.IntegerField(choices=[(-1, '未知'), (0, '简单'), (1, '中等'), (2, '困难')], default=-1, verbose_name='题目难度')),
                ('ques_desc', models.TextField(verbose_name='题目描述')),
                ('ques_ans', models.TextField(verbose_name='标准答案')),
                ('share', models.BooleanField(default=False, verbose_name='其他老师可查看')),
                ('initiator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.teacher', verbose_name='发起人')),
                ('ques_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coding.questionset', verbose_name='所属题库')),
            ],
            options={
                'verbose_name': '题目',
                'verbose_name_plural': '题目',
            },
        ),
        migrations.CreateModel(
            name='PaperQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=10, verbose_name='分值')),
                ('paper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coding.paper')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coding.question', verbose_name='题目列表')),
            ],
            options={
                'verbose_name': '题目和分值',
                'verbose_name_plural': '题目和分值',
                'db_table': 'Paper_Question_relationship',
            },
        ),
        migrations.AddField(
            model_name='paper',
            name='question',
            field=models.ManyToManyField(through='coding.PaperQuestion', to='coding.Question', verbose_name='题目列表'),
        ),
        migrations.CreateModel(
            name='ExerQuesAnswerRec',
            fields=[
                ('rec_id', models.AutoField(primary_key=True, serialize=False, verbose_name='记录ID')),
                ('ans', models.TextField(blank=True, null=True, verbose_name='最新答案')),
                ('ans_status', models.IntegerField(choices=[(-1, '未知'), (0, '答案正确'), (1, '答案错误'), (2, '运行异常'), (3, '正在运行')], default=-1, verbose_name='答案正确性')),
                ('score', models.IntegerField(default=0, verbose_name='本题得分')),
                ('submit_time', models.DateTimeField(auto_now=True, verbose_name='最后提交时间')),
                ('submit_cnt', models.IntegerField(default=0, verbose_name='提交次数')),
                ('exer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='coding.exeranswerrec', verbose_name='对应练习记录')),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='coding.question', verbose_name='题目')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '题目作答记录(练习)',
                'verbose_name_plural': '题目作答记录(练习)',
            },
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('exer_id', models.AutoField(primary_key=True, serialize=False, verbose_name='练习ID')),
                ('exer_name', models.CharField(default='未命名', max_length=100, verbose_name='练习名称')),
                ('start_time', models.DateTimeField(default=None, verbose_name='开始时间')),
                ('end_time', models.DateTimeField(default=None, verbose_name='结束时间')),
                ('publish_time', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='描述')),
                ('active', models.BooleanField(default=False, verbose_name='发布状态')),
                ('classroom', models.ManyToManyField(to='user.Classroom', verbose_name='分配班级')),
                ('paper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coding.paper', verbose_name='试卷')),
            ],
            options={
                'verbose_name': '练习',
                'verbose_name_plural': '练习',
            },
        ),
        migrations.AddField(
            model_name='exeranswerrec',
            name='exer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='coding.exercise', verbose_name='练习'),
        ),
        migrations.AddField(
            model_name='exeranswerrec',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.student', verbose_name='学生'),
        ),
        migrations.CreateModel(
            name='ExamQuesAnswerRec',
            fields=[
                ('rec_id', models.AutoField(primary_key=True, serialize=False, verbose_name='记录ID')),
                ('ans', models.TextField(blank=True, null=True, verbose_name='最新答案')),
                ('ans_status', models.IntegerField(choices=[(-1, '未知'), (0, '答案正确'), (1, '答案错误'), (2, '运行异常'), (3, '正在运行')], default=-1, verbose_name='答案正确性')),
                ('score', models.IntegerField(default=0, verbose_name='本题得分')),
                ('submit_time', models.DateTimeField(auto_now=True, verbose_name='最后提交时间')),
                ('submit_cnt', models.IntegerField(default=0, verbose_name='提交次数')),
                ('exam', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='coding.examanswerrec', verbose_name='对应考试记录')),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='coding.question', verbose_name='题目')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '题目作答记录(考试)',
                'verbose_name_plural': '题目作答记录(考试)',
            },
        ),
        migrations.AddField(
            model_name='exam',
            name='paper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coding.paper', verbose_name='试卷'),
        ),
    ]
