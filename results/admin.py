from django import forms
from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
admin.site.unregister(User)

admin.site.site_header="ADMIN PANEL"
admin.site.index_title="PATHOLOGY MANAGEMENT SYSTEM"
admin.site.site_title="SUPREME DIAGNOSTIC LABORATORIES"

    
# Register the User model with custom Profile inlines
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)


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
    list_display = ('patient', 'test', 'result', 'unit', 'created','updated',)
    # list_filter = ('test', 'date_collected','date_reported','approved_by')
    # search_fields = ('patient__surname', 'patient__lab_no','patient__phone','approved_by')
    # list_per_page=10
    # ordering = ['test']

    # def save_model(self, request, obj, form, change):
    #     if not obj.approved_by:
    #         obj.approved_by=request.user
    #     obj.save()


@admin.register(ChempathTestName)
class ChempathTestNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'reference_range')


@admin.register(ChemicalPathologyResult)
class ChempathResultAdmin(admin.ModelAdmin):
    list_display = ('patient', 'test', 'result', 'unit', 'created','updated',)
    # list_filter = ('test', 'date_collected','date_reported','approved_by')
    # search_fields = ('patient__surname', 'patient__lab_no','patient__phone','approved_by')
    # list_per_page=10
    # ordering = ['test']

    # def save_model(self, request, obj, form, change):
    #     if not obj.approved_by:
    #         obj.approved_by=request.user
    #     obj.save()



@admin.register(MicrobiologyResult)
class MicroResultAdmin(admin.ModelAdmin):
    list_display = ('patient', 'test', 'result', 'unit', 'created','updated',)
    # list_filter = ('test', 'date_collected','date_reported','approved_by')
    # search_fields = ('patient__surname', 'patient__lab_no','patient__phone','approved_by')
    # list_per_page=10
    # ordering = ['test']

    # def save_model(self, request, obj, form, change):
    #     if not obj.approved_by:
    #         obj.approved_by=request.user
    #     obj.save()


@admin.register(MicrobiologyTest)
class MicroTestAdmin(admin.ModelAdmin):
    list_display = ('name','reference_range',)



class SerologyParameterInline(admin.StackedInline):
    model = SerologyParameter
    extra = 0
    list_filter = ('result__test', 'result__patient')


@admin.register(SerologyTestResult)
class SerologyTestResultAdmin(admin.ModelAdmin):
    inlines = [SerologyParameterInline]
    list_display = ('result_code', 'test', 'patient', 'result', 'unit', 'comments')
    list_filter = ('test', 'patient')

    def display_parameters(self, obj):
            return ", ".join([f"{p.result.test} {p.name}: {p.value}" for p in obj.parameters.all()])

    display_parameters.short_description = "Parameters"

@admin.register(SerologyTestName)
class SerologyTestNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'reference_range')

admin.site.register(SerologyParameter)