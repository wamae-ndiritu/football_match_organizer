# Generated by Django 4.2 on 2025-03-25 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teamuser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='teamuser',
            name='last_name',
        ),
        migrations.AlterField(
            model_name='teamuser',
            name='coach_contact',
            field=models.CharField(default='0712345678', max_length=100),
        ),
        migrations.AlterField(
            model_name='teamuser',
            name='coach_name',
            field=models.CharField(default='John Doe', max_length=100),
        ),
        migrations.AlterField(
            model_name='teamuser',
            name='team_name',
            field=models.CharField(default='Team Name', max_length=100),
        ),
    ]
