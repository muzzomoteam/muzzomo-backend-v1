# Generated by Django 5.0.2 on 2024-02-25 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='unit',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='address',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
