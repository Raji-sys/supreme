import django_filters
from django import forms
from .models import *


class PatientFilter(django_filters.FilterSet):
    patient_no = django_filters.CharFilter(label='patient no', field_name='patient_no')

    class Meta:
        model = Patient
        fields = ['patient_no']


class HemaFilter(django_filters.FilterSet):
    collected = django_filters.DateFilter(label="date collected", field_name="collected",lookup_expr='exact', widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y'])
    reported = django_filters.DateFilter(label="date reported", field_name="reported",lookup_expr='exact', widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y'])
    patient_no=django_filters.NumberFilter(label='pn', field_name="patient__patient_no",lookup_expr='exact')
    test=django_filters.CharFilter(label='test',field_name="test",lookup_expr='iexact')                                                                                                     
    result_code=django_filters.CharFilter(label='code',field_name="result_code",lookup_expr='iexact')                                                                                                     

    class Meta:
        model=HematologyResult
        fields=['collected','reported','result_code','patient_no','test']

class ChemFilter(django_filters.FilterSet):
    collected = django_filters.DateFilter(label="date collected", field_name="collected",lookup_expr='exact', widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y'])
    reported = django_filters.DateFilter(label="date reported", field_name="reported",lookup_expr='exact', widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y'])
    patient_no=django_filters.NumberFilter(label='pn', field_name="patient__patient_no",lookup_expr='exact')
    test=django_filters.CharFilter(label='test',field_name="test",lookup_expr='iexact')                                                                                                     
    result_code=django_filters.CharFilter(label='code',field_name="result_code",lookup_expr='iexact')                                                                                                     

    class Meta:
        model=ChemicalPathologyResult
        fields=['collected','reported','result_code','patient_no','test']


class MicroFilter(django_filters.FilterSet):
    collected = django_filters.DateFilter(label="date collected", field_name="collected",lookup_expr='exact', widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y'])
    reported = django_filters.DateFilter(label="date reported", field_name="reported",lookup_expr='exact', widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y'])
    patient_no=django_filters.NumberFilter(label='pn', field_name="patient__patient_no",lookup_expr='exact')
    test=django_filters.CharFilter(label='test',field_name="test__name",lookup_expr='iexact')                                                                                                     
    result_code=django_filters.CharFilter(label='code',field_name="result_code",lookup_expr='iexact')                                                                                                     

    class Meta:
        model=MicrobiologyResult
        fields=['collected','reported','result_code','patient_no','test']

class SerologyFilter(django_filters.FilterSet):
    collected = django_filters.DateFilter(label="date collected", field_name="collected",lookup_expr='exact', widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y'])
    reported = django_filters.DateFilter(label="date reported", field_name="reported",lookup_expr='exact', widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y'])
    patient_no=django_filters.NumberFilter(label='pn', field_name="patient__patient_no",lookup_expr='exact')
    test=django_filters.CharFilter(label='test',field_name="test__name",lookup_expr='iexact')                                                                                                     
    result_code=django_filters.CharFilter(label='code',field_name="result_code",lookup_expr='iexact')                                                                                                     

    class Meta:
        model=SerologyResult
        fields=['collected','reported','result_code','patient_no','test']

class GenFilter(django_filters.FilterSet):
    collected = django_filters.DateFilter(label="date collected", field_name="collected",lookup_expr='exact', widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y'])
    reported = django_filters.DateFilter(label="date reported", field_name="reported",lookup_expr='exact', widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y'])
    patient_no=django_filters.NumberFilter(label='pn', field_name="patient__patient_no",lookup_expr='exact')
    name=django_filters.CharFilter(label='test',field_name="name",lookup_expr='iexact')                                                                                                     
    result_code=django_filters.CharFilter(label='code',field_name="result_code",lookup_expr='iexact')                                                                                                     

    class Meta:
        model=SerologyResult
        fields=['collected','reported','result_code','patient_no','name']