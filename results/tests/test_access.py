"""Login protection, and 'no page crashes' for every route in the app."""
import re

from django.test import Client
from django.urls import URLPattern, reverse

from results import urls as results_urls
from results.models import GeneralTestResult, LetterMessage, Paypoint, Ultrasound
from .base import LAB_TESTS, LabTestCase, make_lab_test

# Routes known to fail, with the reason. Each entry must stay justified -
# test_known_broken_routes_stay_unreachable checks nothing links to them.
KNOWN_BROKEN = {
    # PayCreateView renders 'new_pay.html', which has never existed. No page
    # links here; payments are recorded through update_pay instead.
    'add_pay': 'template new_pay.html does not exist',
}

PUBLIC = {'login', 'logout'}


def all_routes():
    return [p for p in results_urls.urlpatterns if isinstance(p, URLPattern)]


class AccessTests(LabTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        p = cls.patient
        cls.infos = {stem: make_lab_test(p, cls.user, stem) for stem, *_ in LAB_TESTS}
        pay = Paypoint.objects.create(patient=p, unit='General', service='X', price=100)
        cls.general = GeneralTestResult.objects.create(patient=p, test_1='ESR', payment=pay, price=100)
        cls.ultrasound = Ultrasound.objects.create(patient=p, price=5000)
        cls.letter = LetterMessage.objects.create(subject='Notice', content='Hello')
        cls.payment = pay

    def url_for(self, pattern):
        """Fill a route's <args> with real objects from setUpTestData."""
        name, route = pattern.name, str(pattern.pattern)
        stem = re.sub(r'^(create|update)_', '', name or '')
        ids = {
            'update_patient': self.patient.pk, 'update_pay': self.payment.pk,
            'profile-update': self.user.profile.pk, 'profile-delete': self.user.profile.pk,
            'general_result': self.general.pk, 'ultrasound_result': self.ultrasound.pk,
            'message_update': self.letter.pk, 'letter_pdf': self.letter.pk, 'message_delete': self.letter.pk,
        }
        def fill(m):
            arg = m.group(2)
            if arg == 'file_no':
                return self.patient.file_no
            if arg == 'test_info_pk':
                return str(self.infos[stem].pk)
            return str(ids[name])
        return '/' + re.sub(r'<(?:(\w+):)?(\w+)>', fill, route)

    def test_every_page_requires_login(self):
        anon = Client()
        for pattern in all_routes():
            if pattern.name in PUBLIC:
                continue
            url = self.url_for(pattern)
            with self.subTest(route=pattern.name, url=url):
                r = anon.get(url)
                self.assertEqual(r.status_code, 302)
                self.assertTrue(r['Location'].startswith(reverse('login')), r['Location'])

    def test_no_page_crashes_for_logged_in_staff(self):
        client = Client(raise_request_exception=False)
        client.force_login(self.user)
        for pattern in all_routes():
            if pattern.name in KNOWN_BROKEN or pattern.name == 'logout':
                continue
            url = self.url_for(pattern)
            with self.subTest(route=pattern.name, url=url):
                r = client.get(url)
                self.assertLess(r.status_code, 500, f'{url} crashed')
                if r.status_code == 302:
                    self.assertFalse(r['Location'].startswith(reverse('login')), 'logged-in user bounced to login')

    def test_known_broken_routes_stay_unreachable(self):
        """A route listed in KNOWN_BROKEN must not be linked from any page."""
        from pathlib import Path
        templates = Path(__file__).resolve().parents[2]
        for name in KNOWN_BROKEN:
            for tpl in list((templates / 'results/templates').rglob('*.html')) + list((templates / 'theme/templates').rglob('*.html')):
                self.assertNotIn(f"'{name}'", tpl.read_text(), f'{tpl.name} links to broken route {name}')

    def test_login_returns_to_the_requested_page(self):
        c = Client()
        r = c.post(reverse('login') + '?next=/patients-list/', {'username': 'daniel', 'password': 'lab-pass-123'})
        self.assertRedirects(r, '/patients-list/', fetch_redirect_response=False)

    def test_login_refuses_off_site_redirects(self):
        c = Client()
        r = c.post(reverse('login') + '?next=https://evil.example/', {'username': 'daniel', 'password': 'lab-pass-123'})
        self.assertRedirects(r, reverse('index'), fetch_redirect_response=False)

    def test_login_without_next_goes_home(self):
        r = Client().post(reverse('login'), {'username': 'daniel', 'password': 'lab-pass-123'})
        self.assertRedirects(r, reverse('index'), fetch_redirect_response=False)

    def test_wrong_password_stays_on_login(self):
        r = Client().post(reverse('login'), {'username': 'daniel', 'password': 'nope'})
        self.assertEqual(r.status_code, 200)
        self.assertNotIn('_auth_user_id', Client().session)

    def test_logout(self):
        r = self.client.post(reverse('logout'))
        self.assertLess(r.status_code, 400)
        r = self.client.get(reverse('patients_list'))
        self.assertTrue(r['Location'].startswith(reverse('login')))
