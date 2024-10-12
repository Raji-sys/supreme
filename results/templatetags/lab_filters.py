# templatetags/lab_filters.py

from django import template

register = template.Library()

@register.filter
def get_lab_results(patient, lab):
    """Get test results for a specific lab for a patient"""
    return patient.test_results.filter(test__lab=lab).order_by('-created')