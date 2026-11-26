"""Is every test the app can request present in the catalogue (Admin -> Generic tests)?

The SEND REQUEST views look their catalogue row up BY NAME. If a row is renamed
or deleted in Admin, requesting that test quietly fails with an error message
and nothing else - easy to miss for days. This reads the names straight from
the views, so a new test type is covered without editing this file.

    python manage.py check_catalogue        # exit code 1 if anything is missing
"""
import inspect
import re

from django.core.management.base import BaseCommand, CommandError

from results import views
from results.models import GenericTest

LOOKUP = re.compile(r"GenericTest,\s*name__iexact=['\"]([^'\"]+)['\"]")


def required_test_names():
    """{catalogue name: view class} for every request view in results/views.py."""
    names = {}
    for cls_name, cls in inspect.getmembers(views, inspect.isclass):
        if cls.__module__ != views.__name__:
            continue
        for name in LOOKUP.findall(inspect.getsource(cls)):
            names[name] = cls_name
    return names


class Command(BaseCommand):
    help = "Check every requestable test has its catalogue row (by name)."

    def handle(self, *args, **options):
        required = required_test_names()
        missing = sorted(n for n in required if not GenericTest.objects.filter(name__iexact=n).exists())
        unpriced = sorted(n for n in required
                          if GenericTest.objects.filter(name__iexact=n, price__isnull=True).exists())
        if unpriced:
            self.stdout.write(self.style.WARNING(
                "No price set (requests will be billed at nothing): " + ", ".join(unpriced)))
        if missing:
            lines = "\n".join(f"  - {n!r}  (used by {required[n]})" for n in missing)
            raise CommandError(
                f"{len(missing)} test(s) cannot be requested - no catalogue row with this exact name:\n{lines}\n"
                "Fix in Admin -> Generic tests (the name must match, capitals don't matter).")
        self.stdout.write(self.style.SUCCESS(f"Catalogue OK: all {len(required)} requestable tests are present."))
