# Generated by Django 5.0.1 on 2024-10-17 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0026_bloodculture_ampicillin_bloodculture_augmentin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloodculture',
            name='result',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
