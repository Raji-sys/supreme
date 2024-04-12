from django.urls import path, include
from .views import *

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
    path('hematology-result/create/<str:surname>/', HematologyResultCreateView.as_view(), name='hematology_result'),
    path('hematology-result/<str:surname>/<int:pk>/update/', HematologyResultUpdateView.as_view(), name='hematology_update'),
   
    # path('chempath/', ChempathView.as_view(), name='chempath'),    
    # path('chem-path-result/<int:pk>',ChemicalPathologyResultCreateView.as_view(), name='chem_path_result'),
    # path('chem-path-result-update/<int:pk>',ChemicalPathologyResultUpdateView.as_view(), name='chem_path_update'),


    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', include('django.contrib.auth.urls')),
]