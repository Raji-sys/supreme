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
        context['ue'] = patient.test_info.filter(ue_test__isnull=False).order_by('-created').select_related('ue_test')

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
    

class GeneralListView(ListView):
    model=GeneralTestResult
    template_name='general/general_list.html'
    context_object_name='general_results'

    def get_queryset(self):
        queryset=super().get_queryset()
        queryset=queryset.filter(result__isnull=False)
        return queryset

class GeneralRequestListView(ListView):
    model=GeneralTestResult
    template_name='general/general_request.html'
    context_object_name='general_request'

    def get_queryset(self):
        queryset=super().get_queryset()
        queryset=queryset.filter(result__isnull=True)
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

        micro_pays = Paypoint.objects.filter(micro_result_payment__isnull=False,unit__iexact='Microbiology').order_by('-updated')

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

        chempath_pays = Paypoint.objects.filter(chempath_result_payment__isnull=False,unit__iexact='Chemical Pathology').order_by('-updated')

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

        serology_pays = Paypoint.objects.filter(serology_result_payment__isnull=False,unit__iexact='Serology').order_by('-updated')

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


class BloodGroupCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name='Blood Group')
            
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
            
            # Create BloodGroup instance
            blood_group = BloodGroup.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'Blood Group test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating Blood Group test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


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
            
            # Create BloodGroup instance
            ue = UreaAndElectrolyte.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'UREA & ELCTROLYTE test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating UREA & ELCTROLYTE test: {str(e)}')
    
    
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))

class GenotypeCreateView(View):
    @transaction.atomic
    def get(self, request, file_no):
        try:
            patient = get_object_or_404(Patient, file_no=file_no)
            generic_test = get_object_or_404(GenericTest, name='Genotype')
            
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
            
            # Create BloodGroup instance
            geno = Genotype.objects.create(
                test=generic_test,
                test_info=test_info
            )

            messages.success(request, 'Genotype test created successfully')
        except Exception as e:
            messages.error(request, f'Error creating Genotype test: {str(e)}')
        
        return redirect(reverse('patient_details', kwargs={'file_no': file_no}))


class BaseLabResultUpdateView(UpdateView):
    template_name = 'shared_test_form.html'  # Adjust this to your template path

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

# class LiverFunctionCreateView(BaseTestCreateView):
#     model = LiverFunction
#     form_class = LiverFunctionForm

class UreaAndElectrolyteUpdateView(BaseLabResultUpdateView):
    model = UreaAndElectrolyte
    form_class = UreaAndElectrolyteForm


class BloodGroupUpdateView(BaseLabResultUpdateView):
    model = BloodGroup
    form_class = BloodGroupForm


class GenotypeUpdateView(BaseLabResultUpdateView):
    model = Genotype
    form_class = GenotypeForm


# class LiverFunctionUpdateView(BaseLabResultUpdateView):
#     model = LiverFunction
#     form_class = LiverFunctionForm
