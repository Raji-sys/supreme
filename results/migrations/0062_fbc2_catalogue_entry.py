from django.db import migrations

FBC2_NAME = 'Full Blood Count 2'


def add_fbc2_test(apps, schema_editor):
    """Catalogue row that FBC2CreateView bills against.

    Priced the same as the existing 'Full Blood Count' (same test, different
    analyser printout). Change it any time in Admin -> Generic tests. Does
    nothing if the row already exists, so a price set there is never reset.
    """
    GenericTest = apps.get_model('results', 'GenericTest')
    if GenericTest.objects.filter(name__iexact=FBC2_NAME).exists():
        return
    fbc1 = GenericTest.objects.filter(name__iexact='Full Blood Count').first()
    GenericTest.objects.create(
        name=FBC2_NAME,
        lab='Hematology',
        price=fbc1.price if fbc1 else None,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0061_fbc2'),
    ]

    # Reverse is a no-op: the row may already be billed against, and removing
    # a catalogue entry is a decision for the admin page, not a rollback.
    operations = [
        migrations.RunPython(add_fbc2_test, migrations.RunPython.noop),
    ]
