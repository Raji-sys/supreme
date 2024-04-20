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
    path('update-patient/<int:patient_no>', PatientUpdateView.as_view(), name='update_patient'),
    path('patient/<str:surname>/', PatientDetailView.as_view(), name='patient_details'),

    
    path('hematology/', HematologyView.as_view(), name='hematology'),
    path('hematology-list/', HematologyListView.as_view(), name='hematology_list'),
    path('hematology-request/', HematologyRequestListView.as_view(), name='hematology_request'),
    path('hematology-result/create/<str:surname>/', HematologyResultCreateView.as_view(), name='hematology_result'),
    path('hematology-result/<str:surname>/<str:result_code>/update/', HematologyResultUpdateView.as_view(), name='hematology_update'),
    path('report/', ReportView.as_view(), name='report'),
    path('pdf/', views.report_pdf, name='report_pdf'),
   
    # path('chempath/', ChempathView.as_view(), name='chempath'),    
    # path('chem-path-result/<int:pk>',ChemicalPathologyResultCreateView.as_view(), name='chem_path_result'),
    # path('chem-path-result-update/<int:pk>',ChemicalPathologyResultUpdateView.as_view(), name='chem_path_update'),


    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', include('django.contrib.auth.urls')),
]