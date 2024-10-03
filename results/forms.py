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
            field.widget.attrs.update({'class': 'text-center mt-2 text-xs focus:outline-none py-2 rounded-md'})


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name']
    
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'text-center mt-2 text-xs focus:outline-none py-2 rounded-md'})


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['department', 'cadre']
    
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'text-center mt-2 text-xs focus:outline-none py-2 rounded-md'})


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['surname', 'other_names', 'gender','dob', 'phone']
        widgets = {
            'dob': DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False 
            field.widget.attrs.update({'class':'text-center mt-2 text-xs focus:outline-none py-2 rounded-md'})


class HematologyTestForm(forms.ModelForm):
    class Meta:
        model = HematologyResult
        fields = ['test']
    
    def __init__(self, *args, **kwargs):
        super(HematologyTestForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center mt-2 text-xs focus:outline-none py-2 rounded-md'})


class HematologyResultForm(forms.ModelForm):
    class Meta:
        model = HematologyResult
        fields = ['test', 'result','cleared','nature_of_specimen']
    
    def __init__(self, *args, **kwargs):
        super(HematologyResultForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center mt-2 text-xs focus:outline-none py-2 rounded-md'})



class ChempathTestForm(forms.ModelForm):
    class Meta:
        model = ChemicalPathologyResult
        fields = ['test']
    
    def __init__(self, *args, **kwargs):
        super(ChempathTestForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center mt-2 text-xs focus:outline-none py-2 rounded-md'})


class ChempathResultForm(forms.ModelForm):
    class Meta:
        model = ChemicalPathologyResult
        fields = ['test', 'result','cleared','nature_of_specimen']

    def __init__(self, *args, **kwargs):
        super(ChempathResultForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center mt-2 text-xs focus:outline-none py-2 rounded-md'})


class MicroTestForm(forms.ModelForm):
    class Meta:
        model = MicrobiologyResult
        fields = ['test']

    def __init__(self, *args, **kwargs):
        super(MicroTestForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center mt-2 text-xs focus:outline-none py-2 rounded-md'})

class MicroResultForm(forms.ModelForm):
    class Meta:
        model = MicrobiologyResult
        fields = ['test', 'result','cleared','nature_of_specimen']
    
    def __init__(self, *args, **kwargs):
        super(MicroResultForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center mt-2 text-xs focus:outline-none py-2 rounded-md'})


class SerologyTestForm(forms.ModelForm):
    class Meta:
        model = SerologyResult
        fields = ['test']

    def __init__(self, *args, **kwargs):
        super(SerologyTestForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center mt-2 text-xs focus:outline-none py-2 rounded-md'})

class SerologyResultForm(forms.ModelForm):
    class Meta:
        model = SerologyResult
        fields = ['test','result','cleared','nature_of_specimen']
    
    def __init__(self, *args, **kwargs):
        super(SerologyResultForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center mt-2 text-xs focus:outline-none py-2 rounded-md'})


class GeneralTestForm(forms.ModelForm):
    class Meta:
        model=GeneralTestResult
        fields=['name','price']

    def __init__(self, *args, **kwargs):
        super(GeneralTestForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center mt-2 text-xs focus:outline-none py-2 rounded-md'})

class GeneralTestResultForm(forms.ModelForm):
    class Meta:
        model=GeneralTestResult
        fields=['result','cleared','nature_of_specimen']
    
    def __init__(self, *args, **kwargs):
        super(GeneralTestResultForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center mt-2 text-xs focus:outline-none py-2 rounded-md'})


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