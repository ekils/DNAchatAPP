# Generated by Django 2.0.4 on 2018-07-17 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_remove_friendlist_requestnumbers'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='requestcheck',
            unique_together={('host_personal_ID', 'request_ID')},
        ),
    ]
