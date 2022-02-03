# Generated by Django 3.1.7 on 2022-02-03 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0011_auto_20220203_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paperquestion',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coding.question', verbose_name='题目列表'),
        ),
        migrations.AlterField(
            model_name='paperquestion',
            name='score',
            field=models.IntegerField(default=10, verbose_name='分值'),
        ),
    ]
