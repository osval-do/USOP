# Generated by Django 5.0.7 on 2024-11-09 04:15

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_org_membership'),
    ]

    operations = [
        migrations.AddField(
            model_name='org',
            name='extid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, help_text='Automatically genered unique id for external identification', unique=True, verbose_name='Platform ID'),
        ),
        migrations.AddField(
            model_name='user',
            name='extid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, help_text='Automatically genered unique id for external identification', unique=True, verbose_name='Platform ID'),
        ),
    ]
