"""Numbers past 999.

settings.USE_THOUSAND_SEPARATOR is True (so prices read ₦3,000), which means
Django prints ANY number >= 1000 with a comma. Inside a link or form value
that breaks things: '?page=1,000' is a 404, '?id=2,610' matched nothing.
These tests keep it that way fixed - including in templates written later.
"""
import re
from pathlib import Path

from django.urls import reverse

from results.models import Paypoint, Testinfo
from .base import LabTestCase, make_lab_test

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = sorted(list((ROOT / 'results/templates').rglob('*.html')) + list((ROOT / 'theme/templates').rglob('*.html')))

# {{ ... }} inside an attribute that ends up in a URL or is submitted back
IN_ATTRIBUTE = re.compile(r'\b(href|src|action|value|data-[\w-]+)="([^"]*)"')
EXPRESSION = re.compile(r'\{\{\s*(.*?)\s*\}\}')
# expressions that are, or may be, numbers
NUMERIC = re.compile(r'(page_obj|paginator|\.id\b|\.pk\b|\bid\b|\bpk\b|count|number|price|amount|total)')
SAFE = ('stringformat', 'unlocalize', 'get_absolute_url', 'urlencode')


class TemplateLintTests(LabTestCase):

    def test_no_number_in_a_link_or_form_value_can_get_a_comma(self):
        problems = []
        for tpl in TEMPLATES:
            for lineno, line in enumerate(tpl.read_text().splitlines(), 1):
                for _attr, content in IN_ATTRIBUTE.findall(line):
                    for expr in EXPRESSION.findall(content):
                        if NUMERIC.search(expr) and not any(s in expr for s in SAFE):
                            problems.append(f'{tpl.relative_to(ROOT)}:{lineno}  {{{{ {expr} }}}}')
        self.assertEqual(problems, [], "\nNumbers in links/values need |stringformat:'d' (or |unlocalize), "
                                       "otherwise 1000+ prints as '1,000':\n  " + "\n  ".join(problems))


class PaginationPast999Tests(LabTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        # 10,010 payments = 1,001 pages at 10 per page
        Paypoint.objects.bulk_create(
            [Paypoint(patient=cls.patient, unit='Hematology', service='Genotype', price=2000) for _ in range(10_010)])

    def test_page_1000_and_its_links(self):
        r = self.client.get(reverse('pay_list') + '?page=1000')
        self.assertEqual(r.status_code, 200)
        links = re.findall(r'href="\?page=([^"]*)"', r.content.decode())
        # first, previous, next, last - all plain digits (1,001 pages in total)
        self.assertEqual(links, ['1', '999', '1001', '1001'], f'page links on page 1000: {links}')

    def test_following_next_from_page_1000_works(self):
        self.assertEqual(self.client.get(reverse('pay_list') + '?page=1001').status_code, 200)


class CodeSearchTests(LabTestCase):

    def test_code_with_or_without_comma_finds_the_test(self):
        info = make_lab_test(self.patient, self.user, 'genotype')
        self.assertGreaterEqual(info.pk, 100_000)        # suite-wide big ids are on
        for typed in (str(info.pk), f'{info.pk:,}', f' {info.pk} '):
            with self.subTest(typed=typed):
                found = list(self.client.get(reverse('report'), {'id': typed}).context['patient'])
                self.assertEqual(found, [info])
                self.assertPdf(self.client.get(reverse('report_pdf'), {'id': typed}))

    def test_nonsense_code_finds_nothing_without_error(self):
        make_lab_test(self.patient, self.user, 'genotype')
        r = self.client.get(reverse('report'), {'id': 'abc'})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(list(r.context['patient']), [])

    def test_printed_code_has_no_comma(self):
        info = make_lab_test(self.patient, self.user, 'genotype')
        from django.template.loader import get_template
        r = self.client.get(reverse('report_pdf'), {'id': info.pk})
        self.assertPdf(r)
        self.assertTrue(Testinfo.objects.filter(pk=info.pk).exists())
        self.assertNotIn(f'{info.pk:,}', get_template('report_pdf.html').render(
            {'f': [info], 'user': self.user, 'result': f'{info.pk}'}).split('<body>')[1][:400])
