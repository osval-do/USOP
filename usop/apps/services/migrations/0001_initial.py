# Generated by Django 5.0.7 on 2024-11-18 21:55

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0005_alter_org_extid_alter_user_extid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('disabled', models.BooleanField()),
            ],
            options={
                'verbose_name': 'region',
                'verbose_name_plural': 'regions',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('blocked', models.BooleanField(default=False)),
                ('extid', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Automatically generated id for external identification of the service', unique=True, verbose_name='Platform ID')),
                ('pid', models.UUIDField(default=uuid.uuid4, editable=False, help_text='UUID for tracking of this service on the deployment platform', unique=True, verbose_name='Platform ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='users.org')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='services.region')),
            ],
            options={
                'verbose_name': 'service',
                'verbose_name_plural': 'services',
                'ordering': ['name'],
                'indexes': [models.Index(fields=['extid'], name='services_se_extid_46f724_idx'), models.Index(fields=['pid'], name='services_se_pid_ef14a7_idx')],
            },
        ),
    ]
