# Generated by Django 3.1.7 on 2022-02-13 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_classroom_join_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='join_code',
            field=models.CharField(max_length=20, unique=True, verbose_name='班级识别码'),
        ),
    ]