# Generated by Django 4.1.2 on 2022-10-08 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_rename_count_student_booktaken'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issuedbook',
            name='can_renew',
        ),
    ]