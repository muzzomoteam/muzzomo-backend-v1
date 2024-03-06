# Generated by Django 5.0.2 on 2024-02-25 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0002_job_unit_alter_job_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='complete_time',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='start_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='complete_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='start_date',
            field=models.DateField(null=True),
        ),
    ]
