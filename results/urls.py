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
    path('profile/<str:username>/', ProfileDetailView.as_view(), name='profile_details'),

    path('create-patient/', PatientCreateView.as_view(), name='create_patient'),
    path('patients-list/', PatientListView.as_view(), name='patients_list'),
    path('update-patient/<int:pk>', PatientUpdateView.as_view(), name='update_patient'),
    path('patient/<str:surname>/', PatientDetailView.as_view(), name='patient_details'),

    
    path('hematology/', HematologyView.as_view(), name='hematology'),
    path('hematology-list/', HematologyListView.as_view(), name='hematology_list'),
    path('hematology-request/', HematologyRequestListView.as_view(), name='hematology_request'),
    path('hematology-test/create/<str:surname>/', HematologyTestCreateView.as_view(), name='hematology_test'),
    path('hematology-result/create/<str:surname>/<int:pk>/', HematologyResultCreateView.as_view(), name='hematology_result'),
    path('hematology-parameter/update/<int:pk>/', HemaParameterUpdateView.as_view(), name='hema_param'),
    path('hematology-report/', HemaReportView.as_view(), name='hema_report'),
    path('hematology-pdf/', views.hema_report_pdf, name='report_pdf'),
   
    path('chempath/', ChempathView.as_view(), name='chempath'),    
    path('chempath-list/',ChempathListView.as_view(),name='chempath_list'),
    path('chempath-request/',ChempathRequestListView.as_view(),name='chempath_request'),
    path('chempath-test/create/<str:surname>/',ChempathTestCreateView.as_view(), name='chempath_test'),
    path('chempath-result/create/<str:surname>/<int:pk>/',ChempathResultCreateView.as_view(), name='chempath_result'),
    path('chempath-parameter/update/<int:pk>/', ChempathParameterUpdateView.as_view(), name='chempath_param'),
    path('chempath-report/', ChempathReportView.as_view(), name='chempath_report'),
    path('chempath-pdf/', views.chempath_report_pdf, name='chempath_report_pdf'),

    path('micro/', MicrobiologyView.as_view(), name='micro'),    
    path('micro-list/',MicroListView.as_view(),name='micro_list'),
    path('micro-request/',MicroRequestListView.as_view(),name='micro_request'),
    path('micro-test/create/<str:surname>/',MicroTestCreateView.as_view(), name='micro_test'),
    path('micro-result/create/<str:surname>/<int:pk>/',MicroResultCreateView.as_view(), name='micro_result'),
    path('micro-parameter/update/<int:pk>/', MicroParameterUpdateView.as_view(), name='micro_param'),
    path('micro-report/', MicroReportView.as_view(), name='micro_report'),
    path('micro-pdf/', views.micro_report_pdf, name='micro_report_pdf'),
    
    path('serology/', SerologyView.as_view(), name='serology'),    
    path('serology-list/',SerologyListView.as_view(),name='serology_list'),
    path('serology-request/',SerologyRequestListView.as_view(),name='serology_request'),
    # path('serology-test/create/<str:surname>/',SerologyTestCreateView.as_view(), name='serology_test'),
    # path('serology-result/create/<str:surname>/<int:pk>/',SerologyResultCreateView.as_view(), name='serology_result'),
    path('serology-test/create/<str:surname>/', SerologyTestCreateView.as_view(), name='serology_test'),
    path('serology-result/create/<int:pk>/', SerologyParameterFormView.as_view(), name='serology_result'),
    path('serology-parameter/update/<int:pk>/', SerologyParameterUpdateView.as_view(), name='serology_param'),
    path('serology-report/', SerologyReportView.as_view(), name='serology_report'),
    path('serology-pdf/', views.serology_report_pdf, name='serology_report_pdf'),
    
    path('general/', GeneralView.as_view(), name='general'),    
    path('general-list/',GeneralListView.as_view(),name='general_list'),
    path('general-request/',GeneralRequestListView.as_view(),name='general_request'),
    path('general-test/create/<str:surname>/',GeneralTestCreateView.as_view(), name='general_test'),
    path('general-result/create/<str:surname>/<int:pk>/',GeneralResultCreateView.as_view(), name='general_result'),
    path('general-report/', GeneralReportView.as_view(), name='general_report'),
    path('general-pdf/', views.general_report_pdf, name='general_report_pdf'),
 
    # path('get_tests_for_category/',views.get_tests_for_category,name="get_tests_for_category"),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', include('django.contrib.auth.urls')),
]