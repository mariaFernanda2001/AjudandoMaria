# Generated by Django 2.2.6 on 2019-10-06 01:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='desafio',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='resposta',
            name='likes',
        ),
    ]
