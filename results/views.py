from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, ListView
from django.views import View
from .forms import *
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from .models import *
from .forms import *
from .filters import *
from django.contrib.auth import get_user_model
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
import datetime
from django.conf import settings
import os
import csv
from django.db.models import Count
User = get_user_model()



def log_anonymous_required(view_function, redirect_to=None):
    if redirect_to is None:
        redirect_to = '/'
    return user_passes_test(lambda u: not u.is_authenticated, login_url=redirect_to)(view_function)


@login_required
def fetch_resources(uri, rel):
    """
    Handles fetching static and media resources when generating the PDF.
    """
    if uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT,
                            uri.replace(settings.STATIC_URL, ""))
    else:
        path = os.path.join(settings.MEDIA_ROOT,
                            uri.replace(settings.MEDIA_URL, ""))
    return path


@method_decorator(login_required(login_url='login'), name='dispatch')
class IndexView(TemplateView):
    template_name = "index.html"

@method_decorator(log_anonymous_required, name='dispatch')
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy('index')
        else:
            return reverse_lazy('profile_details', args=[self.request.user.username])


@method_decorator(login_required(login_url='login'), name='dispatch')
class CustomLogoutView(LogoutView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, 'logout successful')
        return response


class UserProfileCreateView(CreateView):
    form_class = UserProfileForm
    template_name = 'user_profile_form.html'
    success_url = '/patient/create/'

    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)


class UserProfileUpdateView(UpdateView):
    form_class = UserProfileForm
    template_name = 'user_profile_form.html'
    success_url = '/patient/create/'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        user = form.save()

        profile = Profile.objects.get(user=user)
        profile.middle_name = form.cleaned_data['middle_name']
        profile.department = form.cleaned_data['department']
        profile.cadre = form.cleaned_data['cadre']
        profile.save()

        return super().form_valid(form)
    
    
class PatientCreateView(CreateView):
    model = Patient
    fields = ['first_name', 'last_name', 'other_name', 'gender', 'dob', 'phone']
    template_name = 'patient_form.html'
    success_url = '/hematology/create/'

    def form_valid(self, form):
        patient = form.save(commit=False)
        patient.user = self.request.user
        patient.save()
        return super().form_valid(form)


class PatientUpdateView(UpdateView):
    model = Patient
    fields = ['first_name', 'last_name', 'other_name', 'gender', 'dob', 'phone']
    template_name = 'patient_form.html'
    success_url = '/hematology/create/'



class HematologyTestCreateView(CreateView):
    model = HematologyTest
    fields = ['name', 'reference_range']
    template_name = 'hematology_test_form.html'
    success_url = '/hematology/result/create/'

class HematologyResultCreateView(CreateView):
    model = HematologyResult
    fields = ['lab_user', 'patient', 'test', 'result', 'unit', 'date']
    template_name = 'hematology_result_form.html'
    success_url = '/hematology/result/list/'

class HematologyResultUpdateView(UpdateView):
    model = HematologyResult
    fields = ['lab_user', 'patient', 'test', 'result', 'unit', 'date']
    template_name = 'hematology_result_form.html'
    success_url = '/hematology/result/list/'