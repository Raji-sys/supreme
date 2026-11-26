"""Shared fixtures for the test suite.

Run everything with:   venv/bin/python manage.py test results --debug-mode
(--debug-mode because the server runs with DEBUG=True, and django_fastdev
then turns any missing template variable into an error - the tests should
see what the lab sees.)
"""
from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase

from results.models import (
    AsoTitre, BloodCulture, BloodGlucose, BloodGroup, BoneChemistry, CerebroSpinalFluid, CRP,
    FBC, FBC2, GenericTest, Genotype, GramStain, HCV, HIVScreening, HPB, HVS, LipidProfile,
    LiverFunction, Mantoux, MiscellaneousChempathTests, OccultBlood, Patient, Pregnancy, Profile,
    RheumatoidFactor, SemenAnalysis, SerumProteins, SputumMCS, Stool, Swab_Pus_Aspirate_MCS,
    Testinfo, UreaAndElectrolyte, Urinalysis, UrineMicroscopy, VDRL, Widal, ZNStain,
)

User = get_user_model()

# The catalogue exactly as it is on the lab server (26 Nov 2026): lab, name, price.
# The create views look rows up BY NAME, so these names are part of the contract.
LIVE_CATALOGUE = [
    ('Chemical Pathology', 'BLOOD GLUCOSE', 2000), ('Chemical Pathology', 'Bone Chemistry', 3000),
    ('Chemical Pathology', 'Cerebro Spinal Fluid', 2000), ('Chemical Pathology', 'Lipid Profile', 5000),
    ('Chemical Pathology', 'Liver Function', 5000), ('Chemical Pathology', 'Miscellaneous Chempath Tests', 2000),
    ('Chemical Pathology', 'Serum Proteins', 2000), ('Chemical Pathology', 'Urea & Electrolyte', 5000),
    ('Chemical Pathology', 'URIC ACID', 2000),
    ('Hematology', 'Blood Group', 1500), ('Hematology', 'Full Blood Count', 3000),
    ('Hematology', 'Full Blood Count 2', 3000), ('Hematology', 'Genotype', 2000), ('Hematology', 'PCV', 1500),
    ('Microbiology', 'Blood Culture', 7000), ('Microbiology', 'Gram Stain', 1500), ('Microbiology', 'HVS MCS', 3000),
    ('Microbiology', 'Occult Blood', 2000), ('Microbiology', 'PREGNANCY TEST', 1500),
    ('Microbiology', 'Semen Analysis', 7000), ('Microbiology', 'Sputum MCS', 3000), ('Microbiology', 'Stool MCS', 3000),
    ('Microbiology', 'SWAB PUS ASPIRATE (MCS)', 3000), ('Microbiology', 'Urinalysis', 1500),
    ('Microbiology', 'Urine MCS', 3000), ('Microbiology', 'ZN Stain', 3000),
    ('Serology', 'Aso Titre', 2000), ('Serology', 'CRP', 2000), ('Serology', 'Hepatitis B', 2000),
    ('Serology', 'Hepatitis C', 2000), ('Serology', 'HEPATITIS COMBO', 6000), ('Serology', 'HIV Screening', 2000),
    ('Serology', 'H. PYLORI', 2000), ('Serology', 'Mantoux', 3000), ('Serology', 'MP/Widal', 3000),
    ('Serology', 'Rheumatoid Factor', 2000), ('Serology', 'VDRL', 2000),
]

# Every test type that is requested from the patient folder:
#   (url stem -> create_<stem> / update_<stem>, catalogue name, lab, model, Testinfo related_name)
LAB_TESTS = [
    ('blood_group', 'Blood Group', 'Hematology', BloodGroup, 'bg_test'),
    ('genotype', 'Genotype', 'Hematology', Genotype, 'gt_test'),
    ('fbc', 'Full Blood Count', 'Hematology', FBC, 'fbc_test'),
    ('fbc2', 'Full Blood Count 2', 'Hematology', FBC2, 'fbc2_test'),
    ('urea_electrolyte', 'Urea & Electrolyte', 'Chemical Pathology', UreaAndElectrolyte, 'ue_test'),
    ('liver_function', 'Liver Function', 'Chemical Pathology', LiverFunction, 'lf_test'),
    ('lipid_profile', 'Lipid Profile', 'Chemical Pathology', LipidProfile, 'lp_test'),
    ('blood_glucose', 'BLOOD GLUCOSE', 'Chemical Pathology', BloodGlucose, 'bgl_test'),
    ('serum_proteins', 'Serum Proteins', 'Chemical Pathology', SerumProteins, 'sp_test'),
    ('bone_chemistry', 'Bone Chemistry', 'Chemical Pathology', BoneChemistry, 'bc_test'),
    ('cerebro_spinal_fluid', 'Cerebro Spinal Fluid', 'Chemical Pathology', CerebroSpinalFluid, 'csf_test'),
    ('miscellaneous_chempath_tests', 'Miscellaneous Chempath Tests', 'Chemical Pathology', MiscellaneousChempathTests, 'misc_test'),
    ('widal', 'MP/Widal', 'Serology', Widal, 'widal_test'),
    ('rheumatoid_factor', 'Rheumatoid Factor', 'Serology', RheumatoidFactor, 'rheumatoid_factor_test'),
    ('hpb', 'Hepatitis B', 'Serology', HPB, 'hpb_test'),
    ('hcv', 'Hepatitis C', 'Serology', HCV, 'hcv_test'),
    ('vdrl', 'VDRL', 'Serology', VDRL, 'vdrl_test'),
    ('mantoux', 'Mantoux', 'Serology', Mantoux, 'mantoux_test'),
    ('aso_titre', 'Aso Titre', 'Serology', AsoTitre, 'aso_titre_test'),
    ('crp', 'CRP', 'Serology', CRP, 'crp_test'),
    ('hiv_screening', 'HIV Screening', 'Serology', HIVScreening, 'hiv_test'),
    ('urine_microscopy', 'Urine MCS', 'Microbiology', UrineMicroscopy, 'urine_test'),
    ('hvs', 'HVS MCS', 'Microbiology', HVS, 'hvs_test'),
    ('stool', 'Stool MCS', 'Microbiology', Stool, 'stool_test'),
    ('blood_culture', 'Blood Culture', 'Microbiology', BloodCulture, 'blood_culture_test'),
    ('occult_blood', 'Occult Blood', 'Microbiology', OccultBlood, 'occult_blood_test'),
    ('sputum_mcs', 'Sputum MCS', 'Microbiology', SputumMCS, 'sputum_mcs_test'),
    ('swab_pus_aspirate_mcs', 'SWAB PUS ASPIRATE (MCS)', 'Microbiology', Swab_Pus_Aspirate_MCS, 'swab_pus_aspirate_test'),
    ('gram_stain', 'Gram Stain', 'Microbiology', GramStain, 'gram_stain_test'),
    ('zn_stain', 'ZN Stain', 'Microbiology', ZNStain, 'zn_stain_test'),
    ('semen_analysis', 'Semen Analysis', 'Microbiology', SemenAnalysis, 'semen_analysis_test'),
    ('urinalysis', 'Urinalysis', 'Microbiology', Urinalysis, 'urinalysis_test'),
    ('pregnancy_test', 'PREGNANCY TEST', 'Microbiology', Pregnancy, 'pregnancy_test'),
]

# Per lab: (pending-requests page, finished-results page, cashier's payment list)
LAB_PAGES = {
    'Hematology': ('hematology_request', 'hematology_list', 'hema_pay_list'),
    'Chemical Pathology': ('chempath_request', 'chempath_list', 'chempath_pay_list'),
    'Microbiology': ('micro_request', 'micro_list', 'micro_pay_list'),
    'Serology': ('serology_request', 'serology_list', 'serology_pay_list'),
}


def make_catalogue():
    # update_or_create: migration 0062 has already added 'Full Blood Count 2'
    for lab, name, price in LIVE_CATALOGUE:
        GenericTest.objects.update_or_create(name=name, defaults={'lab': lab, 'price': price})


def make_staff(username='daniel', password='lab-pass-123'):
    user = User.objects.create_user(username=username, password=password,
                                    first_name='Daniel', last_name='Ordia')
    Profile.objects.create(user=user, department='HEMATOLOGY', cadre='SCIENTIST')
    return user


def make_patient(n=1, **extra):
    data = dict(surname='ABUBAKAR', other_names=f'ALH {n}', gender='MALE', age='ADULT',
                phone=f'0803000{n:04d}', hospital_clinic='PRIVATE')
    data.update(extra)
    return Patient.objects.create(**data)


def make_lab_test(patient, user, stem):
    """A requested-but-not-done test, built the way the create views build it."""
    from results.models import Paypoint
    _, name, _lab, model, _rel = next(t for t in LAB_TESTS if t[0] == stem)
    generic = GenericTest.objects.get(name__iexact=name)
    payment = Paypoint.objects.create(patient=patient, status=False, unit=generic.lab,
                                      service=generic.name, price=generic.price)
    info = Testinfo.objects.create(patient=patient, collected_by=user, payment=payment)
    model.objects.create(test=generic, test_info=info)
    return info


def valid_post_data(form):
    """A value every field of this form accepts - what a careful member of
    staff would type. Checkboxes are left unticked."""
    data = {}
    for name, field in form.fields.items():
        if isinstance(field, forms.BooleanField):
            continue
        if isinstance(field, forms.ChoiceField):
            choices = [value for value, _label in field.choices if value not in ('', None)]
            if choices:
                data[name] = str(getattr(choices[0], 'value', choices[0]))
        elif isinstance(field, (forms.IntegerField, forms.DecimalField, forms.FloatField)):
            data[name] = '1'
        elif isinstance(field, forms.DateField):
            data[name] = '2026-01-15'
        else:
            limit = getattr(field, 'max_length', None) or 10
            data[name] = '12'[:limit]
    return data


def start_ids_above_999():
    """Make every table hand out ids from 100,000 up, so the whole suite runs
    with the kind of numbers the live server has (and more): anything that
    breaks past 999 - a comma in a link, a fixed-width code - fails here."""
    from django.apps import apps
    from django.db import connection
    models = list(apps.get_app_config('results').get_models()) + [User]
    with connection.cursor() as cursor:
        for model in models:
            table = model._meta.db_table
            cursor.execute(
                f"SELECT setval(pg_get_serial_sequence(%s, 'id'), "
                f"GREATEST((SELECT COALESCE(MAX(id), 0) FROM \"{table}\") + 1, 100000), false)",
                [table])


class LabTestCase(TestCase):
    """Catalogue + one logged-in member of staff + one patient, ids >= 100,000."""

    @classmethod
    def setUpTestData(cls):
        start_ids_above_999()
        make_catalogue()
        cls.user = make_staff()
        cls.patient = make_patient()

    def setUp(self):
        self.client.force_login(self.user)

    def assertPdf(self, response, msg=''):
        self.assertEqual(response.status_code, 200, msg)
        self.assertEqual(response['Content-Type'], 'application/pdf', msg)
        self.assertTrue(response.content.startswith(b'%PDF'), msg)
