# Generated by Django 5.1.5 on 2025-04-11 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_student_differently_abled_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='differently_abled',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='student',
            name='first_graduate',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='student',
            name='govt_school',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='student',
            name='hosteller',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='student',
            name='single_parent',
            field=models.CharField(max_length=5),
        ),
    ]
