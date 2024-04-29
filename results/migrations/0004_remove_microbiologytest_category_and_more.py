# Generated by Django 5.0.1 on 2024-04-29 14:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0003_chempathtestname_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='microbiologytest',
            name='category',
        ),
        migrations.AlterField(
            model_name='serologyparameter',
            name='result',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='serology_parameters', to='results.serologytestresult'),
        ),
    ]
