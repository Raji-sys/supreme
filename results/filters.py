import django_filters
from django import forms
from .models import *
from django.forms import TimeInput

class PatientFilter(django_filters.FilterSet):
    phone = django_filters.CharFilter(label='phone number', field_name='phone')

    class Meta:
        model = Patient
        fields = ['phone']


class HemaFilter(django_filters.FilterSet):
    collected = django_filters.DateFilter(label="date collected", field_name="collected",lookup_expr='exact', widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y'])
    reported = django_filters.DateFilter(label="date reported", field_name="reported",lookup_expr='exact', widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y'])
    phone=django_filters.NumberFilter(label='phone', field_name="patient__phone",lookup_expr='exact')
    test=django_filters.CharFilter(label='test',field_name="test",lookup_expr='iexact')                                                                                                     

    class Meta:
        model=HematologyResult
        fields=['collected','reported','phone','test']