# Generated by Django 5.0.7 on 2024-11-09 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_org_extid_user_extid'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='org',
            index=models.Index(fields=['extid'], name='users_org_extid_b761d6_idx'),
        ),
    ]