# Generated by Django 5.1.6 on 2025-02-14 07:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0010_alter_question_time_limit'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='answered',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='choice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.choice'),
        ),
    ]
