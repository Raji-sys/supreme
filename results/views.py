from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count,Sum,Q
User = get_user_model()
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import black, grey
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db import reset_queries
reset_queries()

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

@method_decorator(login_required(login_url='login'), name='dispatch')
class SerologyView(TemplateView):
    template_name = "serology/serology.html"

@method_decorator(login_required(login_url='login'), name='dispatch')
class GeneralView(TemplateView):
    template_name = "general/general.html"

@method_decorator(login_required(login_url='login'), name='dispatch')
class ReportView(TemplateView):
    template_name = "report.html"

@method_decorator(login_required(login_url='login'), name='dispatch')
class RevenueView(TemplateView):
    template_name = "revenue.html"

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
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = User.objects.get(username=form.cleaned_data['username'])
        profile_instance = Profile(
            user=user, 
            department=form.cleaned_data.get('department'), 
            cadre=form.cleaned_data.get('cadre')
        )
        profile_instance.save()
        messages.success(self.request, f"Registration for: {user.get_full_name()} was successful")
        return response 


class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = 'profile/profile_update.html'
    success_url = reverse_lazy('profiles_list') 

    def get(self, request, *args, **kwargs):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form
        })

    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {
                'user_form': user_form,
                'profile_form': profile_form
            })


class ProfileListView(ListView):
    model = Profile
    template_name = "profile/profile_list.html"
    context_object_name = 'profiles'    

class UserDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'profile/confirm_delete.html'
    success_url = reverse_lazy('profiles_list')
    success_message = "User and associated profile deleted successfully!"

    def get_object(self, queryset=None):
        profile_id = self.kwargs.get('pk')
        profile = get_object_or_404(Profile, pk=profile_id)
        return get_object_or_404(User, profile=profile)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

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
    form_class= PatientForm
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
        queryset = super().get_queryset().order_by('-file_no')
        # Add search functionality
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(surname__icontains=query) |
                Q(other_names__icontains=query) |
                Q(file_no__icontains=query)|
                Q(phone__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_count = self.get_queryset().count()
        total_patient=Patient.objects.count()
        context['search_count'] = search_count
        context['total_patient'] = total_patient
        context['query'] = self.request.GET.get('q', '')

        return context


class PatientDetailView(DetailView):
    model=Patient
    template_name='patient/patient_details.html'
    context_object_name='patient'

    def get_object(self, queryset=None):
        return Patient.objects.get(file_no=self.kwargs['file_no'])
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        patient=self.get_object()

        context['blood_group'] = patient.test_info.filter(bg_test__isnull=False).order_by('-created').select_related('bg_test')
        context['genotype'] = patient.test_info.filter(gt_test__isnull=False).order_by('-created').select_related('gt_test')
        context['rhesus'] = patient.test_info.filter(rh_test__isnull=False).order_by('-created').select_related('rh_test')
        context['fbc'] = patient.test_info.filter(fbc_test__isnull=False).order_by('-created').select_related('fbc_test')

        context['urea_electrolyte'] = patient.test_info.filter(ue_test__isnull=False).order_by('-created').select_related('ue_test')
        context['liver_function'] = patient.test_info.filter(lf_test__isnull=False).order_by('-created').select_related('lf_test')
        context['lipid_profile'] = patient.test_info.filter(lp_test__isnull=False).order_by('-created').select_related('lp_test')
        context['blood_glucose'] = patient.test_info.filter(bgl_test__isnull=False).order_by('-created').select_related('bgl_test')
        context['bone_chemistry'] = patient.test_info.filter(bc_test__isnull=False).order_by('-created').select_related('bc_test')
        context['serum_proteins'] = patient.test_info.filter(sp_test__isnull=False).order_by('-created').select_related('sp_test')
        context['cerebro_spinal_fluid'] = patient.test_info.filter(csf_test__isnull=False).order_by('-created').select_related('csf_test')
        context['miscellaneous_chempath_tests'] = patient.test_info.filter(misc_test__isnull=False).order_by('-created').select_related('misc_test')

        context['widal'] = patient.test_info.filter(widal_test__isnull=False).order_by('-created').select_related('widal_test')
        context['rheumatoid_factor'] = patient.test_info.filter(rheumatoid_factor_test__isnull=False).order_by('-created').select_related('rheumatoid_factor_test')
        context['hpb'] = patient.test_info.filter(hpb_test__isnull=False).order_by('-created').select_related('hpb_test')
        context['hcv'] = patient.test_info.filter(hcv_test__isnull=False).order_by('-created').select_related('hcv_test')
        context['vdrl']= patient.test_info.filter(vdrl_test__isnull=False).order_by('-created').select_related('vdrl_test')
        context['mantoux']= patient.test_info.filter(mantoux_test__isnull=False).order_by('-created').select_related('mantoux_test')
        context['crp']=patient.test_info.filter(crp_test__isnull=False).order_by('-created').select_related('crp_test')
        context['hiv_screening']= patient.test_info.filter(hiv_test__isnull=False).order_by('-created').select_related('hiv_test')
        context['aso_titre'] = patient.test_info.filter(aso_titre_test__isnull=False).order_by('-created').select_related('aso_titre_test')
        
        context['urine_microscopy'] = patient.test_info.filter(urine_test__isnull=False).order_by('-created').select_related('urine_test')
        context['hvs'] = patient.test_info.filter(hvs_test__isnull=False).order_by('-created').select_related('hvs_test')
        context['stool'] = patient.test_info.filter(stool_test__isnull=False).order_by('-created').select_related('stool_test')
        context['blood_culture'] = patient.test_info.filter(blood_culture_test__isnull=False).order_by('-created').select_related('blood_culture_test')
        context['occult_blood'] = patient.test_info.filter(occult_blood_test__isnull=False).order_by('-created').select_related('occult_blood_test')
        context['sputum_mcs'] = patient.test_info.filter(sputum_mcs_test__isnull=False).order_by('-created').select_related('sputum_mcs_test')
        context['gram_stain'] = patient.test_info.filter(gram_stain_test__isnull=False).order_by('-created').select_related('gram_stain_test')
        context['zn_stain'] = patient.test_info.filter(zn_stain_test__isnull=False).order_by('-created').select_related('zn_stain_test')
        context['semen_analysis'] = patient.test_info.filter(semen_analysis_test__isnull=False).order_by('-created').select_related('semen_analysis_test')
        context['urinalysis'] = patient.test_info.filter(urinalysis_test__isnull=False).order_by('-created').select_related('urinalysis_test')
        context['pregnancy'] = patient.test_info.filter(pregnancy_test__isnull=False).order_by('-created').select_related('pregnancy_test')



        context['general_results']=patient.general_results.all().order_by('-created')
        
        return context
    
    
class HematologyRequestListView(ListView):
    model=Testinfo
    template_name='hema/hematology_request.html'
    context_object_name='hematology_request'
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(payment__unit__iexact="Hematology",cleared=False).order_by('-updated')
        return queryset

    
class HematologyListView(ListView):
    model=Testinfo
    template_name='hema/hematology_list.html'
    context_object_name='hematology_results'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(payment__status=True,payment__unit__iexact='Hematology',cleared=True).order_by('-updated')
        return queryset
    

@method_decorator(login_required(login_url='login'), name='dispatch')
class ReportView(ListView):
    model = Testinfo
    template_name = 'report.html'
    paginate_by = 10
    context_object_name = 'patient'

    def get_queryset(self):
        queryset = super().get_queryset()

        test_filter = TestFilter(self.request.GET, queryset=queryset)
        patient = test_filter.qs.order_by('-created')
        return patient

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test_filter'] = TestFilter(self.request.GET, queryset=self.get_queryset())
        return context

@login_required
def report_pdf(request):
    ndate = datetime.datetime.now()
    filename = ndate.strftime('on_%d_%m_%Y_at_%I_%M%p.pdf')
    f = TestFilter(request.GET, queryset=Testinfo.objects.all()).qs
    
    username = request.user.username.upper() if hasattr(request.user, 'username') else "UNKNOWN USER"
    
    result = ""
    for key, value in request.GET.items():
        if value:
            result += f" {value.upper()}<br>Generated on: {ndate.strftime('%d-%B-%Y at %I:%M %p')}</br>By: {username}"
    
    context = {'f': f,'pagesize': 'A4','orientation': 'potrait', 'result': result,'username': username,'generated_date': ndate.strftime('%d-%B-%Y at %I:%M %p')}
    
    response = HttpResponse(content_type='application/pdf',headers={'Content-Disposition': f'attachment; filename="{filename}"'})
    html = get_template('report_pdf.html').render(context)
    
    buffer = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=buffer, encoding='utf-8', link_callback=fetch_resources)
    
    if not pisa_status.err:
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
    
    return HttpResponse('Error generating PDF', status=500)

class ChempathRequestListView(ListView):
    model=Testinfo
    template_name='chempath/chempath_request.html'
    context_object_name='chempath_request'

    def get_queryset(self):
        queryset=super().get_queryset()
        queryset = queryset.filter(payment__unit__iexact="Chemical pathology",cleared=False).order_by('-updated')
        return queryset
    

class ChempathListView(ListView):
    model=Testinfo
    template_name='chempath/chempath_list.html'
    context_object_name='chempath_results'

    def get_queryset(self):
        queryset=super().get_queryset()
        queryset=queryset.filter(payment__status=True,payment__unit__iexact='Chemical pathology',cleared=True).order_by('-updated')
        return queryset


class MicroRequestListView(ListView):
    model=Testinfo
    template_name='micro/micro_request.html'
    context_object_name='micro_request'

    def get_queryset(self):
        queryset=super().get_queryset()
        queryset = queryset.filter(payment__unit__iexact="Microbiology",cleared=False).order_by('-updated')
        return queryset


class MicroListView(ListView):
    model=Testinfo
    template_name='micro/micro_list.html'
    context_object_name='micro_results'

    def get_queryset(self):
        queryset=super().get_queryset()
        queryset=queryset.filter(payment__status=True,payment__unit__iexact='Microbiology',cleared=True).order_by('-updated')
        return queryset


class SerologyRequestListView(ListView):
    model = Testinfo
    template_name = 'serology/serology_request.html'
    context_object_name = 'serology_request'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(payment__unit__iexact="Serology",cleared=False).order_by('-updated')
        return queryset


class SerologyListView(ListView):
    model=Testinfo
    template_name='serology/serology_list.html'
    context_object_name='serology_results'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset=queryset.filter(payment__status=True,payment__unit__iexact='Serology',cleared=True).order_by('-updated')
        return queryset
    

class GeneralRequestListView(ListView):
    model=GeneralTestResult
    template_name='general/general_request.html'
    context_object_name='general_request'

    def get_queryset(self):
        queryset=super().get_queryset()
        queryset = queryset.filter(cleared=False).order_by('-updated')
        return queryset
    

class GeneralListView(ListView):
    model=GeneralTestResult
    template_name='general/general_list.html'
    context_object_name='general_results'

    def get_queryset(self):
        queryset=super().get_queryset()
        queryset=queryset.filter(payment__status=True,cleared=True).order_by('-updated')
        return queryset


class GeneralTestCreateView(LoginRequiredMixin, CreateView):
    model=GeneralTestResult
    form_class = GeneralTestForm
    template_name = 'general/general_result.html'

    def form_valid(self, form):
        patient = Patient.objects.get(file_no=self.kwargs['file_no'])
        form.instance.patient = patient
        form.instance.collected_by = self.request.user

        general_result = form.save(commit=False)
        payment = Paypoint.objects.create(
            patient=patient,
            status=False,
            service=general_result.name, 
            price=general_result.price,
        )
        general_result.payment = payment 
        general_result.save()
        messages.success(self.request, 'general added successfully')
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.object.patient.get_absolute_url()


class GeneralResultCreateView(LoginRequiredMixin, UpdateView):
    model=GeneralTestResult
    form_class = GeneralTestResultForm
    template_name = 'general/general_result.html'
    context_object_name = 'result'
    success_url=reverse_lazy('general_request')


    def get_object(self, queryset=None):
        patient = get_object_or_404(Patient, file_no=self.kwargs['file_no'])
        return GeneralTestResult.objects.get(patient=patient, pk=self.kwargs['pk'])

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        general_result = form.save(commit=False)
        general_result.result = form.cleaned_data['result']
        general_result.save()
        messages.success(self.request, 'general result updated successfully')
        return super().form_valid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class GeneralReportView(ListView):
    model=GeneralTestResult
    template_name = 'general/general_report.html'
    paginate_by = 10
    context_object_name = 'patient'

    def get_queryset(self):
        queryset = super().get_queryset()

        gen_filter = GenFilter(self.request.GET, queryset=queryset)
        patient = gen_filter.qs.order_by('-created')

        return patient

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gen_filter'] = GenFilter(self.request.GET, queryset=self.get_queryset())
        return context

@login_required
def general_report_pdf(request):
    ndate = datetime.datetime.now()
    filename = ndate.strftime('on_%d_%m_%Y_at_%I_%M%p.pdf')  # Changed slashes to underscores

    f = GenFilter(request.GET, queryset=GeneralTestResult.objects.all()).qs
    # Get username safely
    username = request.user.username.upper() if hasattr(request.user, 'username') else "UNKNOWN USER"
    
    result = ""
    for key, value in request.GET.items():
        if value:
            result += f" {value.upper()}<br>Generated on: {ndate.strftime('%d-%B-%Y at %I:%M %p')}</br>By: {username}"
    
    context = {
        'f': f, 
        'pagesize': 'A4',
        'orientation': 'landscape', 
        'result': result,
        'username': username,
        'generated_date': ndate.strftime('%d-%B-%Y at %I:%M %p')
    }
    
    response = HttpResponse(content_type='application/pdf',
                           headers={'Content-Disposition': f'attachment; filename="{filename}"'})
    
    html = get_template('report_pdf.html').render(context)
    
    buffer = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=buffer, encoding='utf-8', link_callback=fetch_resources)
    
    if not pisa_status.err:
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
    
    return HttpResponse('Error generating PDF', status=500)


class PayCreateView(CreateView):
    model = Paypoint
    form_class = PayForm
    template_name = 'new_pay.html'
    success_url = reverse_lazy("pay_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        paypoint = form.save(commit=False)
        messages.success(self.request, 'TRANSACTION SUCCESSFULLY')
        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', reverse_lazy("pay_list"))
        # Add wallet balance to context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return super().get_success_url()

class PayUpdateView(UpdateView):
    model = Paypoint
    template_name = 'revenue/update_pay.html'
    form_class = PayUpdateForm

    def get_success_url(self):
        messages.success(self.request, 'TRANSACTION SUCCESSFULLY')
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy("pay_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paypoint = self.get_object()
        context['patient'] = paypoint.patient
        context['service'] = paypoint.service
        context['next'] = self.request.GET.get('next', reverse_lazy("pay_list"))
        return context

    
class PayListView(ListView):
    model = Paypoint
    template_name = 'revenue/transaction.html'
    context_object_name = 'pays'
    paginate_by = 10

    def get_queryset(self):
        # Start with an optimized queryset
        queryset = Paypoint.objects.select_related('patient', 'user').order_by('-updated')
        
        # Get filter parameter from URL, default to 'all'
        status_filter = self.request.GET.get('status', 'all')
        
        # Apply status filter if not 'all'
        if status_filter == 'approved':
            queryset = queryset.filter(status=True)
        elif status_filter == 'pending':
            queryset = queryset.filter(status=False)
        
        # Apply other filters from PayFilter
        pay_filter = PayFilter(self.request.GET, queryset=queryset)
        return pay_filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add annotations for quick access to key metrics
        summary = Paypoint.objects.aggregate(
            total_count=Count('id'),
            approved_count=Count('id', filter=Q(status=True)),
            pending_count=Count('id', filter=Q(status=False)),
            total_worth=Sum('price', filter=Q(status=True)),
            total_pending=Sum('price', filter=Q(status=False))
        )
        
        context.update({
            'total_count': summary['total_count'],
            'approved_count': summary['approved_count'],
            'pending_count': summary['pending_count'],
            'total_worth': summary['total_worth'] or 0,
            'total_pending': summary['total_pending'] or 0,
            'current_filter': self.request.GET.get('status', 'all'),
            'payFilter': PayFilter(self.request.GET, queryset=self.get_queryset())
        })
        
        # Add date-based metrics
        today = timezone.now().date()
        context['today_transactions'] = self.get_queryset().filter(created=today).count()
        context['today_worth'] = self.get_queryset().filter(
            created=today, status=True
        ).aggregate(total=Sum('price'))['total'] or 0
        
        return context

def format_currency(amount):
    if amount is None:
        return "N0.00"
    return f"N{amount:,.2f}"

@login_required
def receipt_pdf(request):
    # Get the queryset
    f = PayFilter(request.GET, queryset=Paypoint.objects.all()).qs
    
    # Get the patient from the first Paypoint object
    patient = f.first().patient if f.exists() else None

    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=(3*inch, 11*inch))  # 3 inches wide, 11 inches long

    # Try to register custom fonts, fall back to standard fonts if not available
    try:
        pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
        pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
        font_name = 'Vera'
        font_bold = 'VeraBd'
    except:
        font_name = 'Helvetica'
        font_bold = 'Helvetica-Bold'

    # Start drawing from the top of the page
    y = 10.5*inch

    # Try to draw logo if available
    logo_path = os.path.join(settings.STATIC_ROOT, 'images', '5.png')
    if os.path.exists(logo_path):
        p.drawInlineImage(logo_path, 0.75*inch, y - 0.5*inch, width=1.5*inch, height=0.5*inch)
        y -= 0.7*inch
    else:
        y -= 0.2*inch  # Adjust spacing if no logo

    # Draw the header
    p.setFont(font_bold, 12)
    p.drawCentredString(1.5*inch, y, "PAYMENT RECEIPT")
    y -= 0.3*inch

    # Draw a line
    p.setStrokeColor(grey)
    p.line(0.25*inch, y, 2.75*inch, y)
    y -= 0.2*inch

    # Draw patient info
    p.setFont(font_name, 8)
    if patient:
        p.drawString(0.25*inch, y, f"Patient: {patient}")
        y -= 0.15*inch
        p.drawString(0.25*inch, y, f"File No: {patient.file_no}")
        y -= 0.2*inch

    # Draw a line
    p.line(0.25*inch, y, 2.75*inch, y)
    y -= 0.2*inch

    # Draw column headers
    p.setFont(font_bold, 8)
    p.drawString(0.25*inch, y, "Service")
    p.drawString(1.75*inch, y, "Price")
    p.drawString(2.25*inch, y, "Date")
    y -= 0.15*inch

    # Draw a line
    p.line(0.25*inch, y, 2.75*inch, y)
    y -= 0.1*inch

    # Draw payment details
    p.setFont(font_name, 8)
    total = 0
    for payment in f:
        if y < 1*inch:  # If we're near the bottom of the page, start a new page
            p.showPage()
            p.setFont(font_name, 8)
            y = 10.5*inch

        p.drawString(0.25*inch, y, str(payment.service)[:20])  # Truncate long service names
        p.drawRightString(2.15*inch, y, format_currency(payment.price))
        p.drawString(2.25*inch, y, payment.updated.strftime("%d/%m"))
        y -= 0.15*inch
        total += payment.price or 0  # Use 0 if price is None

    # Draw a line
    y -= 0.1*inch
    p.setStrokeColor(black)
    p.line(0.25*inch, y, 2.75*inch, y)
    y -= 0.2*inch

    # Draw total
    p.setFont(font_bold, 10)
    p.drawString(0.25*inch, y, "Total:")
    p.drawRightString(2.75*inch, y, format_currency(total))

    # Draw footer
    y -= 0.4*inch
    p.setFont(font_name, 7)
    p.drawCentredString(1.5*inch, y, f"Generated: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}")
    y -= 0.15*inch
    p.drawCentredString(1.5*inch, y, f"By: {request.user.username.upper()}")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')


class HemaPayListView(ListView):
    model = Paypoint
    template_name = 'revenue/hema_pay_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Paypoint.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        hematology_pays = Paypoint.objects.filter(test_payments__isnull=False,unit__iexact='Hematology').order_by('-updated')

        hema_pay_total = hematology_pays.count()
        hema_paid_transactions = hematology_pays.filter(status=True)
        hema_total_worth = hema_paid_transactions.aggregate(total_worth=Sum('price'))['total_worth'] or 0


        context['hematology_pays'] = hematology_pays

        context['hema_pay_total'] = hema_pay_total

        context['hema_total_worth'] = hema_total_worth
        return context


class MicroPayListView(ListView):
    model = Paypoint
    template_name = 'revenue/micro_pay_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Paypoint.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        micro_pays = Paypoint.objects.filter(test_payments__isnull=False,unit__iexact='Microbiology').order_by('-updated')

        micro_pay_total = micro_pays.count()
        micro_paid_transactions = micro_pays.filter(status=True)
        micro_total_worth = micro_paid_transactions.aggregate(total_worth=Sum('price'))['total_worth'] or 0

        context['micro_pays'] = micro_pays
        context['micro_pay_total'] = micro_pay_total
        context['micro_total_worth'] = micro_total_worth
        return context  


class ChempathPayListView(ListView):
    model = Paypoint
    template_name = 'revenue/chempath_pay_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Paypoint.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        chempath_pays = Paypoint.objects.filter(test_payments__isnull=False,unit__iexact='Chemical Pathology').order_by('-updated')

        chem_pay_total = chempath_pays.count()
        chem_paid_transactions = chempath_pays.filter(status=True)
        chem_total_worth = chem_paid_transactions.aggregate(total_worth=Sum('price'))['total_worth'] or 0

        context['chempath_pays'] = chempath_pays
        context['chem_pay_total'] = chem_pay_total
        context['chem_total_worth'] = chem_total_worth
        return context


class SerologyPayListView(ListView):
    model = Paypoint
    template_name = 'revenue/serology_pay_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Paypoint.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        serology_pays = Paypoint.objects.filter(test_payments__isnull=False,unit__iexact='Serology').order_by('-updated')

        serology_pay_total = serology_pays.count()
        serology_paid_transactions = serology_pays.filter(status=True)
        serology_total_worth = serology_paid_transactions.aggregate(total_worth=Sum('price'))['total_worth'] or 0

        context['serology_pays'] = serology_pays
        context['serology_pay_total'] = serology_pay_total
        context['serology_total_worth'] = serology_total_worth
        return context  


class GeneralPayListView(ListView):
    model = Paypoint
    template_name = 'revenue/general_pay_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Paypoint.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        general_pays = Paypoint.objects.filter(general_result_payment__isnull=False).order_by('-updated')
 
        general_pay_total = general_pays.count()
        general_paid_transactions = general_pays.filter(status=True)
        general_total_worth = general_paid_transactions.aggregate(total_worth=Sum('price'))['total_worth'] or 0

        context['general_pays'] = general_pays
        context['general_pay_total'] = general_pay_total
        context['general_total_worth'] = general_total_worth
        return context  

    
class BaseTestView(LoginRequiredMixin):
    template_name = 'shared_test_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BaseLabResultUpdateView(BaseTestView, UpdateView):
    def get_object(self, queryset=None):
        # Fetch the patient using the file_no
        patient = get_object_or_404(Patient, file_no=self.kwargs['file_no'])
        # Return the specific test object related to this patient
        return get_object_or_404(self.model, test_info__patient=patient, pk=self.kwargs['pk'])

    def form_valid(self, form):
        # Mark the test as cleared
        form.instance.test_info.cleared = True
        form.instance.test_info.save()

        # Add a success message
        messages.success(self.request, f'{form.instance.test.name} result updated successfully')

        # Redirect to the patient's profile page after saving
        return redirect('patient_details', file_no=self.kwargs['file_no'])

# hematology 
class BloodGroupCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='Blood Group')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            
            blood_group = BloodGroup.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'Blood Group test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating Blood Group test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


class GenotypeCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='Genotype')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            geno = Genotype.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'Genotype test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating Genotype test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


class RhesusCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='Rhesus Factor')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            rhesus = RhesusFactor.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'Rhesus test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating Rhesus test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


class FBCCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='Full Blood Count')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            fbc = FBC.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'FBC test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating FBC test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))

# chempath 
class UECreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='Urea & Electrolyte')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            ue = UreaAndElectrolyte.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'UREA & ELCTROLYTE test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating UREA & ELCTROLYTE test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


class LiverFunctionCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='Liver Function')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            liver_function = LiverFunction.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'Liver Function test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating Liver Function test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


class LipidProfileCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='Lipid Profile')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            lipid_profile = LipidProfile.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'Lipid Profile test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating Lipid Profile test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


class SerumProteinsCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='Serum Proteins')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            serum_proteins = SerumProteins.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'Serum Proteins test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating Serum Proteins test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


class CerebroSpinalFluidCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='Cerebro Spinal Fluid')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            cerebro_spinal_fluid = CerebroSpinalFluid.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'Cerebro Spinal Fluid test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating Cerebro Spinal Fluid test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


class BoneChemistryCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='Bone Chemistry')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            bone_chemistry = BoneChemistry.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'Bone Chemistry test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating Bone Chemistry test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


class MiscellaneousChempathTestsCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='Miscellaneous Chempath Tests')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            miscellaneous_chempath_tests = MiscellaneousChempathTests.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'Miscellaneous Chempath Tests  created successfully')
        except Exception as e:
            messages.error(request, f'Error creating Miscellaneous Chempath Tests: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


class BloodGlucoseCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='Blood Glucose')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            blood_glucose = BloodGlucose.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'Blood Glucose test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating Blood Glucose test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))

# serology 
class WidalCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='Widal')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            widal = Widal.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'Widal test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating Widal test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))
    

class RheumatoidFactorCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='Rheumatoid Factor')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            rheumatoid_factor = RheumatoidFactor.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'Rheumatoid Factor test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating Rheumatoid Factor test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


class HepatitisBCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='Hepatitis B')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            hpb = HPB.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'Hepatitis B test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating Hepatitis B test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


class HepatitisCCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='Hepatitis C')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            hcv = HCV.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'Hepatitis C test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating Hepatitis C test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


class VDRLCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='VDRL')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            vdrl = VDRL.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'VDRL test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating VDRL test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


class MantouxCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='Mantoux')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            mantoux = Mantoux.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'Mantoux test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating Mantoux test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


class AsoTitreCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='Aso Titre')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            aso_titre = AsoTitre.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'Aso Titre test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating Aso Titre test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


class CRPCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='CRP')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            crp = CRP.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'CRP test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating CRP test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


class HIVScreeningCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='HIV Screening')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            hiv_screening = HIVScreening.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'HIV Screening test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating HIVScreening test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


#microbiology
class UrineMicroscopyCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='Urine Microscopy')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            urine_microscopy = UrineMicroscopy.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'Urine Microscopy test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating Urine Microscopy test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


class HVSCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='HVS')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            hvs = HVS.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'HVS test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating HVS test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


class StoolCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='Stool')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            stool = Stool.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'Stool test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating Stool test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


class BloodCultureCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='Blood Culture')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            blood_culture = BloodCulture.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'Blood Culture test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating Blood Culture test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


class OccultBloodCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='Occult Blood')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            occult_blood = OccultBlood.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'Occult Blood test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating Occult Blood test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


class SputumMCSCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='Sputum MCS')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            sputum_mcs = SputumMCS.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'Sputum MCS test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating Sputum MCS test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


class GramStainCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='Gram Stain')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            gram_stain = GramStain.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'Gram Stain test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating Gram Stain test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


class ZNStainCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='ZN Stain')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            zn_stain = ZNStain.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'ZN Stain test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating ZN Stain test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


class SemenAnalysisCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='Semen Analysis')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            semen_analysis = SemenAnalysis.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'Semen Analysis test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating Semen Analysis Stain test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


class UrinalysisCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='Urinalysis')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            urinalysis = Urinalysis.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'Urinalysis test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating Urinalysis test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


class PregnancyCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name__iexact='Pregnancy')
            
            # Create Paypoint first
            payment = Paypoint.objects.create(
                patient=patient,
                status=False,
                unit=generic_test.lab,
                service=generic_test.name,
                price=generic_test.price,
            )
            
            # Now create Testinfo with the payment
            test_info = Testinfo.objects.create(
                patient=patient,
                collected_by=request.user,
                payment=payment
            )
            
            pregnancy = Pregnancy.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'Pregnancy test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating Pregnancy test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


class BaseLabResultUpdateView(UpdateView):
    template_name = 'shared_test_form.html'

    def get_object(self, queryset=None):
        patient = get_object_or_404(Patient, file_no=self.kwargs['file_no'])
        test_info = get_object_or_404(Testinfo, patient=patient, pk=self.kwargs['test_info_pk'])
        return get_object_or_404(self.model, test_info=test_info)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.test_info.cleared = True
        instance.test_info.save()
        instance.save()
        messages.success(self.request, f'{self.model.__name__} result updated successfully')
        return redirect('patient_details', file_no=self.kwargs['file_no'])


# hematology 
class BloodGroupUpdateView(BaseLabResultUpdateView):
    model = BloodGroup
    form_class = BloodGroupForm


class GenotypeUpdateView(BaseLabResultUpdateView):
    model = Genotype
    form_class = GenotypeForm


class RhesusUpdateView(BaseLabResultUpdateView):
    model = RhesusFactor
    form_class = RhesusFactorForm


class FBCUpdateView(BaseLabResultUpdateView):
    model = FBC
    form_class = FBCForm

# chempath 
class UreaAndElectrolyteUpdateView(BaseLabResultUpdateView):
    model = UreaAndElectrolyte
    form_class = UreaAndElectrolyteForm

class LiverFunctionUpdateView(BaseLabResultUpdateView):
    model = LiverFunction
    form_class = LiverFunctionForm


class LipidProfileUpdateView(BaseLabResultUpdateView):
    model = LipidProfile
    form_class = LipidProfileForm


class SerumProteinsUpdateView(BaseLabResultUpdateView):
    model = SerumProteins
    form_class = SerumProteinsForm


class CerebroSpinalFluidUpdateView(BaseLabResultUpdateView):
    model = CerebroSpinalFluid
    form_class = CerebroSpinalFluidForm


class BoneChemistryUpdateView(BaseLabResultUpdateView):
    model = BoneChemistry
    form_class = BoneChemistryForm


class BloodGlucoseUpdateView(BaseLabResultUpdateView):
    model = BloodGlucose
    form_class = BloodGlucoseForm


class MiscellaneousChempathTestsUpdateView(BaseLabResultUpdateView):
    model = MiscellaneousChempathTests
    form_class = MiscellaneousChempathTestsForm


#SEROLOGY TEST
class WidalUpdateView(BaseLabResultUpdateView):
    model = Widal
    form_class = WidalForm


class RheumatoidFactorUpdateView(BaseLabResultUpdateView):
    model = RheumatoidFactor
    form_class = RheumatoidFactorForm


class HepatitisBUpdateView(BaseLabResultUpdateView):
    model = HPB
    form_class = HepatitisBForm


class HepatitisCUpdateView(BaseLabResultUpdateView):
    model = HCV
    form_class = HepatitisCForm


class VDRLUpdateView(BaseLabResultUpdateView):
    model = VDRL
    form_class = VDRLForm


class MantouxUpdateView(BaseLabResultUpdateView):
    model = Mantoux
    form_class = MantouxForm


class AsoTitreUpdateView(BaseLabResultUpdateView):
    model = AsoTitre
    form_class = AsoTitreForm


class CRPUpdateView(BaseLabResultUpdateView):
    model = CRP
    form_class = CRPForm


class HIVScreeningUpdateView(BaseLabResultUpdateView):
    model = HIVScreening
    form_class = HIVScreeningForm


#MICROBIOLOGY
class UrineMicroscopyUpdateView(BaseLabResultUpdateView):
    model = UrineMicroscopy
    form_class = UrineMicroscopyForm


class HVSUpdateView(BaseLabResultUpdateView):
    model = HVS
    form_class = HVSForm


class StoolUpdateView(BaseLabResultUpdateView):
    model = Stool
    form_class = StoolForm


class BloodCultureUpdateView(BaseLabResultUpdateView):
    model = BloodCulture
    form_class = BloodCultureForm


class OccultBloodUpdateView(BaseLabResultUpdateView):
    model = OccultBlood
    form_class = OccultBloodForm


class SputumMCSUpdateView(BaseLabResultUpdateView):
    model = SputumMCS
    form_class = SputumMCSForm


class GramStainUpdateView(BaseLabResultUpdateView):
    model = GramStain
    form_class = GramStainForm


class ZNStainUpdateView(BaseLabResultUpdateView):
    model = ZNStain
    form_class = ZNStainForm


class SemenAnalysisUpdateView(BaseLabResultUpdateView):
    model = SemenAnalysis
    form_class = SemenAnalysisForm


class UrinalysisUpdateView(BaseLabResultUpdateView):
    model = Urinalysis
    form_class = UrinalysisForm


class PregnancyUpdateView(BaseLabResultUpdateView):
    model = Pregnancy
    form_class = PregnancyForm
