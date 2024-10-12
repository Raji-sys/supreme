# Generated by Django 5.0.1 on 2024-10-12 20:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0009_alter_testinfo_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genotype',
            name='test_info',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gt_test', to='results.testinfo'),
        ),
        migrations.AlterField(
            model_name='ureaandelectrolyte',
            name='test_info',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ue_test', to='results.testinfo'),
        ),
    ]
