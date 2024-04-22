from django.urls import path, include
from .views import *
from . import views

urlpatterns = [

    path('', IndexView.as_view(), name='index'),
    
    path('login/', CustomLoginView.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

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
    path('hematology-report/', ReportView.as_view(), name='report'),
    path('hematology-pdf/', views.report_pdf, name='report_pdf'),
   
    path('chempath/', ChempathView.as_view(), name='chempath'),    
    path('chempath-list/',ChempathListView.as_view(),name='chempath_list'),
    path('chempath-request/',ChempathRequestListView.as_view(),name='chempath_request'),
    path('chempath-test/create/<str:surname>/',ChempathTestCreateView.as_view(), name='chempath_test'),
    path('chempath-result/create/<str:surname>/<int:pk>/',ChempathResultCreateView.as_view(), name='chempath_result'),

    path('chempath-report/', ChempathReportView.as_view(), name='chempath_report'),
    path('chempath-pdf/', views.chempath_report_pdf, name='chempath_report_pdf'),

    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', include('django.contrib.auth.urls')),
]