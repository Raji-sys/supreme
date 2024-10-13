from django.urls import path, include
from .views import *
from . import views

urlpatterns = [

    path('', IndexView.as_view(), name='index'),
    
    path('login/', CustomLoginView.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('report/', ReportView.as_view(), name='report'),
    path('print-pdf/', views.report_pdf, name='report_pdf'),

    path('create-profile/', UserProfileCreateView.as_view(), name='create_profile'),
    path('profiles/<int:pk>/update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/<int:pk>/delete/', UserDeleteView.as_view(), name='profile-delete'), 
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
   
   
    path('chempath/', ChempathView.as_view(), name='chempath'),    
    path('chempath-list/',ChempathListView.as_view(),name='chempath_list'),
    path('chempath-request/',ChempathRequestListView.as_view(),name='chempath_request'),

    path('micro/', MicrobiologyView.as_view(), name='micro'),    
    path('micro-list/',MicroListView.as_view(),name='micro_list'),
    path('micro-request/',MicroRequestListView.as_view(),name='micro_request'),
    
    path('serology/', SerologyView.as_view(), name='serology'),    
    path('serology-list/',SerologyListView.as_view(),name='serology_list'),
    path('serology-request/',SerologyRequestListView.as_view(),name='serology_request'),
    
    path('general/', GeneralView.as_view(), name='general'),    
    path('general-list/',GeneralListView.as_view(),name='general_list'),
    path('general-request/',GeneralRequestListView.as_view(),name='general_request'),
    path('general-test/create/<str:file_no>/',GeneralTestCreateView.as_view(), name='general_test'),
    path('general-result/create/<str:file_no>/<int:pk>/',GeneralResultCreateView.as_view(), name='general_result'),
    path('general-report/', GeneralReportView.as_view(), name='general_report'),
    path('general-pdf/', views.general_report_pdf, name='general_report_pdf'),

    path('blood-group/create/<str:file_no>/', BloodGroupCreateView.as_view(), name='create_blood_group'),
    path('blood-group/update/<str:file_no>/<int:test_info_pk>/', BloodGroupUpdateView.as_view(), name='update_blood_group'),

    path('urea-electrolyte/create/<str:file_no>/', views.UECreateView.as_view(), name='create_urea_electrolyte'),
    path('urea-electrolyte/update/<str:file_no>/<int:test_info_pk>/', UreaAndElectrolyteUpdateView.as_view(), name='update_urea_electrolyte'),


    path('genotype/create/<str:file_no>/', GenotypeCreateView.as_view(), name='create_genotype'),
    path('genotype/update/<str:file_no>/<int:test_info_pk>/', GenotypeUpdateView.as_view(), name='update_genotype'),

    path('rhesus/create/<str:file_no>/', RhesusCreateView.as_view(), name='create_rhesus'),
    path('rhesus/update/<str:file_no>/<int:test_info_pk>/', RhesusUpdateView.as_view(), name='update_rhesus'),

    path('fbc/create/<str:file_no>/', FBCCreateView.as_view(), name='create_fbc'),
    path('fbc/update/<str:file_no>/<int:test_info_pk>/', FBCUpdateView.as_view(), name='update_fbc'),

    # path('liver-function/create/<str:file_no>/', views.LiverFunctionCreateView.as_view(), name='create_liver_function'),
    # path('liver-function/update/<str:file_no>/<int:pk>/', views.LiverFunctionUpdateView.as_view(), name='update_liver_function'),
    
    

    path('logout/', CustomLogoutView.as_view(), name='logout'),

    path('', include('django.contrib.auth.urls')),
]