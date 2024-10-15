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

    # hematology 
    path('blood-group/create/<str:file_no>/', BloodGroupCreateView.as_view(), name='create_blood_group'),
    path('blood-group/update/<str:file_no>/<int:test_info_pk>/', BloodGroupUpdateView.as_view(), name='update_blood_group'),

    path('genotype/create/<str:file_no>/', GenotypeCreateView.as_view(), name='create_genotype'),
    path('genotype/update/<str:file_no>/<int:test_info_pk>/', GenotypeUpdateView.as_view(), name='update_genotype'),

    path('rhesus/create/<str:file_no>/', RhesusCreateView.as_view(), name='create_rhesus'),
    path('rhesus/update/<str:file_no>/<int:test_info_pk>/', RhesusUpdateView.as_view(), name='update_rhesus'),

    path('fbc/create/<str:file_no>/', FBCCreateView.as_view(), name='create_fbc'),
    path('fbc/update/<str:file_no>/<int:test_info_pk>/', FBCUpdateView.as_view(), name='update_fbc'),

    # chempath
    path('urea-electrolyte/create/<str:file_no>/', UECreateView.as_view(), name='create_urea_electrolyte'),
    path('urea-electrolyte/update/<str:file_no>/<int:test_info_pk>/', UreaAndElectrolyteUpdateView.as_view(), name='update_urea_electrolyte'),

    path('liver-function/create/<str:file_no>/', LiverFunctionCreateView.as_view(), name='create_liver_function'),
    path('liver-function/update/<str:file_no>/<int:test_info_pk>/', LiverFunctionUpdateView.as_view(), name='update_liver_function'),
    
    path('lipid-profile/create/<str:file_no>/', LipidProfileCreateView.as_view(), name='create_lipid_profile'),
    path('lipid-profile/update/<str:file_no>/<int:test_info_pk>/', LipidProfileUpdateView.as_view(), name='update_lipid_profile'),
    
    path('blood-glucose/create/<str:file_no>/', BloodGlucoseCreateView.as_view(), name='create_blood_glucose'),
    path('blood-glucose/update/<str:file_no>/<int:test_info_pk>/', BloodGlucoseUpdateView.as_view(), name='update_blood_glucose'),
    
    path('serum-proteins/create/<str:file_no>/', SerumProteinsCreateView.as_view(), name='create_serum_proteins'),
    path('serum-proteins/update/<str:file_no>/<int:test_info_pk>/', SerumProteinsUpdateView.as_view(), name='update_serum_proteins'),
    
    path('bone-chemistry/create/<str:file_no>/', BoneChemistryCreateView.as_view(), name='create_bone_chemistry'),
    path('bone-chemistry/update/<str:file_no>/<int:test_info_pk>/', BoneChemistryUpdateView.as_view(), name='update_bone_chemistry'),
    
    path('cerebro-spinal-fluid/create/<str:file_no>/', CerebroSpinalFluidCreateView.as_view(), name='create_cerebro_spinal_fluid'),
    path('cerebro-spinal-fluid/update/<str:file_no>/<int:test_info_pk>/', CerebroSpinalFluidUpdateView.as_view(), name='update_cerebro_spinal_fluid'),
    
    path('miscellaneous-chempath-tests/create/<str:file_no>/', MiscellaneousChempathTestsCreateView.as_view(), name='create_miscellaneous_chempath_tests'),
    path('miscellaneous-chempath-tests/update/<str:file_no>/<int:test_info_pk>/', MiscellaneousChempathTestsUpdateView.as_view(), name='update_miscellaneous_chempath_tests'),
    
    # serology 
    path('widal/create/<str:file_no>/', WidalCreateView.as_view(), name='create_widal'),
    path('widal/update/<str:file_no>/<int:test_info_pk>/', WidalUpdateView.as_view(), name='update_widal'),

    path('rheumatoid-factor/create/<str:file_no>/', RheumatoidFactorCreateView.as_view(), name='create_rheumatoid_factor'),
    path('rheumatoid-factor/update/<str:file_no>/<int:test_info_pk>/', RheumatoidFactorUpdateView.as_view(), name='update_rheumatoid_factor'),

    path('hepatitis-b/create/<str:file_no>/', HepatitisBCreateView.as_view(), name='create_hepatitis_b'),
    path('hepatitis-b/update/<str:file_no>/<int:test_info_pk>/', HepatitisBUpdateView.as_view(), name='update_hepatitis_b'),

    path('hepatitis-c/create/<str:file_no>/', HepatitisCCreateView.as_view(), name='create_hepatitis_c'),
    path('hepatitis-c/update/<str:file_no>/<int:test_info_pk>/', HepatitisCUpdateView.as_view(), name='update_hepatitis_c'),

    path('vdrl/create/<str:file_no>/', VDRLCreateView.as_view(), name='create_vdrl'),
    path('vdrl/update/<str:file_no>/<int:test_info_pk>/', VDRLUpdateView.as_view(), name='update_vdrl'),

    path('mantoux/create/<str:file_no>/', MantouxCreateView.as_view(), name='create_mantoux'),
    path('mantoux/update/<str:file_no>/<int:test_info_pk>/', MantouxUpdateView.as_view(), name='update_mantoux'),

    path('aso-titre/create/<str:file_no>/', AsoTitreCreateView.as_view(), name='create_aso_titre'),
    path('aso-titre/update/<str:file_no>/<int:test_info_pk>/', AsoTitreUpdateView.as_view(), name='update_aso_titre'),

    path('crp/create/<str:file_no>/', CRPCreateView.as_view(), name='create_crp'),
    path('crp/update/<str:file_no>/<int:test_info_pk>/', CRPUpdateView.as_view(), name='update_crp'),

    path('hiv-screening/create/<str:file_no>/', HIVScreeningCreateView.as_view(), name='create_hiv_screening'),
    path('hiv-screening/update/<str:file_no>/<int:test_info_pk>/', HIVScreeningUpdateView.as_view(), name='update_hiv_screening'),

    # microbiology
    
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    path('', include('django.contrib.auth.urls')),
]