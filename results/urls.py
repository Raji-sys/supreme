from django.urls import path, include
from .views import *
from . import views

urlpatterns = [

    path('', IndexView.as_view(), name='index'),
    
    path('login/', CustomLoginView.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('report/', ReportView.as_view(), name='report'),

    path('create-profile/', UserProfileCreateView.as_view(), name='create_profile'),
    path('profile-list/', ProfileListView.as_view(), name='profiles_list'),

    path('create-patient/', PatientCreateView.as_view(), name='create_patient'),
    path('patients-list/', PatientListView.as_view(), name='patients_list'),
    path('update-patient/<int:pk>', PatientUpdateView.as_view(), name='update_patient'),
    path('patient/<str:file_no>/', PatientDetailView.as_view(), name='patient_details'),

    path('get-started/revenue', RevenueView.as_view(), name='revenue'),
    
    path('revenue/update-payment/<int:pk>/', PayUpdateView.as_view(), name='update_pay'),
    path('revenue/add-payment/', PayCreateView.as_view(), name='add_pay'),
    path('revenue/hema-list/', HemaPayListView.as_view(), name='hema_pay_list'),
    path('revenue/micro-list/', MicroPayListView.as_view(), name='micro_pay_list'),
    path('revenue/chempath-list/', ChempathPayListView.as_view(), name='chempath_pay_list'),
    path('revenue/serology-list/', SerologyPayListView.as_view(), name='serology_pay_list'),
    path('revenue/general-list/', GeneralPayListView.as_view(), name='general_pay_list'),
    path('revenue/receipt/', views.receipt_pdf, name='receipt_pdf'),
    path('revenue/payment-list/', PayListView.as_view(), name='pay_list'),

    path('hematology/', HematologyView.as_view(), name='hematology'),
    path('hematology-list/', HematologyListView.as_view(), name='hematology_list'),
    path('hematology-request/', HematologyRequestListView.as_view(), name='hematology_request'),
    path('hematology-test/create/<str:file_no>/', HematologyTestCreateView.as_view(), name='hematology_test'),
    path('hematology-result/create/<str:file_no>/<int:pk>/', HematologyResultCreateView.as_view(), name='hematology_result'),
    path('hematology-report/', HemaReportView.as_view(), name='hema_report'),
    path('hematology-pdf/', views.hema_report_pdf, name='report_pdf'),
   
    path('chempath/', ChempathView.as_view(), name='chempath'),    
    path('chempath-list/',ChempathListView.as_view(),name='chempath_list'),
    path('chempath-request/',ChempathRequestListView.as_view(),name='chempath_request'),
    path('chempath-test/create/<str:file_no>/',ChempathTestCreateView.as_view(), name='chempath_test'),
    path('chempath-result/create/<str:file_no>/<int:pk>/',ChempathResultCreateView.as_view(), name='chempath_result'),
    path('chempath-report/', ChempathReportView.as_view(), name='chempath_report'),
    path('chempath-pdf/', views.chempath_report_pdf, name='chempath_report_pdf'),

    path('micro/', MicrobiologyView.as_view(), name='micro'),    
    path('micro-list/',MicroListView.as_view(),name='micro_list'),
    path('micro-request/',MicroRequestListView.as_view(),name='micro_request'),
    path('micro-test/create/<str:file_no>/',MicroTestCreateView.as_view(), name='micro_test'),
    path('micro-result/create/<str:file_no>/<int:pk>/',MicroResultCreateView.as_view(), name='micro_result'),
    path('micro-report/', MicroReportView.as_view(), name='micro_report'),
    path('micro-pdf/', views.micro_report_pdf, name='micro_report_pdf'),
    
    path('serology/', SerologyView.as_view(), name='serology'),    
    path('serology-list/',SerologyListView.as_view(),name='serology_list'),
    path('serology-request/',SerologyRequestListView.as_view(),name='serology_request'),
    path('serology-test/create/<str:file_no>/', SerologyTestCreateView.as_view(), name='serology_test'),
    path('serology-result/create/<str:file_no>/<int:pk>/', SerologyResultCreateView.as_view(), name='serology_result'),
    path('serology-report/', SerologyReportView.as_view(), name='serology_report'),
    path('serology-pdf/', views.serology_report_pdf, name='serology_report_pdf'),
    
    path('general/', GeneralView.as_view(), name='general'),    
    path('general-list/',GeneralListView.as_view(),name='general_list'),
    path('general-request/',GeneralRequestListView.as_view(),name='general_request'),
    path('general-test/create/<str:file_no>/',GeneralTestCreateView.as_view(), name='general_test'),
    path('general-result/create/<str:file_no>/<int:pk>/',GeneralResultCreateView.as_view(), name='general_result'),
    path('general-report/', GeneralReportView.as_view(), name='general_report'),
    path('general-pdf/', views.general_report_pdf, name='general_report_pdf'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', include('django.contrib.auth.urls')),
]