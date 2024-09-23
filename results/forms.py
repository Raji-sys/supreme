from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import *
User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    department = forms.ChoiceField(choices=Profile.dep, required=False)
    cadre = forms.ChoiceField(choices=Profile.rank, required=False)

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name',
                  'last_name', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center mt-2 text-xs focus:outline-none py-2 rounded-md'})


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['surname', 'other_names', 'gender', 'phone']
    
    def __init__(self, *args, **kwargs):
        super(Patient, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center mt-2 text-xs focus:outline-none py-2 rounded-md'})


class HematologyTestForm(forms.ModelForm):
    class Meta:
        model = HematologyResult
        fields = ['test']
    
    def __init__(self, *args, **kwargs):
        super(HematologyResult, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center mt-2 text-xs focus:outline-none py-2 rounded-md'})


class HematologyResultForm(forms.ModelForm):
    class Meta:
        model = HematologyResult
        fields = ['test', 'result', 'unit']
    
    def __init__(self, *args, **kwargs):
        super(HematologyResult, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center mt-2 text-xs focus:outline-none py-2 rounded-md'})



class ChempathTestForm(forms.ModelForm):
    class Meta:
        model = ChemicalPathologyResult
        fields = ['test']
    
    def __init__(self, *args, **kwargs):
        super(ChemicalPathologyResult, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center mt-2 text-xs focus:outline-none py-2 rounded-md'})


class ChempathResultForm(forms.ModelForm):
    class Meta:
        model = ChemicalPathologyResult
        fields = ['test', 'result', 'unit']

    def __init__(self, *args, **kwargs):
        super(ChemicalPathologyResult, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center mt-2 text-xs focus:outline-none py-2 rounded-md'})


class MicroTestForm(forms.ModelForm):
    class Meta:
        model = MicrobiologyResult
        fields = ['test']

    def __init__(self, *args, **kwargs):
        super(MicrobiologyResult, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center mt-2 text-xs focus:outline-none py-2 rounded-md'})

class MicroResultForm(forms.ModelForm):
    class Meta:
        model = MicrobiologyResult
        fields = ['test', 'result', 'unit']
    
    def __init__(self, *args, **kwargs):
        super(MicrobiologyResult, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center mt-2 text-xs focus:outline-none py-2 rounded-md'})


class SerologyTestForm(forms.ModelForm):
    class Meta:
        model = SerologyTestResult
        fields = ['test']

    def __init__(self, *args, **kwargs):
        super(SerologyTestResult, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center mt-2 text-xs focus:outline-none py-2 rounded-md'})

class SerologyTestResultForm(forms.ModelForm):
    class Meta:
        model = SerologyTestResult
        fields = ['test','result']
    
    def __init__(self, *args, **kwargs):
        super(SerologyTestResult, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center mt-2 text-xs focus:outline-none py-2 rounded-md'})


class GeneralTestForm(forms.ModelForm):
    class Meta:
        model=GeneralTestResult
        fields=['name']

    def __init__(self, *args, **kwargs):
        super(GeneralTestResult, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center mt-2 text-xs focus:outline-none py-2 rounded-md'})

class GeneralTestResultForm(forms.ModelForm):
    class Meta:
        model=GeneralTestResult
        fields=['result','unit','comments']
    
    def __init__(self, *args, **kwargs):
        super(GeneralTestResult, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required=False    
            field.widget.attrs.update({'class':'text-center mt-2 text-xs focus:outline-none py-2 rounded-md'})