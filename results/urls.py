from django.urls import path, include
from .views import *

urlpatterns = [

    path('', IndexView.as_view(), name='index'),
    
    path('login/', CustomLoginView.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('create-profile/', UserProfileCreateView.as_view(), name='create_profile'),
    path('update-profile/', UserProfileUpdateView.as_view(), name='update_profile'),

    path('create-patient/', PatientCreateView.as_view(), name='create_patient'),
    path('patients/', PatientListView.as_view(), name='patients_list'),
    path('update-patient/', PatientUpdateView.as_view(), name='update_patient'),
    path('patient/<int:pk>/', PatientDetailView.as_view(), name='patient_details'),

    path('hematology/', HematologyView.as_view(), name='hematology'),
    path('hametology-test/',HematologyTestCreateView.as_view(), name='hametology_test'),
    path('hametology-result/',HematologyResultCreateView.as_view(), name='hametology_result'),
    path('hametology-result-update/',HematologyResultUpdateView.as_view(), name='hametology_update'),

    path('chempath/', ChempathView.as_view(), name='chempath'),    
    path('chem-path-test/',HematologyTestCreateView.as_view(), name='chem_path_test'),
    path('chem-path-result/',HematologyResultCreateView.as_view(), name='chem_path_result'),
    path('chem-path-result-update/',HematologyResultUpdateView.as_view(), name='chem_path_update'),


    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', include('django.contrib.auth.urls')),
]