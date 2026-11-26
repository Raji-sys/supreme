"""Patients, payments/receipts, General tests, Ultrasound, letters, staff accounts."""
from django.contrib.auth import get_user_model
from django.urls import reverse

from results.models import GeneralTestResult, LetterMessage, Patient, Paypoint, Profile, Ultrasound
from .base import LabTestCase, make_lab_test, make_patient

User = get_user_model()

PATIENT_FORM = dict(surname='MUSA', other_names='AISHA', gender='FEMALE', age='ADULT',
                    phone='08031112222', hospital_clinic='PRIVATE')


class PatientTests(LabTestCase):

    def test_register_patient_gets_next_file_number(self):
        r = self.client.post(reverse('create_patient'), PATIENT_FORM)
        self.assertRedirects(r, reverse('patients_list'), fetch_redirect_response=False)
        new = Patient.objects.get(phone='08031112222')
        self.assertEqual(new.file_no, f'{int(self.patient.file_no) + 1:06d}')

    def test_age_accepts_numbers_words_and_months(self):
        for i, age in enumerate(['45', 'ADULT', 'CHILD', '6 MONTHS', 'AD']):
            with self.subTest(age=age):
                data = dict(PATIENT_FORM, phone=f'0809000000{i}', age=age)
                r = self.client.post(reverse('create_patient'), data)
                self.assertEqual(r.status_code, 302)
                self.assertEqual(Patient.objects.get(phone=data['phone']).age, age)

    def test_age_box_suggests_adult_and_child(self):
        r = self.client.get(reverse('create_patient'))
        self.assertContains(r, 'list="id_age_suggestions"')
        self.assertContains(r, '<option value="ADULT">', html=False)
        self.assertContains(r, '<option value="CHILD">', html=False)

    def test_duplicate_phone_is_a_form_error_not_a_crash(self):
        r = self.client.post(reverse('create_patient'), dict(PATIENT_FORM, phone=self.patient.phone))
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.context['form'].errors)

    def test_edit_patient(self):
        r = self.client.post(reverse('update_patient', args=[self.patient.pk]),
                             dict(PATIENT_FORM, phone=self.patient.phone, surname='CHANGED'))
        self.assertEqual(r.status_code, 302)
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.surname, 'CHANGED')

    def test_patient_list_search(self):
        make_patient(2, surname='ZAINAB')
        for q in ('ZAINAB', self.patient.file_no, self.patient.phone):
            with self.subTest(q=q):
                r = self.client.get(reverse('patients_list') + f'?q={q}')
                self.assertEqual(r.status_code, 200)
                self.assertGreaterEqual(r.context['search_count'], 1)

    def test_patient_folder_shows_every_department_tab(self):
        r = self.client.get(reverse('patient_details', args=[self.patient.file_no]))
        for tab in ('HEMATOLOGY', 'CHEMICAL PATHOLOGY', 'MICROBIOLOGY', 'SEROLOGY', 'GENERAL', 'ULTRASOUND',
                    'full blood count 1', 'full blood count 2'):
            self.assertContains(r, tab)

    def test_unknown_file_number_is_not_found_not_a_crash(self):
        self.assertEqual(self.client.get('/patient/999999/').status_code, 404)


class PaymentTests(LabTestCase):

    def test_mark_paid(self):
        info = make_lab_test(self.patient, self.user, 'genotype')
        self.client.post(reverse('update_pay', args=[info.payment.pk]), {'status': 'on'})
        info.payment.refresh_from_db()
        self.assertTrue(info.payment.status)

    def test_a_recorded_payment_cannot_be_unticked(self):
        """House rule (PayUpdateForm makes 'status' required): once the cashier
        has recorded a payment it cannot be reversed from this form."""
        info = make_lab_test(self.patient, self.user, 'genotype')
        url = reverse('update_pay', args=[info.payment.pk])
        self.client.post(url, {'status': 'on'})
        r = self.client.post(url, {})
        self.assertEqual(r.status_code, 200)
        info.payment.refresh_from_db()
        self.assertTrue(info.payment.status)

    def test_payment_returns_to_next_page(self):
        info = make_lab_test(self.patient, self.user, 'genotype')
        r = self.client.post(reverse('update_pay', args=[info.payment.pk]) + '?next=/revenue/hema-list/', {'status': 'on'})
        self.assertRedirects(r, '/revenue/hema-list/', fetch_redirect_response=False)

    def test_receipt_pdf(self):
        make_lab_test(self.patient, self.user, 'genotype')
        self.assertPdf(self.client.get(reverse('receipt_pdf') + f'?patient={self.patient.file_no}'))

    def test_all_transactions_page(self):
        make_lab_test(self.patient, self.user, 'genotype')
        self.assertContains(self.client.get(reverse('pay_list')), 'Genotype')


class ReportFilterTests(LabTestCase):

    def test_report_filters_do_not_crash(self):
        info = make_lab_test(self.patient, self.user, 'genotype')
        for query in (f'id={info.pk}', f'patient_no={self.patient.file_no}', 'collected=2026-01-15',
                      'test=Genotype', 'test=genotype', 'test=nothing-like-this'):
            with self.subTest(query=query):
                self.assertEqual(self.client.get(reverse('report') + '?' + query).status_code, 200)
                self.assertPdf(self.client.get(reverse('report_pdf') + '?' + query))

    def test_report_filter_by_test_name_finds_it(self):
        g = make_lab_test(self.patient, self.user, 'genotype')
        w = make_lab_test(self.patient, self.user, 'widal')
        found = list(self.client.get(reverse('report') + '?test=genotype').context['patient'])
        self.assertIn(g, found)
        self.assertNotIn(w, found)


class GeneralTestTests(LabTestCase):

    def test_general_test_request_result_and_pdf(self):
        p = self.patient
        r = self.client.post(reverse('general_test', args=[p.file_no]),
                             {'test_1': 'ESR', 'test_2': 'H. PYLORI', 'price': '2500'})
        self.assertRedirects(r, reverse('patient_details', args=[p.file_no]), fetch_redirect_response=False)
        g = GeneralTestResult.objects.get(patient=p)
        self.assertTrue(g.result_code.startswith('GEN'))
        self.assertIsNotNone(g.payment)
        self.assertEqual(g.payment.price, 2500)

        self.assertContains(self.client.get(reverse('general_request')), p.surname)
        r = self.client.post(reverse('general_result', args=[p.file_no, g.pk]),
                             {'test_1': 'ESR', 'result_1': '12 mm/hr', 'reference_range_test_1a': '0-15', 'cleared': 'on'})
        self.assertEqual(r.status_code, 302)
        g.refresh_from_db()
        self.assertEqual(g.result_1, '12 mm/hr')
        self.assertEqual(g.updated_by, self.user)

        self.assertEqual(self.client.get(reverse('general_report') + f'?id={g.pk}').status_code, 200)
        self.assertPdf(self.client.get(reverse('general_report_pdf') + f'?id={g.pk}'))
        self.assertEqual(self.client.get(reverse('patient_details', args=[p.file_no])).status_code, 200)


class UltrasoundTests(LabTestCase):

    def test_ultrasound_request_result_and_pdf(self):
        p = self.patient
        r = self.client.post(reverse('ultrasound_test', args=[p.file_no]), {'price': '5000'})
        self.assertEqual(r.status_code, 302)
        u = Ultrasound.objects.get(patient=p)
        self.assertTrue(u.result_code.startswith('ULTS'))
        r = self.client.post(reverse('ultrasound_result', args=[p.file_no, u.pk]),
                             {'result': 'Normal liver echotexture.', 'cleared': 'on'})
        self.assertEqual(r.status_code, 302)
        u.refresh_from_db()
        self.assertEqual(u.result, 'Normal liver echotexture.')
        self.assertPdf(self.client.get(reverse('ultrasound_report_pdf') + f'?id={u.result_code}'))

    def test_ultrasound_pdf_with_no_matches(self):
        """Was a crash until 26 Nov 2026 (code_str used before assignment)."""
        self.assertPdf(self.client.get(reverse('ultrasound_report_pdf') + '?id=NOPE'))

    def test_ultrasound_codes_continue_upwards(self):
        a = Ultrasound.objects.create(patient=self.patient, price=1)
        b = Ultrasound.objects.create(patient=self.patient, price=1)
        self.assertEqual(int(b.result_code[4:]), int(a.result_code[4:]) + 1)


class LetterTests(LabTestCase):

    def test_letter_create_edit_print_delete(self):
        r = self.client.post(reverse('message_create'), {'recipient_name': 'The MD', 'recipient_address': 'Kano',
                                                          'subject': 'Notice', 'content': 'Dear Sir'})
        self.assertRedirects(r, reverse('message_list'), fetch_redirect_response=False)
        m = LetterMessage.objects.get(subject='Notice')
        self.assertContains(self.client.get(reverse('message_list')), 'Notice')
        self.client.post(reverse('message_update', args=[m.pk]), {'subject': 'Updated', 'content': 'Dear Sir'})
        m.refresh_from_db()
        self.assertEqual(m.subject, 'Updated')
        self.assertPdf(self.client.get(reverse('letter_pdf', args=[m.pk])))
        self.client.post(reverse('message_delete', args=[m.pk]))
        self.assertFalse(LetterMessage.objects.filter(pk=m.pk).exists())


class StaffAccountTests(LabTestCase):

    def test_register_staff_creates_user_and_profile(self):
        r = self.client.post(reverse('create_profile'), {
            'username': 'amina', 'first_name': 'Amina', 'last_name': 'Bello',
            'password1': 'Str0ng-pass-2026', 'password2': 'Str0ng-pass-2026',
            'department': 'SEROLOGY', 'cadre': 'TECHNICIAN'})
        self.assertEqual(r.status_code, 302)
        u = User.objects.get(username='amina')
        self.assertEqual(u.profile.department, 'SEROLOGY')
        self.assertContains(self.client.get(reverse('profiles_list')), 'Amina Bello')

    def test_new_staff_can_log_in(self):
        self.client.post(reverse('create_profile'), {
            'username': 'amina', 'first_name': 'Amina', 'last_name': 'Bello',
            'password1': 'Str0ng-pass-2026', 'password2': 'Str0ng-pass-2026',
            'department': 'SEROLOGY', 'cadre': 'TECHNICIAN'})
        self.client.logout()
        self.assertTrue(self.client.login(username='amina', password='Str0ng-pass-2026'))

    def test_update_own_profile(self):
        r = self.client.post(reverse('profile-update', args=[self.user.profile.pk]),
                             {'username': 'daniel', 'first_name': 'Dan', 'last_name': 'Ordia',
                              'department': 'MICROBIOLOGY', 'cadre': 'SCIENTIST'})
        self.assertEqual(r.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Dan')
        self.assertEqual(self.user.profile.department, 'MICROBIOLOGY')

    def test_delete_staff(self):
        other = User.objects.create_user('temp', password='x')
        prof = Profile.objects.create(user=other)
        self.client.post(reverse('profile-delete', args=[prof.pk]))
        self.assertFalse(User.objects.filter(username='temp').exists())


class DepartmentReportFilterTests(LabTestCase):
    """The 'test' box on the General report searches all 15 test slots; the
    Ultrasound report has no such box. Both used to crash when typed in."""

    def test_general_report_test_box(self):
        a = GeneralTestResult.objects.create(patient=self.patient, test_1='ESR', test_3='H. PYLORI')
        b = GeneralTestResult.objects.create(patient=self.patient, test_1='WIDAL')
        found = list(self.client.get(reverse('general_report') + '?name=h. pylori').context['object_list'])
        self.assertIn(a, found)
        self.assertNotIn(b, found)
        self.assertPdf(self.client.get(reverse('general_report_pdf') + '?name=ESR'))

    def test_ultrasound_report_ignores_stray_name_param(self):
        self.assertEqual(self.client.get(reverse('ultrasound_report') + '?name=x').status_code, 200)
        self.assertPdf(self.client.get(reverse('ultrasound_report_pdf') + '?name=x'))


class ChempathRangeTests(LabTestCase):
    """Blood glucose ranges as the lab specified them (26 Nov 2026):
    FBS 3.0-6.0 mmol/L, RBS 3.0-7.0 mmol/L."""

    def printed(self, test_type):
        from django.template.loader import get_template
        info = make_lab_test(self.patient, self.user, 'blood_glucose')
        info.bgl_test.test_type, info.bgl_test.result = test_type, '5.0'
        info.bgl_test.save()
        return get_template('report_pdf.html').render({'f': [info], 'user': self.user, 'result': ''})

    def test_fasting_range(self):
        self.assertIn('3.0-6.0', self.printed('FASTING'))

    def test_random_range(self):
        html = self.printed('RANDOM')
        self.assertIn('3.0-7.0', html)
        self.assertNotIn('3.0-6.11', html)


class DashboardLayoutTests(LabTestCase):

    def test_dashboard_is_four_columns_and_does_not_stretch_edge_to_edge(self):
        r = self.client.get(reverse('dashboard'))
        self.assertContains(r, 'lg:grid-cols-4')
        self.assertContains(r, 'max-w-6xl mx-auto')
