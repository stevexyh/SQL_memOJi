# Generated by Django 3.1.7 on 2022-02-13 02:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0050_delete_paperanswerrec'),
    ]

    operations = [
        migrations.DeleteModel(
            name='QuesAnswerRec',
        ),
    ]