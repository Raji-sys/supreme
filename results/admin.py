from .models import *
from django.contrib import admin

admin.site.site_header="ADMIN PANEL"
admin.site.index_title="PATHOLOGY MANAGEMENT SYSTEM"
admin.site.site_title="SUPREME DIAGNOSTIC LABORATORIES"



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=('user','department','cadre')
    search_fields = ('user',)
    search_fields = ('cadre','department')


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('surname', 'other_names', 'gender', 'age', 'phone',)
    search_fields = ('surname',)
    list_filter = ('gender',)


# @admin.register(GeneralTestResult)
# class GeneralAdmin(admin.ModelAdmin):
#     list_display = ('name', 'price')

@admin.register(Paypoint)
class PaypointAdmin(admin.ModelAdmin):
    list_display = ('patient','service','price','status')


@admin.register(GenericTest)
class GenericTestAdmin(admin.ModelAdmin):
    list_display = ('lab','name', 'price','reference_range')


@admin.register(Testinfo)
class TestinfoAdmin(admin.ModelAdmin):
    list_display = ('patient', 'payment_status', 'code', 'test_lab', 'test_price')

    @admin.display(ordering='test__lab__name', description='Lab')
    def test_lab(self, obj):
        return obj.test.lab.name if obj.test.lab else ''

    @admin.display(ordering='test__price', description='Cost')
    def test_price(self, obj):
        return obj.test.price if obj.test.price else ''

    @admin.display(ordering='payment__status', description='Payment')
    def payment_status(self, obj):
        return obj.payment.status if obj.payment.status else ''
