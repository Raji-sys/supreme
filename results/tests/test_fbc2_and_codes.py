"""FBC 2 specifics, and the auto-numbered codes (file numbers, SUP, GEN, ULTS)."""
import importlib

from django.apps import apps as django_apps
from django.urls import reverse

from results.forms import FBC2Form
from results.models import (FBC2, FBC2_PARAMETERS, GeneralTestResult, GenericTest, Patient,
                            Testinfo, next_serial)
from .base import LabTestCase, make_lab_test, make_patient

PHOTO_VALUES = dict(wbc='5.5', lymph_count='2.0', mid_count='0.5', gran_count='3.0', lymph_pct='36.9',
                    mid_pct='9.6', gran_pct='53.5', hgb='12.5', rbc='4.80', hct='38.1', mcv='79.4',
                    mch='26.0', mchc='32.8', rdw_cv='13.9', rdw_sd='36.0', plt='429', mpv='9.7',
                    pdw='15.3', pct='0.416')


class FBC2Tests(LabTestCase):

    def test_parameters_match_the_analyser_printout(self):
        self.assertEqual([p[1] for p in FBC2_PARAMETERS],
                         ['WBC', 'Lymph#', 'Mid#', 'Gran#', 'Lymph%', 'Mid%', 'Gran%', 'HGB', 'RBC', 'HCT',
                          'MCV', 'MCH', 'MCHC', 'RDW-CV', 'RDW-SD', 'PLT', 'MPV', 'PDW', 'PCT'])
        for field, label, unit, low, high in FBC2_PARAMETERS:
            with self.subTest(label):
                self.assertLess(float(low), float(high))
                FBC2._meta.get_field(field)  # every parameter has a column

    def test_flags_on_the_sample_printout(self):
        f = FBC2(**PHOTO_VALUES)
        flags = {r['label']: r['flag'] for r in f.rows() if r['flag']}
        self.assertEqual(flags, {'MCV': 'L', 'MCH': 'L', 'PLT': 'H', 'PCT': 'H'})

    def test_values_on_the_limits_are_not_flagged(self):
        f = FBC2(wbc='4.0', plt='400')
        self.assertEqual([r['flag'] for r in f.rows()], ['', ''])

    def test_free_text_is_shown_but_never_flagged(self):
        r = FBC2(wbc='<0.1').rows()[0]
        self.assertEqual((r['value'], r['flag']), ('<0.1', ''))

    def test_units_for_screen_and_pdf(self):
        r = FBC2(wbc='5').rows()[0]
        self.assertEqual(r['unit'], 'x10⁹/L')
        self.assertEqual(r['unit_html'], 'x10<sup>9</sup>/L')
        self.assertEqual(FBC2(rbc='4').rows()[0]['unit_html'], 'x10<sup>12</sup>/L')

    def test_folder_lists_only_entered_values_pdf_lists_all(self):
        f = FBC2(wbc='5')
        self.assertEqual(len(f.rows()), 1)
        self.assertEqual(len(f.all_rows()), 19)
        self.assertEqual(f.all_rows()[1]['value'], '')

    def test_form_shows_units_and_ranges(self):
        form = FBC2Form()
        self.assertEqual(form.fields['wbc'].label, 'WBC (x10⁹/L)')
        self.assertEqual(form.fields['pct'].help_text, 'Ref: 0.108 - 0.282')
        self.assertEqual(form.fields['pdw'].label, 'PDW')

    def test_unentered_report_prints_blank_sheet(self):
        info = make_lab_test(self.patient, self.user, 'fbc2')
        r = self.client.get(reverse('report_pdf') + f'?id={info.pk}')
        self.assertPdf(r)

    def test_folder_shows_flags_and_awaiting(self):
        info = make_lab_test(self.patient, self.user, 'fbc2')
        folder = reverse('patient_details', args=[self.patient.file_no])
        self.assertContains(self.client.get(folder), 'awaiting result')
        self.client.post(reverse('update_fbc2', args=[self.patient.file_no, info.pk]),
                         dict(PHOTO_VALUES, nature_of_specimen='BLOOD'))
        r = self.client.get(folder)
        self.assertContains(r, '79.4 L')
        self.assertContains(r, '429 H')

    def test_catalogue_migration_copies_fbc1_price_and_never_overwrites(self):
        mig = importlib.import_module('results.migrations.0062_fbc2_catalogue_entry')
        GenericTest.objects.filter(name='Full Blood Count 2').update(name='parked')
        mig.add_fbc2_test(django_apps, None)
        new = GenericTest.objects.get(name='Full Blood Count 2')
        self.assertEqual((new.lab, new.price), ('Hematology', 3000))
        new.price = 3500
        new.save()
        mig.add_fbc2_test(django_apps, None)
        self.assertEqual(GenericTest.objects.get(name='Full Blood Count 2').price, 3500)


class CodeNumberingTests(LabTestCase):
    """Codes are text, so 'GEN1000' sorts before 'GEN999'. These pin down that
    numbering keeps counting up past 999 / 9999 instead of colliding."""

    def test_general_codes_continue_past_999(self):
        GeneralTestResult.objects.create(patient=self.patient, test_1='X', result_code='GEN998')
        GeneralTestResult.objects.create(patient=self.patient, test_1='X', result_code='GEN999')
        a = GeneralTestResult.objects.create(patient=self.patient, test_1='X')
        b = GeneralTestResult.objects.create(patient=self.patient, test_1='X')
        self.assertEqual((a.result_code, b.result_code), ('GEN1000', 'GEN1001'))

    def test_general_codes_normal_increment(self):
        GeneralTestResult.objects.create(patient=self.patient, test_1='X', result_code='GEN723')
        self.assertEqual(GeneralTestResult.objects.create(patient=self.patient, test_1='X').result_code, 'GEN724')

    def test_first_general_code(self):
        self.assertEqual(GeneralTestResult.objects.create(patient=self.patient, test_1='X').result_code, 'GEN001')

    def test_request_codes_continue_past_9999(self):
        Testinfo.objects.create(patient=self.patient, code='SUP9999')
        a = Testinfo.objects.create(patient=self.patient)
        b = Testinfo.objects.create(patient=self.patient)
        self.assertEqual((a.code, b.code), ('SUP10000', 'SUP10001'))

    def test_request_codes_normal_increment(self):
        Testinfo.objects.create(patient=self.patient, code='SUP2917')
        self.assertEqual(Testinfo.objects.create(patient=self.patient).code, 'SUP2918')

    def test_requests_through_the_folder_get_distinct_codes(self):
        Testinfo.objects.create(patient=self.patient, code='SUP9999')
        for stem in ('genotype', 'widal', 'crp'):
            self.client.get(reverse(f'create_{stem}', args=[self.patient.file_no]))
        codes = list(Testinfo.objects.order_by('id').values_list('code', flat=True))
        self.assertEqual(codes[-3:], ['SUP10000', 'SUP10001', 'SUP10002'])

    def test_next_serial_ignores_odd_codes(self):
        Testinfo.objects.create(patient=self.patient, code='SUP0007')
        Testinfo.objects.create(patient=self.patient, code='SUPX')
        self.assertEqual(next_serial(Testinfo, 'code', 'SUP', 4), 'SUP0008')

    def test_patient_file_numbers(self):
        a = make_patient(2)
        b = make_patient(3)
        self.assertEqual(int(b.file_no), int(a.file_no) + 1)
        self.assertEqual(len(b.file_no), 6)
        self.assertTrue(Patient.objects.filter(file_no='000001').exists())


class CatalogueCheckTests(LabTestCase):
    """manage.py check_catalogue - run on the server by deploy.sh."""

    def test_finds_every_request_view(self):
        from results.management.commands.check_catalogue import required_test_names
        from .base import LAB_TESTS
        self.assertEqual({n.lower() for n in required_test_names()}, {t[1].lower() for t in LAB_TESTS})

    def test_passes_on_the_live_catalogue(self):
        from django.core.management import call_command
        call_command('check_catalogue', stdout=open('/dev/null', 'w'))

    def test_fails_when_a_test_is_renamed_in_admin(self):
        from django.core.management import call_command
        from django.core.management.base import CommandError
        GenericTest.objects.filter(name='Genotype').update(name='Genotype (new)')
        with self.assertRaisesMessage(CommandError, "'Genotype'"):
            call_command('check_catalogue', stdout=open('/dev/null', 'w'))
