from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import *
User = get_user_model()
from django.forms import DateInput

class CustomUserCreationForm(UserCreationForm):
    department = forms.ChoiceField(choices=Profile.dep, required=False)
    cadre = forms.ChoiceField(choices=Profile.rank, required=False)

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'department', 'cadre']
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
            field.widget.attrs.update({'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'})


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name']
    
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'})


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['department', 'cadre']
    
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'})


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['surname', 'other_names', 'gender','age', 'phone','hospital_clinic']
    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=True 
            field.widget.attrs.update({'class':'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'})



class GeneralTestForm(forms.ModelForm):
    class Meta:
        model=GeneralTestResult
        fields=['name','price']

    def __init__(self, *args, **kwargs):
        super(GeneralTestForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'})

class GeneralTestResultForm(forms.ModelForm):
    class Meta:
        model=GeneralTestResult
        fields=['result','cleared','nature_of_specimen','comments']
    
    def __init__(self, *args, **kwargs):
        super(GeneralTestResultForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'})


class PayForm(forms.ModelForm):
    class Meta:
        model = Paypoint
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super(PayForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=True
            field.widget.attrs.update(
                {'class': 'text-center text-xs focus:outline-none border border-green-400 p-3 rounded shadow-lg focus:shadow-xl focus:border-green-200'})


class PayUpdateForm(forms.ModelForm):
    class Meta:
        model = Paypoint
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super(PayUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=True
            field.widget.attrs.update(
                {'class': 'text-center text-xs focus:outline-none border border-green-400 p-3 rounded shadow-lg focus:shadow-xl focus:border-green-200'})
            

class BloodGroupForm(forms.ModelForm):
    class Meta:
        model = BloodGroup
        fields = ['result']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        blood_group = super().save(commit=False)
        if commit:
            blood_group.save()
            test_info = blood_group.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return blood_group


class GenotypeForm(forms.ModelForm):
    class Meta:
        model = Genotype
        fields = ['result']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        genotype = super().save(commit=False)
        if commit:
            genotype.save()
            test_info = genotype.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return genotype


# class RhesusFactorForm(forms.ModelForm):
#     class Meta:
#         model = RhesusFactor
#         fields = ['rhesus_d']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self.instance and self.instance.test_info:
#             self.fields['nature_of_specimen'] = forms.CharField(
#                 initial=self.instance.test_info.nature_of_specimen,
#                 required=False
#             )
#             self.fields['cleared'] = forms.BooleanField(
#                 initial=self.instance.test_info.cleared,
#                 required=False
#             )
#         for field in self.fields.values():
#             field.widget.attrs.update({
#                 'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
#             })

#     def save(self, commit=True):
#         rhesus = super().save(commit=False)
#         if commit:
#             rhesus.save()
#             test_info = rhesus.test_info
#             test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
#             test_info.cleared = self.cleaned_data.get('cleared')
#             test_info.save()
#         return rhesus


class FBCForm(forms.ModelForm):
    class Meta:
        model = FBC
        exclude = ['test','test_info']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        fbc = super().save(commit=False)
        if commit:
            fbc.save()
            test_info = fbc.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return fbc
    

class UreaAndElectrolyteForm(forms.ModelForm):
    class Meta:
        model = UreaAndElectrolyte
        fields = ['urea', 'sodium', 'potassium', 'bicarbonate', 'chloride', 'creatinine']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        ue = super().save(commit=False)
        if commit:
            ue.save()
            test_info = ue.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return ue


class LiverFunctionForm(forms.ModelForm):
    class Meta:
        model = LiverFunction
        exclude = ['test','test_info']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        liver_function = super().save(commit=False)
        if commit:
            liver_function.save()
            test_info = liver_function.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return liver_function


class LipidProfileForm(forms.ModelForm):
    class Meta:
        model = LipidProfile
        exclude = ['test','test_info']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        lipid_profile = super().save(commit=False)
        if commit:
            lipid_profile.save()
            test_info = lipid_profile.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return lipid_profile


class LipidProfileForm(forms.ModelForm):
    class Meta:
        model = LipidProfile
        exclude = ['test','test_info']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        lipid_profile = super().save(commit=False)
        if commit:
            lipid_profile.save()
            test_info = lipid_profile.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return lipid_profile


class BloodGlucoseForm(forms.ModelForm):
    class Meta:
        model = BloodGlucose
        exclude = ['test','test_info']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        blood_glucose = super().save(commit=False)
        if commit:
            blood_glucose.save()
            test_info = blood_glucose.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return blood_glucose


class SerumProteinsForm(forms.ModelForm):
    class Meta:
        model = SerumProteins
        exclude = ['test','test_info']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        serum_proteins = super().save(commit=False)
        if commit:
            serum_proteins.save()
            test_info = serum_proteins.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return serum_proteins


class CerebroSpinalFluidForm(forms.ModelForm):
    class Meta:
        model = CerebroSpinalFluid
        exclude = ['test','test_info']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        cerebro_spinal_fluid = super().save(commit=False)
        if commit:
            cerebro_spinal_fluid.save()
            test_info = cerebro_spinal_fluid.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return cerebro_spinal_fluid


class BoneChemistryForm(forms.ModelForm):
    class Meta:
        model = BoneChemistry
        exclude = ['test','test_info']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        bone_chemistry = super().save(commit=False)
        if commit:
            bone_chemistry.save()
            test_info = bone_chemistry.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return bone_chemistry


class MiscellaneousChempathTestsForm(forms.ModelForm):
    class Meta:
        model = MiscellaneousChempathTests
        exclude = ['test','test_info']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        miscellaneous_chempath_tests = super().save(commit=False)
        if commit:
            miscellaneous_chempath_tests.save()
            test_info = miscellaneous_chempath_tests.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return miscellaneous_chempath_tests


class WidalForm(forms.ModelForm):
    class Meta:
        model = Widal
        exclude = ['test','test_info']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        widal = super().save(commit=False)
        if commit:
            widal.save()
            test_info = widal.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return widal


class HepatitisBForm(forms.ModelForm):
    class Meta:
        model = HPB
        exclude = ['test','test_info']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        hepatitis_b = super().save(commit=False)
        if commit:
            hepatitis_b.save()
            test_info = hepatitis_b.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return hepatitis_b



class HepatitisCForm(forms.ModelForm):
    class Meta:
        model = HCV
        exclude = ['test','test_info']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        hepatitis_c = super().save(commit=False)
        if commit:
            hepatitis_c.save()
            test_info = hepatitis_c.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return hepatitis_c


class VDRLForm(forms.ModelForm):
    class Meta:
        model = VDRL
        exclude = ['test','test_info']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        vdrl = super().save(commit=False)
        if commit:
            vdrl.save()
            test_info = vdrl.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return vdrl


class MantouxForm(forms.ModelForm):
    class Meta:
        model = Mantoux
        exclude = ['test','test_info']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        mantoux = super().save(commit=False)
        if commit:
            mantoux.save()
            test_info = mantoux.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return mantoux


class AsoTitreForm(forms.ModelForm):
    class Meta:
        model = AsoTitre
        exclude = ['test','test_info']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        aso_titre = super().save(commit=False)
        if commit:
            aso_titre.save()
            test_info = aso_titre.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return aso_titre


class CRPForm(forms.ModelForm):
    class Meta:
        model = CRP
        exclude = ['test','test_info']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        crp = super().save(commit=False)
        if commit:
            crp.save()
            test_info = crp.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return crp


class HIVScreeningForm(forms.ModelForm):
    class Meta:
        model = HIVScreening
        exclude = ['test','test_info']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        hiv_screening = super().save(commit=False)
        if commit:
            hiv_screening.save()
            test_info = hiv_screening.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return hiv_screening


class RheumatoidFactorForm(forms.ModelForm):
    class Meta:
        model = RheumatoidFactor
        exclude = ['test','test_info']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        rheumatoid_factor = super().save(commit=False)
        if commit:
            rheumatoid_factor.save()
            test_info = rheumatoid_factor.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return rheumatoid_factor


class UrineMicroscopyForm(forms.ModelForm):
    class Meta:
        model = UrineMicroscopy
        exclude = ['test','test_info']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        urine_microscopy = super().save(commit=False)
        if commit:
            urine_microscopy.save()
            test_info = urine_microscopy.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return urine_microscopy


class HVSForm(forms.ModelForm):
    class Meta:
        model = HVS
        exclude = ['test','test_info']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        hvs = super().save(commit=False)
        if commit:
            hvs.save()
            test_info = hvs.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return hvs


class StoolForm(forms.ModelForm):
    class Meta:
        model = Stool
        exclude = ['test','test_info']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        stool = super().save(commit=False)
        if commit:
            stool.save()
            test_info = stool.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return stool


class Swab_pus_asiprate_mcsForm(forms.ModelForm):
    class Meta:
        model = Swab_Pus_Aspirate_MCS
        exclude = ['test','test_info']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        swap_pus_aspirate = super().save(commit=False)
        if commit:
            swap_pus_aspirate.save()
            test_info = swap_pus_aspirate.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return swap_pus_aspirate

class BloodCultureForm(forms.ModelForm):
    class Meta:
        model = BloodCulture
        exclude = ['test','test_info']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        blood_culture = super().save(commit=False)
        if commit:
            blood_culture.save()
            test_info = blood_culture.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return blood_culture


class OccultBloodForm(forms.ModelForm):
    class Meta:
        model = OccultBlood
        exclude = ['test','test_info']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        occult_blood = super().save(commit=False)
        if commit:
            occult_blood.save()
            test_info = occult_blood.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return occult_blood


class SputumMCSForm(forms.ModelForm):
    class Meta:
        model = SputumMCS
        exclude = ['test','test_info']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        sputum_mcs = super().save(commit=False)
        if commit:
            sputum_mcs.save()
            test_info = sputum_mcs.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return sputum_mcs


class GramStainForm(forms.ModelForm):
    class Meta:
        model = GramStain
        exclude = ['test','test_info']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        gram_stain = super().save(commit=False)
        if commit:
            gram_stain.save()
            test_info = gram_stain.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return gram_stain


class ZNStainForm(forms.ModelForm):
    class Meta:
        model = ZNStain
        exclude = ['test','test_info']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        zn_stain = super().save(commit=False)
        if commit:
            zn_stain.save()
            test_info = zn_stain.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return zn_stain


class SemenAnalysisForm(forms.ModelForm):
    class Meta:
        model = SemenAnalysis
        exclude = ['test','test_info']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        semen_analysis = super().save(commit=False)
        if commit:
            semen_analysis.save()
            test_info = semen_analysis.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return semen_analysis


class UrinalysisForm(forms.ModelForm):
    class Meta:
        model = Urinalysis
        exclude = ['test','test_info']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        urinalysis = super().save(commit=False)
        if commit:
            urinalysis.save()
            test_info = urinalysis.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return urinalysis


class PregnancyForm(forms.ModelForm):
    class Meta:
        model = Pregnancy
        exclude = ['test','test_info']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.test_info:
            self.fields['nature_of_specimen'] = forms.CharField(
                initial=self.instance.test_info.nature_of_specimen,
                required=False
            )
            self.fields['cleared'] = forms.BooleanField(
                initial=self.instance.test_info.cleared,
                required=False
            )
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

    def save(self, commit=True):
        pregnancy = super().save(commit=False)
        if commit:
            pregnancy.save()
            test_info = pregnancy.test_info
            test_info.nature_of_specimen = self.cleaned_data.get('nature_of_specimen')
            test_info.cleared = self.cleaned_data.get('cleared')
            test_info.save()
        return pregnancy