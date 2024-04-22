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
from django.http import HttpResponse, JsonResponse
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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
User = get_user_model()



def log_anonymous_required(view_function, redirect_to=None):
    if redirect_to is None:
        redirect_to = '/'
    return user_passes_test(lambda u: not u.is_authenticated, login_url=redirect_to)(view_function)


@login_required
def fetch_resources(uri, rel):
    if uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT,uri.replace(settings.STATIC_URL, ""))
    else:
        path = os.path.join(settings.MEDIA_ROOT,uri.replace(settings.MEDIA_URL, ""))
    return path


@method_decorator(login_required(login_url='login'), name='dispatch')
class IndexView(TemplateView):
    template_name = "index.html"

@method_decorator(login_required(login_url='login'), name='dispatch')
class DashboardView(TemplateView):
    template_name = "dashboard.html"

@method_decorator(login_required(login_url='login'), name='dispatch')
class HematologyView(TemplateView):
    template_name = "hema/hematology.html"

@method_decorator(login_required(login_url='login'), name='dispatch')
class ChempathView(TemplateView):
    template_name = "chempath/chempath.html"

@method_decorator(login_required(login_url='login'), name='dispatch')
class MicrobiologyView(TemplateView):
    template_name = "micro/micro.html"

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
    form_class = CustomUserCreationForm
    template_name = 'profile/profile_create.html'
    success_url = reverse_lazy('profile_list')

    def form_valid(self, form):
        if form.is_valid():
            response = super().form_valid(form)
            user = User.objects.get(username=form.cleaned_data['username'])
            profile_instance = Profile(user=user)
            profile_instance.save()
            messages.success(
                self.request, f"Registration for: {user.get_full_name()} was successful")
            return response
        else:
            print("Form errors:", form.errors)
            return self.form_invalid(form)
    
class ProfileDetailView(DetailView):
    template_name = 'profile/profile_details.html'
    model = Profile
    context_object_name='profile'

    def get_object(self, queryset=None):
        if self.request.user.is_superuser:
            username_from_url = self.kwargs.get('username')
            user = get_object_or_404(User, username=username_from_url)
        else:
            user = self.request.user
        return get_object_or_404(Profile, user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = context['object']
        return context


class ProfileListView(ListView):
    model = Profile
    template_name = "profile/profile_list.html"
    context_object_name = 'profiles'

    
class PatientCreateView(CreateView):
    model = Patient
    form_class= PatientForm
    template_name = 'patient/patient_create.html'
    success_url = reverse_lazy('patients_list')

    def form_valid(self, form):
        messages.success(self.request,'Patient created successfully')
        return super().form_valid(form)


class PatientUpdateView(UpdateView):
    model = Patient
    fields = ['surname', 'other_names', 'gender', 'dob', 'phone']
    template_name = 'patient/patient_create.html'
    success_url = reverse_lazy('patients_list')
 
    def form_valid(self, form):
        messages.success(self.request,'Patient updated successfully')
        return super().form_valid(form)


class PatientListView(ListView):
    model=Patient
    template_name='patient/patient_list.html'
    context_object_name='patients'
    paginate_by = 10

    def get_queryset(self):
        patients = super().get_queryset().order_by('-created')
        patient_filter = PatientFilter(self.request.GET, queryset=patients)
        return patient_filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_patient = self.get_queryset().count()
        context['patientFilter'] = PatientFilter(
            self.request.GET, queryset=self.get_queryset())
        context['total_patient'] = total_patient
        return context


class PatientDetailView(DetailView):
    model=Patient
    template_name='patient/patient_details.html'
    context_object_name='patient'

    def get_object(self, queryset=None):
        return Patient.objects.get(surname=self.kwargs['surname'])
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        patient=self.get_object()
        context['hematology_results']=patient.hematology_result.all()
        context['chempath_results']=patient.chemical_pathology_results.all()
        context['micro_results']=patient.microbiology_results.all()
        return context
    
class HematologyListView(ListView):
    model=HematologyResult
    template_name='hema/hematology_list.html'
    context_object_name='hematology_results'

    def get_queryset(self):
        queryset=super().get_queryset()
        queryset=queryset.filter(result__isnull=False)
        return queryset

class HematologyRequestListView(ListView):
    model=HematologyResult
    template_name='hema/hematology_request.html'
    context_object_name='hematology_request'

    def get_queryset(self):
        queryset=super().get_queryset()
        queryset=queryset.filter(result__isnull=True)
        return queryset


class HematologyTestCreateView(LoginRequiredMixin, CreateView):
    model = HematologyResult
    form_class = HematologyTestForm
    template_name = 'hema/hematology_result.html'

    def form_valid(self, form):
        # Set the approved_by field to the current user
        form.instance.approved_by = self.request.user

        # Get the patient instance from the request
        patient = Patient.objects.get(surname=self.kwargs['surname'])
        form.instance.patient = patient
        messages.success(self.request, 'Hematology result -created successfully')
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.object.patient.get_absolute_url()

class HematologyResultCreateView(LoginRequiredMixin, UpdateView):
    model = HematologyResult
    form_class = HematologyResultForm
    template_name = 'hema/hematology_update.html'
    context_object_name = 'result'

    def get_object(self, queryset=None):
        patient = Patient.objects.get(surname=self.kwargs['surname'])
        return HematologyResult.objects.get(patient=patient, pk=self.kwargs['pk'])

    def form_valid(self, form):
        messages.success(self.request, 'Hematology result updated successfully')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('patient_details', kwargs={'surname': self.kwargs['surname']})


@method_decorator(login_required(login_url='login'), name='dispatch')
class ReportView(ListView):
    model = HematologyResult
    template_name = 'hema/hema_report.html'
    paginate_by = 10
    context_object_name = 'patient'

    def get_queryset(self):
        queryset = super().get_queryset()

        hema_filter = HemaFilter(self.request.GET, queryset=queryset)
        patient = hema_filter.qs.order_by('-created')

        return patient

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hema_filter'] = HemaFilter(self.request.GET, queryset=self.get_queryset())
        return context


@login_required
def hema_report_pdf(request):
    ndate = datetime.datetime.now()
    filename = ndate.strftime('on_%d/%m/%Y_at_%I.%M%p.pdf')
    f = HemaFilter(request.GET, queryset=HematologyResult.objects.all()).qs

    result = ""
    for key, value in request.GET.items():
        if value:
            result += f" {value.upper()}<br>Generated on: {ndate.strftime('%d-%B-%Y at %I:%M %p')}</br>By: {request.user.username.upper()}"

    context = {'f': f, 'pagesize': 'A4',
               'orientation': 'landscape', 'result': result}
    response = HttpResponse(content_type='application/pdf',
                            headers={'Content-Disposition': f'filename="Report__{filename}"'})

    buffer = BytesIO()

    pisa_status = pisa.CreatePDF(get_template('report_pdf.html').render(
        context), dest=buffer, encoding='utf-8', link_callback=fetch_resources)

    if not pisa_status.err:
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
    return HttpResponse('Error generating PDF', status=500)


class ChempathListView(ListView):
    model=ChemicalPathologyResult
    template_name='chempath/chempath_list.html'
    context_object_name='chempath_results'

    def get_queryset(self):
        queryset=super().get_queryset()
        queryset=queryset.filter(result__isnull=False)
        return queryset

class ChempathRequestListView(ListView):
    model=ChemicalPathologyResult
    template_name='chempath/chempath_request.html'
    context_object_name='chempath_request'

    def get_queryset(self):
        queryset=super().get_queryset()
        queryset=queryset.filter(result__isnull=True)
        return queryset


class ChempathTestCreateView(LoginRequiredMixin, CreateView):
    model=ChemicalPathologyResult
    form_class = ChempathTestForm
    template_name = 'chempath/chempath_result.html'

    def form_valid(self, form):
        # Set the approved_by field to the current user
        form.instance.approved_by = self.request.user

        # Get the patient instance from the request
        patient = Patient.objects.get(surname=self.kwargs['surname'])
        form.instance.patient = patient
        messages.success(self.request, 'Chemical pathology result created successfully')
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.object.patient.get_absolute_url()


class ChempathResultCreateView(LoginRequiredMixin, UpdateView):
    model=ChemicalPathologyResult
    form_class = ChempathResultForm
    template_name = 'chempath/chempath_update.html'
    context_object_name = 'result'

    def get_object(self, queryset=None):
        patient = Patient.objects.get(surname=self.kwargs['surname'])
        return ChemicalPathologyResult.objects.get(patient=patient, pk=self.kwargs['pk'])

    def form_valid(self, form):
        messages.success(self.request, 'Chemical pathology result updated successfully')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('patient_details', kwargs={'surname': self.kwargs['surname']})


@method_decorator(login_required(login_url='login'), name='dispatch')
class ChempathReportView(ListView):
    model=ChemicalPathologyResult
    template_name = 'chempath/chempath_report.html'
    paginate_by = 10
    context_object_name = 'patient'

    def get_queryset(self):
        queryset = super().get_queryset()

        chem_filter = ChemFilter(self.request.GET, queryset=queryset)
        patient = chem_filter.qs.order_by('-created')

        return patient

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chem_filter'] = ChemFilter(self.request.GET, queryset=self.get_queryset())
        return context


@login_required
def chempath_report_pdf(request):
    ndate = datetime.datetime.now()
    filename = ndate.strftime('on_%d/%m/%Y_at_%I.%M%p.pdf')
    f = ChemFilter(request.GET, queryset=ChemicalPathologyResult.objects.all()).qs

    result = ""
    for key, value in request.GET.items():
        if value:
            result += f" {value.upper()}<br>Generated on: {ndate.strftime('%d-%B-%Y at %I:%M %p')}</br>By: {request.user.username.upper()}"

    context = {'f': f, 'pagesize': 'A4',
               'orientation': 'landscape', 'result': result}
    response = HttpResponse(content_type='application/pdf',
                            headers={'Content-Disposition': f'filename="Report__{filename}"'})

    buffer = BytesIO()

    pisa_status = pisa.CreatePDF(get_template('report_pdf.html').render(
        context), dest=buffer, encoding='utf-8', link_callback=fetch_resources)

    if not pisa_status.err:
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
    return HttpResponse('Error generating PDF', status=500)


class MicroListView(ListView):
    model=MicrobiologyResult
    template_name='micro/micro_list.html'
    context_object_name='micro_results'

    def get_queryset(self):
        queryset=super().get_queryset()
        queryset=queryset.filter(result__isnull=False)
        return queryset

class MicroRequestListView(ListView):
    model=MicrobiologyResult
    template_name='micro/micro_request.html'
    context_object_name='micro_request'

    def get_queryset(self):
        queryset=super().get_queryset()
        queryset=queryset.filter(result__isnull=True)
        return queryset


class MicroTestCreateView(LoginRequiredMixin, CreateView):
    model=MicrobiologyResult
    form_class = MicroTestForm
    template_name = 'micro/micro_result.html'

    def form_valid(self, form):
        # Set the approved_by field to the current user
        form.instance.approved_by = self.request.user

        # Get the patient instance from the request
        patient = Patient.objects.get(surname=self.kwargs['surname'])
        form.instance.patient = patient
        category_id=form.cleaned_data['category'].id
        test_id=form.cleaned_data['test'].id
        form.instance.category=MicroTestCategory.objects.get(id=category_id)
        form.instance.test=MicrobiologyTest.objects.get(id=test_id)

        messages.success(self.request, 'Microbiology result created successfully')
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.object.patient.get_absolute_url()

@login_required
def get_tests_for_category(request):
    category_id=request.GET.get('category_id')
    tests=MicrobiologyTest.objects.filter(category_id=category_id).values('id','name').order_by('name')
    data=list(tests)
    return JsonResponse(data,safe=False)


class MicroResultCreateView(LoginRequiredMixin, UpdateView):
    model=MicrobiologyResult
    form_class = MicroResultForm
    template_name = 'micro/micro_update.html'
    context_object_name = 'result'

    def get_object(self, queryset=None):
        patient = Patient.objects.get(surname=self.kwargs['surname'])
        return MicrobiologyResult.objects.get(patient=patient, pk=self.kwargs['pk'])

    def form_valid(self, form):
        messages.success(self.request, 'Microbiology result updated successfully')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('patient_details', kwargs={'surname': self.kwargs['surname']})


@method_decorator(login_required(login_url='login'), name='dispatch')
class MicroReportView(ListView):
    model=MicrobiologyResult
    template_name = 'micro/micro_report.html'
    paginate_by = 10
    context_object_name = 'patient'

    def get_queryset(self):
        queryset = super().get_queryset()

        micro_filter = MicroFilter(self.request.GET, queryset=queryset)
        patient = micro_filter.qs.order_by('-created')

        return patient

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['micro_filter'] = MicroFilter(self.request.GET, queryset=self.get_queryset())
        return context


@login_required
def micro_report_pdf(request):
    ndate = datetime.datetime.now()
    filename = ndate.strftime('on_%d/%m/%Y_at_%I.%M%p.pdf')
    f = MicroFilter(request.GET, queryset=MicrobiologyResult.objects.all()).qs

    result = ""
    for key, value in request.GET.items():
        if value:
            result += f" {value.upper()}<br>Generated on: {ndate.strftime('%d-%B-%Y at %I:%M %p')}</br>By: {request.user.username.upper()}"

    context = {'f': f, 'pagesize': 'A4',
               'orientation': 'landscape', 'result': result}
    response = HttpResponse(content_type='application/pdf',
                            headers={'Content-Disposition': f'filename="Report__{filename}"'})

    buffer = BytesIO()

    pisa_status = pisa.CreatePDF(get_template('report_pdf.html').render(
        context), dest=buffer, encoding='utf-8', link_callback=fetch_resources)

    if not pisa_status.err:
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
    return HttpResponse('Error generating PDF', status=500)