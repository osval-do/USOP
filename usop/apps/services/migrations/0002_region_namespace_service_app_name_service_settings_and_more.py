# Generated by Django 5.0.7 on 2024-12-18 18:50

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
        ('users', '0006_org_logo_org_namespace_alter_org_extid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='namespace',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='service',
            name='app_name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='service',
            name='settings',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='service',
            name='status',
            field=models.CharField(choices=[('NEW', 'New'), ('DEPLOYING', 'Deploying'), ('DEPLOYING_FAILED', 'Deploying failed'), ('RUNNING', 'Running'), ('STOPPING', 'Stopping'), ('STOPPED', 'Stopped'), ('TO_UPGRADE', 'To upgrade'), ('UPGRADING', 'Upgrading'), ('UPGRADING_FAILED', 'Upgrading failed'), ('RESUMMING', 'Resumming'), ('CLEARING', 'Clearing'), ('DESTROYED', 'Destroyed'), ('BACKING_UP', 'Backing up')], default='NEW', max_length=150),
        ),
        migrations.AlterField(
            model_name='service',
            name='extid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, help_text='Automatically generated id for external identification of the service', unique=True, verbose_name='Ext ID'),
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('extid', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Automatically generated id for external identification of the template', unique=True, verbose_name='Ext ID')),
                ('pid', models.UUIDField(default=uuid.uuid4, editable=False, help_text='UUID for tracking of this template on the deployment platform', unique=True, verbose_name='Platform ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('template_settings', models.JSONField(blank=True, null=True)),
                ('chart_id', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name': 'template',
                'verbose_name_plural': 'templates',
                'ordering': ['name'],
                'indexes': [models.Index(fields=['extid'], name='services_te_extid_edb1a7_idx'), models.Index(fields=['pid'], name='services_te_pid_88ed63_idx')],
            },
        ),
        migrations.CreateModel(
            name='TemplateSKU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField(blank=True, null=True)),
                ('ui_enabled', models.BooleanField(default=True)),
                ('extid', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Automatically generated id for external identification of the template sku', unique=True, verbose_name='Ext ID')),
                ('pid', models.UUIDField(default=uuid.uuid4, editable=False, help_text='UUID for tracking of this template sku on the deployment platform', unique=True, verbose_name='Platform ID')),
                ('sku_settings', models.JSONField(blank=True, null=True)),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='templates', to='users.org')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='templates', to='services.region')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skus', to='services.template')),
            ],
            options={
                'verbose_name': 'template sku',
                'verbose_name_plural': 'template skus',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='service',
            name='template_sku',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='services', to='services.templatesku'),
        ),
        migrations.CreateModel(
            name='TemplateVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version_name', models.CharField(max_length=128)),
                ('helm_repo', models.CharField(max_length=256)),
                ('extid', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Automatically generated id for external identification of the template version', unique=True, verbose_name='Ext ID')),
                ('pid', models.UUIDField(default=uuid.uuid4, editable=False, help_text='UUID for tracking of this template version on the deployment platform', unique=True, verbose_name='Platform ID')),
                ('version_settings', models.JSONField(blank=True, null=True)),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='services.template')),
            ],
            options={
                'verbose_name': 'template version',
                'verbose_name_plural': 'template versions',
                'ordering': ['version_name'],
            },
        ),
        migrations.AddField(
            model_name='service',
            name='template_version',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='services', to='services.templateversion'),
        ),
        migrations.AddIndex(
            model_name='templatesku',
            index=models.Index(fields=['extid'], name='services_te_extid_3f5b99_idx'),
        ),
        migrations.AddIndex(
            model_name='templatesku',
            index=models.Index(fields=['pid'], name='services_te_pid_8d82f2_idx'),
        ),
        migrations.AddIndex(
            model_name='templateversion',
            index=models.Index(fields=['extid'], name='services_te_extid_fad309_idx'),
        ),
        migrations.AddIndex(
            model_name='templateversion',
            index=models.Index(fields=['pid'], name='services_te_pid_e66db2_idx'),
        ),
    ]