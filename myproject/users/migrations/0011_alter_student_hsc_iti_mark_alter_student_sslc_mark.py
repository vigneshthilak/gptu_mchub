# Generated by Django 5.1.5 on 2025-03-16 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_student_differently_abled_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='hsc_iti_mark',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='sslc_mark',
            field=models.IntegerField(),
        ),
    ]
