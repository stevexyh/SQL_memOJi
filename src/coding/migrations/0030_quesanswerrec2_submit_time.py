# Generated by Django 3.1.7 on 2022-02-06 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0029_quesanswerrec2_submit_cnt'),
    ]

    operations = [
        migrations.AddField(
            model_name='quesanswerrec2',
            name='submit_time',
            field=models.DateTimeField(auto_now=True, verbose_name='最后提交时间'),
        ),
    ]