# Generated by Django 5.1.5 on 2025-03-29 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_delete_authuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='department',
            field=models.CharField(blank=True, choices=[('DCIVIL', 'DCIVIL'), ('DMECH', 'DMECH'), ('DEEE', 'DEEE'), ('DECE', 'DECE'), ('DCSE', 'DCSE'), ('DMX', 'DMX'), ('DMT', 'DMT'), ('OTHERS', 'OTHERS')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(blank=True, choices=[('female', 'Female'), ('male', 'Male'), ('others', 'Others')], default='Female', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
