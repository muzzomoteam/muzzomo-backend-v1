# Generated by Django 5.0.2 on 2024-03-06 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0004_job_job_description_job_service_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]