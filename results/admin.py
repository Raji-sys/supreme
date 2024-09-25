from .models import *
from django.contrib import admin

admin.site.site_header="ADMIN PANEL"
admin.site.index_title="PATHOLOGY MANAGEMENT SYSTEM"
admin.site.site_title="SUPREME DIAGNOSTIC LABORATORIES"

    
# Register the Patient model
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('surname', 'other_names', 'gender', 'dob', 'phone',)
    search_fields = ('surname',)
    list_filter = ('gender',)


@admin.register(HematologyTest)
class HematologyTestAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(HematologyResult)
class HematologyResultAdmin(admin.ModelAdmin):
    list_display = ('patient', 'test', 'result',  'created','updated',)
    # list_filter = ('test', 'date_collected','date_reported','approved_by')
    # search_fields = ('patient__surname', 'patient__lab_no','patient__phone','approved_by')
    # list_per_page=10
    # ordering = ['test']

@admin.register(ChempathTestName)
class ChempathTestNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'reference_range')


@admin.register(ChemicalPathologyResult)
class ChempathResultAdmin(admin.ModelAdmin):
    list_display = ('patient', 'test', 'result',  'created','updated',)
    # list_filter = ('test', 'date_collected','date_reported','approved_by')
    # search_fields = ('patient__surname', 'patient__lab_no','patient__phone','approved_by')
    # list_per_page=10
    # ordering = ['test']


@admin.register(MicrobiologyResult)
class MicroResultAdmin(admin.ModelAdmin):
    list_display = ('patient', 'test', 'result',  'created','updated',)
    # list_filter = ('test', 'date_collected','date_reported','approved_by')
    # search_fields = ('patient__surname', 'patient__lab_no','patient__phone','approved_by')
    # list_per_page=10
    # ordering = ['test']


@admin.register(MicrobiologyTest)
class MicroTestAdmin(admin.ModelAdmin):
    list_display = ('name','reference_range',)


@admin.register(SerologyTestResult)
class SerologyTestResultAdmin(admin.ModelAdmin):
    list_display = ('result_code', 'test', 'patient', 'result',  'comments')
    list_filter = ('test', 'patient')


@admin.register(SerologyTestName)
class SerologyTestNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'reference_range')