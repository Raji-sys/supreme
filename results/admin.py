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


# @admin.register(AsoTitre)
# class Testingdmin(admin.ModelAdmin):
#     list_display = ('id',)

@admin.register(Paypoint)
class PaypointAdmin(admin.ModelAdmin):
    list_display = ('patient','service','price','status')


@admin.register(GenericTest)
class GenericTestAdmin(admin.ModelAdmin):
    list_display = ('lab','name', 'price')
    search_fields = ('lab','name','price')
    list_filter = ('lab','name','price')


@admin.register(Testinfo)
class TestinfoAdmin(admin.ModelAdmin):
    list_display = ('patient', 'payment_status', 'code', 'test_lab', 'test_name', 'test_price')

    @admin.display(ordering='payment__unit', description='Lab')
    def test_lab(self, obj):
        return obj.payment.unit if obj.payment.unit else ''
    
    @admin.display(ordering='payment__unit', description='Test')
    def test_name(self, obj):
        return obj.payment.service if obj.payment.service else ''

    @admin.display(ordering='payment__price', description='Cost')
    def test_price(self, obj):
        return obj.payment.price if obj.payment.price else ''

    @admin.display(ordering='payment__status', description='Payment')
    def payment_status(self, obj):
        return obj.payment.status if obj.payment.status else ''
