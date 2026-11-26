"""The lab's daily workflow, for every test type requested from the patient folder:

    SEND REQUEST -> unpaid charge at the cashier -> appears in the lab's
    pending requests -> cashier marks it paid -> scientist enters results ->
    appears in the lab's results list -> prints as a PDF report.
"""
from django.urls import reverse
from django.utils.html import escape

from results.models import GenericTest, Paypoint, Testinfo
from .base import LAB_PAGES, LAB_TESTS, LabTestCase, make_lab_test, valid_post_data


class EveryTestTypeWorkflowTests(LabTestCase):

    def test_full_workflow_for_every_test_type(self):
        for stem, name, lab, model, related in LAB_TESTS:
            with self.subTest(test=name):
                self._run_workflow(stem, name, lab, model, related)

    def _run_workflow(self, stem, name, lab, model, related):
        p = self.patient
        request_page, results_page, pay_page = LAB_PAGES[lab]
        before = set(Testinfo.objects.values_list('id', flat=True))

        # 1. SEND REQUEST from the patient folder
        r = self.client.get(reverse(f'create_{stem}', args=[p.file_no]))
        self.assertRedirects(r, reverse('patient_details', args=[p.file_no]), fetch_redirect_response=False)
        new = Testinfo.objects.exclude(id__in=before)
        self.assertEqual(new.count(), 1, 'exactly one request is created')
        info = new.get()
        result = getattr(info, related)
        self.assertIsInstance(result, model)

        # 2. it raised an UNPAID charge at the catalogue price, under the right lab
        generic = GenericTest.objects.get(name__iexact=name)
        self.assertFalse(info.payment.status)
        self.assertEqual(info.payment.price, generic.price)
        self.assertEqual(info.payment.unit, lab)
        self.assertEqual(info.payment.service, generic.name)
        self.assertFalse(info.cleared)
        self.assertTrue(info.code.startswith('SUP'))

        # 3. the lab sees it as pending; the cashier sees the charge
        self.assertContains(self.client.get(reverse(request_page)), escape(generic.name))
        self.assertContains(self.client.get(reverse(pay_page)), escape(generic.name))

        # 4. cashier marks it paid
        r = self.client.post(reverse('update_pay', args=[info.payment.pk]), {'status': 'on'})
        self.assertEqual(r.status_code, 302)
        info.payment.refresh_from_db()
        self.assertTrue(info.payment.status)

        # 5. the result form opens EMPTY - results are typed in after the test is run.
        #    (A deliberate model default, such as Widal's '> 1/80' significance
        #    titre, is not a result and is allowed.)
        url = reverse(f'update_{stem}', args=[p.file_no, info.pk])
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        form = r.context['form']
        for field_name in form.fields:
            if field_name in ('nature_of_specimen', 'cleared'):
                continue
            allowed = [None, '', False]
            try:
                allowed.append(model._meta.get_field(field_name).get_default())
            except Exception:
                pass
            self.assertIn(form.initial.get(field_name), allowed,
                          f'{field_name} must not be pre-filled on a new request')

        # 6. scientist enters results
        data = valid_post_data(form)
        data['nature_of_specimen'] = 'BLOOD'
        r = self.client.post(url, data)
        if r.status_code != 302:
            self.fail(f'result form rejected: {r.context["form"].errors.as_text()}')
        self.assertRedirects(r, reverse('patient_details', args=[p.file_no]), fetch_redirect_response=False)
        info.refresh_from_db()
        result.refresh_from_db()
        self.assertTrue(info.cleared, 'saving a result clears the request')
        self.assertEqual(info.nature_of_specimen, 'BLOOD')
        for field_name, value in data.items():
            if hasattr(result, field_name) and not field_name.startswith('test'):
                self.assertEqual(str(getattr(result, field_name)), value, f'{field_name} was not saved')

        # 7. it moves from pending to the results list
        self.assertContains(self.client.get(reverse(results_page)), escape(generic.name))

        # 8. the patient folder still renders, with the result's edit link
        r = self.client.get(reverse('patient_details', args=[p.file_no]))
        self.assertContains(r, url)

        # 9. and it prints
        self.assertPdf(self.client.get(reverse('report_pdf') + f'?id={info.pk}'), f'{name} PDF')

    def test_request_for_a_test_missing_from_the_catalogue_fails_safely(self):
        """If someone renames or deletes a test in Admin, SEND REQUEST must not
        crash or create half a request - it shows an error and creates nothing."""
        GenericTest.objects.filter(name='Genotype').delete()
        before = (Paypoint.objects.count(), Testinfo.objects.count())
        r = self.client.get(reverse('create_genotype', args=[self.patient.file_no]), follow=True)
        self.assertEqual(r.status_code, 200)
        self.assertEqual((Paypoint.objects.count(), Testinfo.objects.count()), before)

    def test_editing_a_result_keeps_the_entered_values(self):
        info = make_lab_test(self.patient, self.user, 'genotype')
        url = reverse('update_genotype', args=[self.patient.file_no, info.pk])
        self.client.post(url, {'result': 'AS', 'nature_of_specimen': 'BLOOD'})
        r = self.client.get(url)
        self.assertEqual(r.context['form'].initial.get('result'), 'AS')

    def test_report_page_and_combined_pdf(self):
        a = make_lab_test(self.patient, self.user, 'genotype')
        b = make_lab_test(self.patient, self.user, 'widal')
        self.assertEqual(self.client.get(reverse('report')).status_code, 200)
        self.assertEqual(self.client.get(reverse('report') + f'?id={a.pk}').status_code, 200)
        # filtering by patient prints every test for that patient in one PDF
        self.assertPdf(self.client.get(reverse('report_pdf') + f'?patient_no={self.patient.file_no}'))
        self.assertTrue(b)
