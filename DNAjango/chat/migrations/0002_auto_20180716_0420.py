# Generated by Django 2.0.4 on 2018-07-16 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personal',
            name='personal_ID',
        ),
        migrations.AddField(
            model_name='personal',
            name='personal_id',
            field=models.CharField(blank=True, max_length=25),
        ),
    ]
