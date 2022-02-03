# Generated by Django 3.1.7 on 2022-02-03 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0014_auto_20220203_1721'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paperanswerrec',
            options={'verbose_name': '试卷作答记录(应该是没用了)', 'verbose_name_plural': '试卷作答记录(应该是没用了)'},
        ),
        migrations.AlterField(
            model_name='examanswerrec',
            name='rec_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='考试记录ID'),
        ),
        migrations.AlterField(
            model_name='exeranswerrec',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='交卷时间'),
        ),
        migrations.AlterField(
            model_name='exeranswerrec',
            name='rec_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='练习记录ID'),
        ),
        migrations.AlterField(
            model_name='exeranswerrec',
            name='score',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='总成绩'),
        ),
    ]
