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
        fields = ['surname', 'other_names', 'gender','age', 'phone']
    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=True 
            field.widget.attrs.update({'class':'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'})


class HematologyTestForm(forms.ModelForm):
    class Meta:
        model = HematologyResult
        fields = ['test']
    
    def __init__(self, *args, **kwargs):
        super(HematologyTestForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'})


class HematologyResultForm(forms.ModelForm):
    class Meta:
        model = HematologyResult
        fields = ['test', 'result','cleared','nature_of_specimen']
    
    def __init__(self, *args, **kwargs):
        super(HematologyResultForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'})



class ChempathTestForm(forms.ModelForm):
    class Meta:
        model = ChemicalPathologyResult
        fields = ['test']
    
    def __init__(self, *args, **kwargs):
        super(ChempathTestForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'})


class ChempathResultForm(forms.ModelForm):
    class Meta:
        model = ChemicalPathologyResult
        fields = ['test', 'result','cleared','nature_of_specimen']

    def __init__(self, *args, **kwargs):
        super(ChempathResultForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'})


class MicroTestForm(forms.ModelForm):
    class Meta:
        model = MicrobiologyResult
        fields = ['test']

    def __init__(self, *args, **kwargs):
        super(MicroTestForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'})

class MicroResultForm(forms.ModelForm):
    class Meta:
        model = MicrobiologyResult
        fields = ['test', 'result','cleared','nature_of_specimen']
    
    def __init__(self, *args, **kwargs):
        super(MicroResultForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'})


class SerologyTestForm(forms.ModelForm):
    class Meta:
        model = SerologyResult
        fields = ['test']

    def __init__(self, *args, **kwargs):
        super(SerologyTestForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'})

class SerologyResultForm(forms.ModelForm):
    class Meta:
        model = SerologyResult
        fields = ['test','result','cleared','nature_of_specimen']
    
    def __init__(self, *args, **kwargs):
        super(SerologyResultForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
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
        fields=['result','cleared','nature_of_specimen']
    
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
            

class UreaAndElectrolyteTestForm(forms.ModelForm):
    class Meta:
        model = UreaAndElectrolyte
        fields = ['test']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })


class LiverFunctionForm(forms.ModelForm):
    class Meta:
        model = LiverFunction
        fields = ['alkaline_phosphatase', 'sgot', 'sgpt', 'gamma_gt', 'total_bilirubin', 'direct_bilirubin']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

class BloodGroupTestForm(forms.ModelForm):
    class Meta:
        model = BloodGroup
        fields = ['test']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
            field.widget.attrs.update({
                'class': 'text-center text-xs focus:outline-none border border-green-400 p-2 rounded shadow-lg focus:shadow-xl focus:border-green-200'
            })

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
    

class UreaAndElectrolyteForm(forms.ModelForm):
    class Meta:
        model = UreaAndElectrolyte
        fields = ['urea', 'sodium', 'potassium', 'bicarbonate', 'chloride', 'caretinine']
    
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