# Generated by Django 3.1.7 on 2022-02-06 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0016_auto_20220203_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='examanswerrec',
            name='status',
            field=models.BooleanField(default=False, verbose_name='提交状态'),
        ),
        migrations.AddField(
            model_name='exeranswerrec',
            name='status',
            field=models.BooleanField(default=False, verbose_name='提交状态'),
        ),
    ]