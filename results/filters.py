import django_filters
from django import forms
from django.db.models import Q
from .models import *


class GenFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(
        label='id',
        field_name="id",
        lookup_expr='iexact'
    )
    collected = django_filters.DateFilter(label="date collected", field_name="collected",lookup_expr='exact', widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y'])   
    patient_no=django_filters.NumberFilter(label='pn', field_name="patient__file_no",lookup_expr='exact')
    # A General request holds up to 15 tests (test_1 .. test_15); this box finds
    # requests that include the typed test. (It used to filter on a 'name'
    # field the model doesn't have, which crashed the page.)
    name=django_filters.CharFilter(label='test', method='filter_test_name')

    class Meta:
        model=GeneralTestResult
        fields=['collected','patient_no','name']

    def filter_test_name(self, queryset, name, value):
        match = Q()
        for i in range(1, 16):
            match |= Q(**{f'test_{i}__iexact': value})
        return queryset.filter(match)

class PayFilter(django_filters.FilterSet):
    user=django_filters.CharFilter(label='STAFF', field_name="user__username",lookup_expr='iexact')
    patient=django_filters.CharFilter(label='FILE NO',field_name="patient__file_no",lookup_expr='iexact')                                                                                                     
    service=django_filters.CharFilter(label='SERVICE',field_name="service",lookup_expr='iexact')                                                                                                     
    created1 = django_filters.DateFilter(label="DATE1", field_name="created", lookup_expr='lte', widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y'])
    created2 = django_filters.DateFilter(label="DATE2", field_name="created", lookup_expr='gte', widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y'])

    class Meta:
        model = Paypoint
        fields = ['user','patient','service']


class TestFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(
        label='id',
        field_name="id",
        lookup_expr='iexact'
    )
    collected = django_filters.DateFilter(
        label="date collected",
        field_name="collected",
        lookup_expr='exact',
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y']
    )
    patient_no = django_filters.NumberFilter(
        label='pn',
        field_name="patient__file_no",
        lookup_expr='exact'
    )
    test = django_filters.CharFilter(
        label='test',
        # The test's name lives on its charge (Testinfo has no 'test' field -
        # 'test__name' crashed the report page whenever this box was used).
        field_name="payment__service",
        lookup_expr='iexact'
    )

    class Meta:
        model = Testinfo
        fields = ['id','collected', 'patient_no', 'test']


class UltrasoundFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(
        label='code',
        field_name="result_code",
        lookup_expr='iexact'
    )
    collected = django_filters.DateFilter(label="date collected", field_name="collected",lookup_expr='exact', widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y'])   
    patient_no=django_filters.NumberFilter(label='pn', field_name="patient__file_no",lookup_expr='exact')
    # No 'test' box here: an ultrasound has no test name to search, and the box
    # that used to be here filtered on a missing field and crashed the page.

    class Meta:
        model=Ultrasound
        fields=['collected','patient_no']
