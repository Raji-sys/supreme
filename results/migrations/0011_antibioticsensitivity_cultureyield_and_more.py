# Generated by Django 5.0.1 on 2024-10-13 15:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0010_alter_genotype_test_info_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AntibioticSensitivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('antibiotic_name', models.CharField(max_length=50)),
                ('sensitivity_1', models.BooleanField(default=False)),
                ('sensitivity_2', models.BooleanField(default=False)),
                ('sensitivity_3', models.BooleanField(default=False)),
                ('sensitivity_4', models.BooleanField(default=False)),
                ('resistance', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CultureYield',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_growth', models.BooleanField(default=False)),
                ('ecoli', models.BooleanField(default=False)),
                ('coliform', models.BooleanField(default=False)),
                ('staph_aureus', models.BooleanField(default=False)),
                ('pseudomonas', models.BooleanField(default=False)),
                ('streptococcus', models.BooleanField(default=False)),
                ('others', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='chemicalpathologyresult',
            name='collected_by',
        ),
        migrations.RemoveField(
            model_name='chemicalpathologyresult',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='chemicalpathologyresult',
            name='payment',
        ),
        migrations.RemoveField(
            model_name='chemicalpathologyresult',
            name='test',
        ),
        migrations.RemoveField(
            model_name='chemicalpathologyresult',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='hematologyresult',
            name='collected_by',
        ),
        migrations.RemoveField(
            model_name='hematologyresult',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='hematologyresult',
            name='payment',
        ),
        migrations.RemoveField(
            model_name='hematologyresult',
            name='test',
        ),
        migrations.RemoveField(
            model_name='hematologyresult',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='microbiologyresult',
            name='collected_by',
        ),
        migrations.RemoveField(
            model_name='microbiologyresult',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='microbiologyresult',
            name='payment',
        ),
        migrations.RemoveField(
            model_name='microbiologyresult',
            name='test',
        ),
        migrations.RemoveField(
            model_name='microbiologyresult',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='serologyresult',
            name='collected_by',
        ),
        migrations.RemoveField(
            model_name='serologyresult',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='serologyresult',
            name='payment',
        ),
        migrations.RemoveField(
            model_name='serologyresult',
            name='test',
        ),
        migrations.RemoveField(
            model_name='serologyresult',
            name='updated_by',
        ),
        migrations.AlterField(
            model_name='bloodgroup',
            name='result',
            field=models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='genotype',
            name='result',
            field=models.CharField(choices=[('AA', 'AA'), ('AS', 'AS'), ('SS', 'SS'), ('AC', 'AC'), ('SC', 'SC')], max_length=2, null=True),
        ),
        migrations.CreateModel(
            name='AsoTitre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(blank=True, max_length=10, null=True)),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='results.generictest')),
                ('test_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='aso_titre_test', to='results.testinfo')),
            ],
        ),
        migrations.CreateModel(
            name='BoneChemistry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alkaline_phosphatase', models.DecimalField(decimal_places=2, help_text='Alkaline Phosphatase (U/L)', max_digits=5, null=True)),
                ('calcium', models.DecimalField(decimal_places=2, help_text='Calcium (mmol/L)', max_digits=4, null=True)),
                ('inorganic_phosphate', models.DecimalField(decimal_places=2, help_text='Inorganic Phosphate (mmol/L)', max_digits=4, null=True)),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='results.generictest')),
                ('test_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bc_test', to='results.testinfo')),
            ],
        ),
        migrations.CreateModel(
            name='CerebroSpinalFluid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('csf_glucose', models.DecimalField(decimal_places=2, help_text='CSF Glucose (mmol/L)', max_digits=5, null=True)),
                ('csf_protein', models.DecimalField(decimal_places=2, help_text='CSF Protein (mg/dL)', max_digits=5, null=True)),
                ('csf_chloride', models.DecimalField(decimal_places=2, help_text='CSF Chloride (mmol/L)', max_digits=5, null=True)),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='results.generictest')),
                ('test_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cp_test', to='results.testinfo')),
            ],
        ),
        migrations.CreateModel(
            name='CRP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(blank=True, max_length=10, null=True)),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='results.generictest')),
                ('test_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='crp_test', to='results.testinfo')),
            ],
        ),
        migrations.CreateModel(
            name='BloodCulture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('antibiotic_sensitivity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='results.antibioticsensitivity')),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='results.generictest')),
                ('test_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blood_culture_test', to='results.testinfo')),
                ('culture_yield', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='results.cultureyield')),
            ],
        ),
        migrations.CreateModel(
            name='FBC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hb', models.DecimalField(decimal_places=2, max_digits=5)),
                ('pcv', models.DecimalField(decimal_places=2, max_digits=5)),
                ('mchc', models.DecimalField(decimal_places=2, max_digits=5)),
                ('rbc', models.DecimalField(decimal_places=2, max_digits=5)),
                ('mch', models.DecimalField(decimal_places=2, max_digits=5)),
                ('mcv', models.DecimalField(decimal_places=2, max_digits=5)),
                ('retic', models.DecimalField(decimal_places=2, max_digits=5)),
                ('retic_index', models.DecimalField(decimal_places=2, max_digits=5)),
                ('platelets', models.DecimalField(decimal_places=2, max_digits=6)),
                ('wbc', models.DecimalField(decimal_places=2, max_digits=6)),
                ('esr', models.DecimalField(decimal_places=2, max_digits=6)),
                ('sickle_cells', models.BooleanField(default=False)),
                ('hypochromia', models.BooleanField(default=False)),
                ('polychromasia', models.BooleanField(default=False)),
                ('nucleated_rbc', models.BooleanField(default=False)),
                ('anisocytosis', models.BooleanField(default=False)),
                ('macrocytosis', models.BooleanField(default=False)),
                ('microcytosis', models.BooleanField(default=False)),
                ('poikilocytosis', models.BooleanField(default=False)),
                ('target_cells', models.BooleanField(default=False)),
                ('neutrophils', models.DecimalField(decimal_places=2, max_digits=5)),
                ('eosinophils', models.DecimalField(decimal_places=2, max_digits=5)),
                ('basophils', models.DecimalField(decimal_places=2, max_digits=5)),
                ('trans_lymph', models.DecimalField(decimal_places=2, max_digits=5)),
                ('lymphocytes', models.DecimalField(decimal_places=2, max_digits=5)),
                ('monocytes', models.DecimalField(decimal_places=2, max_digits=5)),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='results.generictest')),
                ('test_info', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fbc_test', to='results.testinfo')),
            ],
        ),
        migrations.CreateModel(
            name='GramStain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('urine', models.BooleanField(default=False)),
                ('hvs', models.BooleanField(default=False, verbose_name='High Vaginal Swab')),
                ('swab', models.BooleanField(default=False)),
                ('pus', models.BooleanField(default=False)),
                ('aspirate', models.BooleanField(default=False)),
                ('sputum', models.BooleanField(default=False)),
                ('gram_positive_cocci', models.BooleanField(default=False)),
                ('gram_negative_cocci', models.BooleanField(default=False)),
                ('gram_positive_rods', models.BooleanField(default=False)),
                ('gram_negative_rods', models.BooleanField(default=False)),
                ('gram_positive_clusters', models.BooleanField(default=False)),
                ('gram_negative_clusters', models.BooleanField(default=False)),
                ('gram_positive_chains', models.BooleanField(default=False)),
                ('gram_negative_chains', models.BooleanField(default=False)),
                ('other_findings', models.TextField(blank=True, null=True)),
                ('antibiotic_sensitivity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='results.antibioticsensitivity')),
                ('culture_yield', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='results.cultureyield')),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='results.generictest')),
                ('test_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gram_stain_test', to='results.testinfo')),
            ],
        ),
        migrations.CreateModel(
            name='HepatitisB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(blank=True, max_length=10, null=True)),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='results.generictest')),
                ('test_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hpb_test', to='results.testinfo')),
            ],
        ),
        migrations.CreateModel(
            name='HepatitisC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(blank=True, max_length=10, null=True)),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='results.generictest')),
                ('test_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hcv_test', to='results.testinfo')),
            ],
        ),
        migrations.CreateModel(
            name='HIVScreening',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(blank=True, max_length=10, null=True)),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='results.generictest')),
                ('test_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hiv_test', to='results.testinfo')),
            ],
        ),
        migrations.CreateModel(
            name='HVS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pus_cells', models.CharField(blank=True, max_length=50, null=True)),
                ('rbc', models.CharField(blank=True, max_length=50, null=True)),
                ('epithelial_cells', models.CharField(blank=True, max_length=50, null=True)),
                ('t_vaginalis', models.CharField(blank=True, max_length=50, null=True)),
                ('yeast_cells', models.CharField(blank=True, max_length=50, null=True)),
                ('antibiotic_sensitivity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='results.antibioticsensitivity')),
                ('culture_yield', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='results.cultureyield')),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='results.generictest')),
                ('test_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hvs_test', to='results.testinfo')),
            ],
        ),
        migrations.CreateModel(
            name='Mantoux',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(blank=True, max_length=10, null=True)),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='results.generictest')),
                ('test_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mantoux_test', to='results.testinfo')),
            ],
        ),
        migrations.CreateModel(
            name='MiscellaneousChempathTests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uric_acid', models.DecimalField(decimal_places=2, help_text='Uric Acid (umol/L)', max_digits=5, null=True)),
                ('serum_amylase', models.DecimalField(decimal_places=2, help_text='Serum Amylase (U/L)', max_digits=5, null=True)),
                ('acid_phosphatase_total', models.DecimalField(decimal_places=2, help_text='Acid Phosphatase Total (U/L)', max_digits=4, null=True)),
                ('acid_phosphatase_prostatic', models.DecimalField(decimal_places=2, help_text='Acid Phosphatase Prostatic (U/L)', max_digits=4, null=True)),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='results.generictest')),
                ('test_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='misc_test', to='results.testinfo')),
            ],
        ),
        migrations.CreateModel(
            name='OccultBlood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(choices=[('Pos', 'Positive'), ('Neg', 'Negative')], max_length=3)),
                ('antibiotic_sensitivity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='results.antibioticsensitivity')),
                ('culture_yield', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='results.cultureyield')),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='results.generictest')),
                ('test_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='occult_blood_test', to='results.testinfo')),
            ],
        ),
        migrations.CreateModel(
            name='PregnancyTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(choices=[('Pos', 'Positive'), ('Neg', 'Negative')], max_length=10, null=True)),
                ('method', models.CharField(choices=[('Urine', 'Urine Test'), ('Blood', 'Blood Test')], max_length=50, null=True)),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='results.generictest')),
                ('test_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pregnancy_test', to='results.testinfo')),
            ],
        ),
        migrations.CreateModel(
            name='RhesusFactorTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rhesus_d', models.CharField(choices=[('Positive', 'Positive'), ('Negative', 'Negative')], max_length=8, null=True)),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='results.generictest')),
                ('test_info', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rh_test', to='results.testinfo')),
            ],
        ),
        migrations.CreateModel(
            name='RheumatoidFactor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(blank=True, max_length=10, null=True)),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='results.generictest')),
                ('test_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rhematoid_factor_test', to='results.testinfo')),
            ],
        ),
        migrations.CreateModel(
            name='SemenAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_produced', models.TimeField()),
                ('time_examined', models.TimeField()),
                ('color', models.CharField(max_length=50)),
                ('volume', models.DecimalField(decimal_places=2, help_text='Volume (ml)', max_digits=5)),
                ('viscosity', models.CharField(max_length=50)),
                ('consistency', models.CharField(max_length=50)),
                ('motility_active', models.DecimalField(decimal_places=2, help_text='Active Motility (%)', max_digits=5)),
                ('motility_moderate', models.DecimalField(decimal_places=2, help_text='Moderate Motility (%)', max_digits=5)),
                ('motility_sluggish', models.DecimalField(decimal_places=2, help_text='Sluggish Motility (%)', max_digits=5)),
                ('morphology_normal', models.DecimalField(decimal_places=2, help_text='Normal Morphology (%)', max_digits=5)),
                ('morphology_abnormal', models.DecimalField(decimal_places=2, help_text='Abnormal Morphology (%)', max_digits=5)),
                ('morphology_sluggish', models.DecimalField(decimal_places=2, help_text='Sluggish Morphology (%)', max_digits=5)),
                ('total_sperm_count', models.DecimalField(decimal_places=2, help_text='Total Sperm Count (x10^6/ml)', max_digits=5)),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='results.generictest')),
                ('test_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='semen_analysis_test', to='results.testinfo')),
            ],
        ),
        migrations.CreateModel(
            name='SerumProteins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_protein', models.DecimalField(decimal_places=2, help_text='Total Protein (g/dL)', max_digits=4, null=True)),
                ('albumin', models.DecimalField(decimal_places=2, help_text='Albumin (g/dL)', max_digits=4, null=True)),
                ('globulin', models.DecimalField(decimal_places=2, help_text='Globulin (g/dL)', max_digits=4, null=True)),
                ('a_g_ratio', models.DecimalField(decimal_places=2, help_text='A/G Ratio', max_digits=3, null=True)),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='results.generictest')),
                ('test_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sp_test', to='results.testinfo')),
            ],
        ),
        migrations.CreateModel(
            name='SputumMCS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('antibiotic_sensitivity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='results.antibioticsensitivity')),
                ('culture_yield', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='results.cultureyield')),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='results.generictest')),
                ('test_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sputum_mcs_test', to='results.testinfo')),
            ],
        ),
        migrations.CreateModel(
            name='Stool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consistency', models.CharField(blank=True, max_length=50, null=True)),
                ('color', models.CharField(blank=True, max_length=50, null=True)),
                ('mucus', models.CharField(blank=True, max_length=50, null=True)),
                ('blood', models.CharField(blank=True, max_length=50, null=True)),
                ('ova', models.CharField(blank=True, max_length=50, null=True)),
                ('cyst', models.CharField(blank=True, max_length=50, null=True)),
                ('antibiotic_sensitivity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='results.antibioticsensitivity')),
                ('culture_yield', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='results.cultureyield')),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='results.generictest')),
                ('test_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stool_test', to='results.testinfo')),
            ],
        ),
        migrations.CreateModel(
            name='UrinalysisTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(blank=True, max_length=50, null=True)),
                ('appearance', models.CharField(blank=True, max_length=50, null=True)),
                ('specific_gravity', models.DecimalField(blank=True, decimal_places=3, max_digits=5, null=True)),
                ('ph', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('protein', models.CharField(blank=True, max_length=50, null=True)),
                ('glucose', models.CharField(blank=True, max_length=50, null=True)),
                ('ketones', models.CharField(blank=True, max_length=50, null=True)),
                ('bilirubin', models.CharField(blank=True, max_length=50, null=True)),
                ('urobilinogen', models.CharField(blank=True, max_length=50, null=True)),
                ('nitrites', models.CharField(blank=True, max_length=50, null=True)),
                ('leukocyte_esterase', models.CharField(blank=True, max_length=50, null=True)),
                ('blood', models.CharField(blank=True, max_length=50, null=True)),
                ('antibiotic_sensitivity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='results.antibioticsensitivity')),
                ('culture_yield', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='results.cultureyield')),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='results.generictest')),
                ('test_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='urinalysis_test', to='results.testinfo')),
            ],
        ),
        migrations.CreateModel(
            name='UrineMicroscopy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pus_cells', models.CharField(blank=True, max_length=50, null=True)),
                ('rbc', models.CharField(blank=True, max_length=50, null=True)),
                ('epithelial_cells', models.CharField(blank=True, max_length=50, null=True)),
                ('casts', models.CharField(blank=True, max_length=50, null=True)),
                ('crystals', models.CharField(blank=True, max_length=50, null=True)),
                ('ova', models.CharField(blank=True, max_length=50, null=True)),
                ('antibiotic_sensitivity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='results.antibioticsensitivity')),
                ('culture_yield', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='results.cultureyield')),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='results.generictest')),
                ('test_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='urine_test', to='results.testinfo')),
            ],
        ),
        migrations.CreateModel(
            name='VDRL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(blank=True, max_length=10, null=True)),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='results.generictest')),
                ('test_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vdrl_test', to='results.testinfo')),
            ],
        ),
        migrations.CreateModel(
            name='WidalTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('o_antigen_s_typhi_d', models.CharField(blank=True, max_length=10, null=True)),
                ('o_antigen_s_paratyphi_a', models.CharField(blank=True, max_length=10, null=True)),
                ('o_antigen_s_paratyphi_b', models.CharField(blank=True, max_length=10, null=True)),
                ('o_antigen_s_paratyphi_c', models.CharField(blank=True, max_length=10, null=True)),
                ('h_antigen_s_typhi_d', models.CharField(blank=True, max_length=10, null=True)),
                ('h_antigen_s_paratyphi_a', models.CharField(blank=True, max_length=10, null=True)),
                ('h_antigen_s_paratyphi_b', models.CharField(blank=True, max_length=10, null=True)),
                ('h_antigen_s_paratyphi_c', models.CharField(blank=True, max_length=10, null=True)),
                ('diagnostic_titre', models.CharField(blank=True, default='> 1/80', max_length=20, null=True)),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='results.generictest')),
                ('test_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='widal_test', to='results.testinfo')),
            ],
        ),
        migrations.CreateModel(
            name='ZNStain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_sample', models.CharField(blank=True, max_length=50, null=True)),
                ('second_sample', models.CharField(blank=True, max_length=50, null=True)),
                ('third_sample', models.CharField(blank=True, max_length=50, null=True)),
                ('antibiotic_sensitivity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='results.antibioticsensitivity')),
                ('culture_yield', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='results.cultureyield')),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='results.generictest')),
                ('test_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='zns_stain_test', to='results.testinfo')),
            ],
        ),
        migrations.DeleteModel(
            name='ChempathTest',
        ),
        migrations.DeleteModel(
            name='ChemicalPathologyResult',
        ),
        migrations.DeleteModel(
            name='HematologyTest',
        ),
        migrations.DeleteModel(
            name='HematologyResult',
        ),
        migrations.DeleteModel(
            name='MicrobiologyTest',
        ),
        migrations.DeleteModel(
            name='MicrobiologyResult',
        ),
        migrations.DeleteModel(
            name='SerologyTest',
        ),
        migrations.DeleteModel(
            name='SerologyResult',
        ),
    ]
