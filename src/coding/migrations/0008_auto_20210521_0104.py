# Generated by Django 3.1.7 on 2021-05-20 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0007_auto_20210520_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionset',
            name='db_name',
            field=models.CharField(default='null', max_length=100, unique=True, verbose_name='数据库名称'),
        ),
    ]