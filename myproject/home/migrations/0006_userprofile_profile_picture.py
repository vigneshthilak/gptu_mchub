# Generated by Django 5.1.5 on 2025-04-05 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_userprofile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_pics/default-avatar.png', null=True, upload_to='profile_pics/'),
        ),
    ]
