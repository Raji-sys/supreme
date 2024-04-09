from django import forms
from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
admin.site.unregister(User)

admin.site.site_header="ADMIN PANEL"
admin.site.index_title="PATHOLOGY MANAGEMENT SYSTEM"
admin.site.site_title="SUPREME DIAGNOSTIC LABORATORIES"

    

@admin.register(HematologyResult)
class HematologyResultAdmin(admin.ModelAdmin):
    list_display = ('patient', 'test', 'result', 'unit', 'date_collected','date_reported')
    list_filter = ('test', 'date_collected','date_reported','approved_by')
    search_fields = ('patient__surname', 'patient__lab_no','patient__phone','approved_by')
    list_per_page=10
    ordering = ['test']

    def save_model(self, request, obj, form, change):
        if not obj.lab_user:
            obj.lab_user=request.user
        obj.save()


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
    list_display = ('full_name', 'gender', 'dob', 'phone')
    search_fields = ('first_name', 'last_name', 'other_name')
    list_filter = ('gender',)


# Register the HematologyTest model
@admin.register(HematologyTest)
class HematologyTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'reference_range')

