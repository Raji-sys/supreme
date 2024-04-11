from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import *
User = get_user_model()


class UserProfileForm(UserCreationForm):
    middle_name = forms.CharField(max_length=300, required=False)
    department = forms.ChoiceField(choices=Profile.dep, required=False)
    cadre = forms.ChoiceField(choices=Profile.rank, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            Profile.objects.create(user=user, middle_name=self.cleaned_data["middle_name"], department=self.cleaned_data["department"], cadre=self.cleaned_data["cadre"])
        return user


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['surname', 'other_names', 'gender', 'dob', 'phone']


class HematologyTestForm(forms.ModelForm):
    class Meta:
        model = HematologyTest
        fields = ['name', 'reference_range']


class HematologyResultForm(forms.ModelForm):
    class Meta:
        model = HematologyResult
        fields = ['approved_by', 'patient', 'test', 'result', 'unit']


class ChemicalPathologyTestForm(forms.ModelForm):
    class Meta:
        model = ChemicalPathologyTest
        fields = ['name', 'reference_range']


class ChemicalPathologyResultForm(forms.ModelForm):
    class Meta:
        model = ChemicalPathologyResult
        fields = ['approved_by', 'patient', 'test', 'result', 'unit']