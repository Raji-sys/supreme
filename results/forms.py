from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import *
User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    middle_name = forms.CharField(max_length=30, required=False)
    department = forms.ChoiceField(choices=Profile.dep, required=False)
    cadre = forms.ChoiceField(choices=Profile.rank, required=False)

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name',
                  'last_name', 'password1', 'password2']
        
class UserProfileForm(UserCreationForm):
    middle_name = forms.CharField(max_length=300, required=False)
    department = forms.ChoiceField(choices=Profile.dep, required=False)
    cadre = forms.ChoiceField(choices=Profile.rank, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Profile.objects.create(user=user, middle_name=self.cleaned_data["middle_name"], department=self.cleaned_data["department"], cadre=self.cleaned_data["cadre"])
        return user


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['surname', 'other_names', 'gender', 'phone']


class HematologyTestForm(forms.ModelForm):
    class Meta:
        model = HematologyResult
        fields = ['test']


class HematologyResultForm(forms.ModelForm):
    class Meta:
        model = HematologyResult
        fields = ['test', 'result', 'unit']


class ChempathTestForm(forms.ModelForm):
    class Meta:
        model = ChemicalPathologyResult
        fields = ['test']


class ChempathResultForm(forms.ModelForm):
    class Meta:
        model = ChemicalPathologyResult
        fields = ['test', 'result', 'unit']


class MicroTestForm(forms.ModelForm):
    class Meta:
        model = MicrobiologyResult
        fields = ['category','test']

    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['test'].queryset=MicrobiologyTest.objects.all()
        for field in self.fields.values():
            field.required=True

    def clean(self):
        cleaned_data=super().clean()
        category=cleaned_data.get('category')
        test=cleaned_data.get('test')

class MicroResultForm(forms.ModelForm):
    class Meta:
        model = MicrobiologyResult
        fields = ['category','test', 'result', 'unit']


class SerologyTestForm(forms.ModelForm):
    class Meta:
        model = SerologyTestResult
        fields = ['test',]


class SerologyParameterForm(forms.ModelForm):
    class Meta:
        model = SerologyParameter
        fields = ['name', 'value']


class GeneralTestForm(forms.ModelForm):
    class Meta:
        model=GeneralTestResult
        fields=['name']


class GeneralTestResultForm(forms.ModelForm):
    class Meta:
        model=GeneralTestResult
        fields=['result','unit','comments']