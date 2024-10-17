# Generated by Django 5.0.1 on 2024-10-17 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0023_remove_serumproteins_a_g_ratio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gramstain',
            name='antibiotic_sensitivity',
        ),
        migrations.RemoveField(
            model_name='znstain',
            name='antibiotic_sensitivity',
        ),
        migrations.RemoveField(
            model_name='urinemicroscopy',
            name='antibiotic_sensitivity',
        ),
        migrations.RemoveField(
            model_name='urinalysis',
            name='antibiotic_sensitivity',
        ),
        migrations.RemoveField(
            model_name='sputummcs',
            name='antibiotic_sensitivity',
        ),
        migrations.RemoveField(
            model_name='stool',
            name='antibiotic_sensitivity',
        ),
        migrations.RemoveField(
            model_name='occultblood',
            name='antibiotic_sensitivity',
        ),
        migrations.RemoveField(
            model_name='hvs',
            name='antibiotic_sensitivity',
        ),
        migrations.RemoveField(
            model_name='bloodculture',
            name='antibiotic_sensitivity',
        ),
        migrations.RemoveField(
            model_name='bloodculture',
            name='culture_yield',
        ),
        migrations.RemoveField(
            model_name='cultureyield',
            name='coliform',
        ),
        migrations.RemoveField(
            model_name='cultureyield',
            name='ecoli',
        ),
        migrations.RemoveField(
            model_name='cultureyield',
            name='no_growth',
        ),
        migrations.RemoveField(
            model_name='cultureyield',
            name='others',
        ),
        migrations.RemoveField(
            model_name='cultureyield',
            name='pseudomonas',
        ),
        migrations.RemoveField(
            model_name='cultureyield',
            name='staph_aureus',
        ),
        migrations.RemoveField(
            model_name='cultureyield',
            name='streptococcus',
        ),
        migrations.RemoveField(
            model_name='gramstain',
            name='culture_yield',
        ),
        migrations.RemoveField(
            model_name='hvs',
            name='culture_yield',
        ),
        migrations.RemoveField(
            model_name='occultblood',
            name='culture_yield',
        ),
        migrations.RemoveField(
            model_name='sputummcs',
            name='culture_yield',
        ),
        migrations.RemoveField(
            model_name='stool',
            name='culture_yield',
        ),
        migrations.RemoveField(
            model_name='urinalysis',
            name='culture_yield',
        ),
        migrations.RemoveField(
            model_name='urinemicroscopy',
            name='culture_yield',
        ),
        migrations.RemoveField(
            model_name='znstain',
            name='culture_yield',
        ),
        migrations.AddField(
            model_name='cultureyield',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='urinemicroscopy',
            name='ampicillin',
            field=models.CharField(blank=True, choices=[('1', '1 - Least Sensitive'), ('2', '2 - Moderately Sensitive'), ('3', '3 - Sensitive'), ('4', '4 - Highly Sensitive'), ('R', 'Resistant')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='urinemicroscopy',
            name='augmentin',
            field=models.CharField(blank=True, choices=[('1', '1 - Least Sensitive'), ('2', '2 - Moderately Sensitive'), ('3', '3 - Sensitive'), ('4', '4 - Highly Sensitive'), ('R', 'Resistant')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='urinemicroscopy',
            name='ceftazidime',
            field=models.CharField(blank=True, choices=[('1', '1 - Least Sensitive'), ('2', '2 - Moderately Sensitive'), ('3', '3 - Sensitive'), ('4', '4 - Highly Sensitive'), ('R', 'Resistant')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='urinemicroscopy',
            name='ceftriaxone',
            field=models.CharField(blank=True, choices=[('1', '1 - Least Sensitive'), ('2', '2 - Moderately Sensitive'), ('3', '3 - Sensitive'), ('4', '4 - Highly Sensitive'), ('R', 'Resistant')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='urinemicroscopy',
            name='cefuroxime',
            field=models.CharField(blank=True, choices=[('1', '1 - Least Sensitive'), ('2', '2 - Moderately Sensitive'), ('3', '3 - Sensitive'), ('4', '4 - Highly Sensitive'), ('R', 'Resistant')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='urinemicroscopy',
            name='cephalexin',
            field=models.CharField(blank=True, choices=[('1', '1 - Least Sensitive'), ('2', '2 - Moderately Sensitive'), ('3', '3 - Sensitive'), ('4', '4 - Highly Sensitive'), ('R', 'Resistant')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='urinemicroscopy',
            name='chloramphenicol',
            field=models.CharField(blank=True, choices=[('1', '1 - Least Sensitive'), ('2', '2 - Moderately Sensitive'), ('3', '3 - Sensitive'), ('4', '4 - Highly Sensitive'), ('R', 'Resistant')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='urinemicroscopy',
            name='ciprofloxacin',
            field=models.CharField(blank=True, choices=[('1', '1 - Least Sensitive'), ('2', '2 - Moderately Sensitive'), ('3', '3 - Sensitive'), ('4', '4 - Highly Sensitive'), ('R', 'Resistant')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='urinemicroscopy',
            name='cloxacillin',
            field=models.CharField(blank=True, choices=[('1', '1 - Least Sensitive'), ('2', '2 - Moderately Sensitive'), ('3', '3 - Sensitive'), ('4', '4 - Highly Sensitive'), ('R', 'Resistant')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='urinemicroscopy',
            name='cotrimoxazole',
            field=models.CharField(blank=True, choices=[('1', '1 - Least Sensitive'), ('2', '2 - Moderately Sensitive'), ('3', '3 - Sensitive'), ('4', '4 - Highly Sensitive'), ('R', 'Resistant')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='urinemicroscopy',
            name='culture_yields',
            field=models.ManyToManyField(blank=True, to='results.cultureyield'),
        ),
        migrations.AddField(
            model_name='urinemicroscopy',
            name='dalacin_c',
            field=models.CharField(blank=True, choices=[('1', '1 - Least Sensitive'), ('2', '2 - Moderately Sensitive'), ('3', '3 - Sensitive'), ('4', '4 - Highly Sensitive'), ('R', 'Resistant')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='urinemicroscopy',
            name='erythromycin',
            field=models.CharField(blank=True, choices=[('1', '1 - Least Sensitive'), ('2', '2 - Moderately Sensitive'), ('3', '3 - Sensitive'), ('4', '4 - Highly Sensitive'), ('R', 'Resistant')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='urinemicroscopy',
            name='flucloxacillin',
            field=models.CharField(blank=True, choices=[('1', '1 - Least Sensitive'), ('2', '2 - Moderately Sensitive'), ('3', '3 - Sensitive'), ('4', '4 - Highly Sensitive'), ('R', 'Resistant')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='urinemicroscopy',
            name='gentamycin',
            field=models.CharField(blank=True, choices=[('1', '1 - Least Sensitive'), ('2', '2 - Moderately Sensitive'), ('3', '3 - Sensitive'), ('4', '4 - Highly Sensitive'), ('R', 'Resistant')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='urinemicroscopy',
            name='lincomycin',
            field=models.CharField(blank=True, choices=[('1', '1 - Least Sensitive'), ('2', '2 - Moderately Sensitive'), ('3', '3 - Sensitive'), ('4', '4 - Highly Sensitive'), ('R', 'Resistant')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='urinemicroscopy',
            name='nalidixic_acid',
            field=models.CharField(blank=True, choices=[('1', '1 - Least Sensitive'), ('2', '2 - Moderately Sensitive'), ('3', '3 - Sensitive'), ('4', '4 - Highly Sensitive'), ('R', 'Resistant')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='urinemicroscopy',
            name='nitrofurantoin',
            field=models.CharField(blank=True, choices=[('1', '1 - Least Sensitive'), ('2', '2 - Moderately Sensitive'), ('3', '3 - Sensitive'), ('4', '4 - Highly Sensitive'), ('R', 'Resistant')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='urinemicroscopy',
            name='ofloxacin',
            field=models.CharField(blank=True, choices=[('1', '1 - Least Sensitive'), ('2', '2 - Moderately Sensitive'), ('3', '3 - Sensitive'), ('4', '4 - Highly Sensitive'), ('R', 'Resistant')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='urinemicroscopy',
            name='pefloxacin',
            field=models.CharField(blank=True, choices=[('1', '1 - Least Sensitive'), ('2', '2 - Moderately Sensitive'), ('3', '3 - Sensitive'), ('4', '4 - Highly Sensitive'), ('R', 'Resistant')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='urinemicroscopy',
            name='roxithromycin',
            field=models.CharField(blank=True, choices=[('1', '1 - Least Sensitive'), ('2', '2 - Moderately Sensitive'), ('3', '3 - Sensitive'), ('4', '4 - Highly Sensitive'), ('R', 'Resistant')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='urinemicroscopy',
            name='streptomycin',
            field=models.CharField(blank=True, choices=[('1', '1 - Least Sensitive'), ('2', '2 - Moderately Sensitive'), ('3', '3 - Sensitive'), ('4', '4 - Highly Sensitive'), ('R', 'Resistant')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='urinemicroscopy',
            name='tetracycline',
            field=models.CharField(blank=True, choices=[('1', '1 - Least Sensitive'), ('2', '2 - Moderately Sensitive'), ('3', '3 - Sensitive'), ('4', '4 - Highly Sensitive'), ('R', 'Resistant')], max_length=1, null=True),
        ),
        migrations.DeleteModel(
            name='AntibioticSensitivity',
        ),
    ]
