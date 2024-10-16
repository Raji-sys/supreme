# Generated by Django 5.0.1 on 2024-10-12 18:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0006_remove_bloodglucose_patient_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloodglucose',
            name='test_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bgl_test', to='results.testinfo'),
        ),
        migrations.AlterField(
            model_name='bloodgroup',
            name='test_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bg_test', to='results.testinfo'),
        ),
        migrations.AlterField(
            model_name='genotype',
            name='test_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gt_test', to='results.testinfo'),
        ),
        migrations.AlterField(
            model_name='lipidprofile',
            name='test_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lp_test', to='results.testinfo'),
        ),
        migrations.AlterField(
            model_name='liverfunction',
            name='test_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lf_test', to='results.testinfo'),
        ),
        migrations.AlterField(
            model_name='ureaandelectrolyte',
            name='test_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ue_test', to='results.testinfo'),
        ),
    ]
