# Generated by Django 4.2.16 on 2024-10-01 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otp_app', '0006_rename_otp_validated_usermodel_otp_mode_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='otp_validate',
            field=models.BooleanField(default=False),
        ),
    ]
