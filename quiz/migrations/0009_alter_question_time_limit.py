# Generated by Django 5.1.6 on 2025-02-13 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0008_alter_result_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='time_limit',
            field=models.IntegerField(default=33),
        ),
    ]
