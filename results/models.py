from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils import timezone
from django.core.exceptions import ValidationError
from django_quill.fields import QuillField



    
class SerialNumberField(models.CharField):
    description = "A unique serial number field with leading zeros"

    def __init__(self, *args, **kwargs):
        kwargs['unique'] = True
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["unique"]
        return name, path, args, kwargs


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    dep = (
        ('CHEMICAL PATHOLOGY', 'CHEMICAL PATHOLOGY'),
        ('HEMATOLOGY', 'HEMATOLOGY'),
        ('HISTOPATOLOGY', 'HISTOPATOLOGY'),
        ('MICROBIOLOGY', 'MICROBIOLOGY'),
        ('SEROLOGY', 'SEROLOGY'),
        ('OTHER', 'OTHER'),
    )
    department = models.CharField(choices=dep, blank=True, max_length=300, null=True)
    rank = (
        ('SCIENTIST', 'SCIENTIST'),
        ('TECHNICIAN', 'TECHNICIAN'),
        ('OTHER', 'OTHER'),
    )
    cadre = models.CharField(choices=rank, blank=True, max_length=300, null=True)
    created = models.DateTimeField('date added', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('profile_details', args=[self.user])

    def full_name(self):
        return f"{self.user.get_full_name()}"

    def __str__(self):
        if self.user:
            return f"{self.full_name()}"

        
class Patient(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    patient_no = SerialNumberField(default="", editable=False,max_length=20,null=False,blank=True)
    surname = models.CharField(max_length=300, blank=True, null=True)
    other_names = models.CharField(max_length=300, blank=True, null=True)
    sex = (('MALE', 'MALE'), ('FEMALE', 'FEMALE'))
    gender = models.CharField(choices=sex, max_length=10, null=True, blank=True)
    lab_no = models.CharField(max_length=10, null=True, blank=True)
    clinical_diagnosis = models.CharField(max_length=100, null=True, blank=True)
    hospital_clinic= models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField('date of birth', null=True, blank=True)
    phone = models.PositiveIntegerField(null=True, blank=True, unique=True)
    created = models.DateTimeField('date added', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.patient_no:
            last_instance = self.__class__.objects.order_by('patient_no').last()

            if last_instance:
                last_patient_no = int(last_instance.patient_no)
                new_patient_no = f"{last_patient_no + 1:07d}"  # 07 for 7 leading zeros
            else:
                new_patient_no = "0000001"

            self.patient_no = new_patient_no

        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('patient_details', args=[self.surname])

    def full_name(self):
        return f"{self.surname} {self.other_names}"

    def __str__(self):
        if self.surname:
            return f"{self.full_name()}"


class Paypoint(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    patient=models.ForeignKey(Patient,null=True, on_delete=models.CASCADE,related_name="patient_payments")
    service = models.CharField(max_length=100, null=True, blank=True)  
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    status=models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateField(auto_now=True)


class HematologyTest(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    reference_range = models.CharField(max_length=200, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.reference_range:
            return f"{self.name}, {self.reference_range}"
        else:
            return f"{self.name}"

class HematologyResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='hematology_result', null=True, blank=True)
    payment=models.ForeignKey(Paypoint,null=True, on_delete=models.CASCADE,related_name='hematology_result_payment')
    result_code = SerialNumberField(default="", editable=False,max_length=20,null=False,blank=True)
    test = models.ForeignKey(HematologyTest, max_length=100, null=True, blank=True, on_delete=models.CASCADE, related_name="results")
    cleared=models.BooleanField(default=False)
    result = QuillField(null=True, blank=True)
    comments=models.TextField(null=True, blank=True)
    natured_of_specimen = models.CharField(max_length=1-0, null=True, blank=True)
    collected = models.DateField(auto_now=True, null=True,blank=True)
    reported = models.DateField(auto_now=True, null=True, blank=True)
    collected_by = models.ForeignKey(User, null=True, blank=True, related_name='hematology_results_collected', on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name='hematology_results_reported', on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
 
    
    def save(self, *args, **kwargs):
        if not self.result_code:
            last_instance = self.__class__.objects.order_by('result_code').last()

            if last_instance:
                last_result_code = int(last_instance.result_code.removeprefix('HEM'))
                new_result_code = f"HEM{last_result_code + 1:03d}"
            else:
                new_result_code = "HEM001"

            self.result_code = new_result_code

        super().save(*args, **kwargs)

    def __str__(self):
        if self.patient:
            return f"{self.patient.full_name()} - {self.test} - {self.result}"
        

class ChempathTest(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    reference_range = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        if self.reference_range:
            return f"{self.name}, {self.reference_range}"
        else:
            return f"{self.name}"
    

class ChemicalPathologyResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='chemical_pathology_results',null=True, blank=True)
    payment=models.ForeignKey(Paypoint,null=True, on_delete=models.CASCADE,related_name='chempath_result_payment')
    result_code = SerialNumberField(default="", editable=False,max_length=20,null=False,blank=True)
    test = models.ForeignKey(ChempathTest, max_length=100, null=True, blank=True, on_delete=models.CASCADE, related_name="results")
    cleared=models.BooleanField(default=False)
    result = QuillField(null=True, blank=True)
    comments=models.TextField(null=True, blank=True)
    natured_of_specimen = models.CharField(max_length=1-0, null=True, blank=True)
    collected = models.DateField(auto_now=True, null=True,blank=True)
    reported = models.DateField(auto_now=True, null=True, blank=True)
    collected_by = models.ForeignKey(User, null=True, blank=True, related_name='chempath_results_collected', on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name='chempath_results_reported', on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    
    def save(self, *args, **kwargs):
        if not self.result_code:
            last_instance = self.__class__.objects.order_by('result_code').last()

            if last_instance:
                last_result_code = int(last_instance.result_code.removeprefix('CHP'))
                new_result_code = f"CHP{last_result_code + 1:03d}"
            else:
                new_result_code = "CHP001"

            self.result_code = new_result_code

        super().save(*args, **kwargs)

    def __str__(self):
        if self.patient:
            return f"{self.patient} - {self.test} - {self.result}"
    

class MicrobiologyTest(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    reference_range = models.CharField(max_length=200,null=True,blank=True)
    
    def __str__(self):
        if self.reference_range:
            return f"{self.name}, {self.reference_range}"
        else:
            return f"{self.name}"

class MicrobiologyResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='microbiology_results',null=True, blank=True)
    payment=models.ForeignKey(Paypoint,null=True, on_delete=models.CASCADE,related_name='micro_result_payment')
    result_code = SerialNumberField(default="", editable=False,max_length=20,null=False,blank=True)
    test = models.ForeignKey(MicrobiologyTest, on_delete=models.CASCADE, null=True, blank=True)
    cleared=models.BooleanField(default=False)
    result = QuillField(null=True, blank=True)
    comments=models.TextField(null=True, blank=True)
    natured_of_specimen = models.CharField(max_length=1-0, null=True, blank=True)
    collected = models.DateField(auto_now=True, null=True,blank=True)
    reported = models.DateField(auto_now=True, null=True, blank=True)
    collected_by = models.ForeignKey(User, null=True, blank=True, related_name='microbiology_results_collected', on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name='microbiology_results_reported', on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.result_code:
            last_instance = self.__class__.objects.order_by('result_code').last()

            if last_instance:
                last_result_code = int(last_instance.result_code.removeprefix('MIC'))
                new_result_code = f"MIC{last_result_code + 1:03d}"
            else:
                new_result_code = "MIC001"

            self.result_code = new_result_code

        super().save(*args, **kwargs)

    def __str__(self):
        if self.patient:
            return f"{self.patient} -{self.test} - {self.result}"


class SerologyTest(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    reference_range = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        if self.reference_range:
            return f"{self.name}, {self.reference_range}"
        else:
            return f"{self.name}"

class SerologyResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='serology_results', null=True, blank=True)
    payment=models.ForeignKey(Paypoint,null=True, on_delete=models.CASCADE,related_name='serology_result_payment')
    result_code = SerialNumberField(max_length=20, unique=True, editable=False, default="")
    test = models.ForeignKey(SerologyTest, on_delete=models.CASCADE, null=True, blank=True, related_name='results')
    cleared=models.BooleanField(default=False)
    result = QuillField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    nature_of_specimen = models.CharField(max_length=100, null=True, blank=True)
    collected = models.DateField(auto_now_add=True, null=True, blank=True)
    reported = models.DateField(auto_now=True, null=True, blank=True)
    collected_by = models.ForeignKey(User, null=True, blank=True, related_name='serology_results_collected', on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name='serology_results_reported', on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
 
    def save(self, *args, **kwargs):
        if not self.result_code:
            last_instance = SerologyResult.objects.order_by('result_code').last()
            if last_instance:
                last_result_code = int(last_instance.result_code.replace('SER', ''))
                new_result_code = f"SER{last_result_code + 1:03d}"
            else:
                new_result_code = "SER001"
            self.result_code = new_result_code
        super().save(*args, **kwargs)

    def __str__(self):
        parts = []
        if self.patient:
            parts.append(str(self.patient))
        if self.test:
            parts.append(str(self.test))
        if self.result:
            parts.append(str(self.result))
        return " - ".join(parts)

    def __str__(self):
        if self.patient:
            return f"{self.patient} - {self.test} - {self.result}"
        else:
            return f"{self.test} - {self.result}"


class GeneralTestResult(models.Model):
    name = models.CharField(max_length=100, null=True)
    payment=models.ForeignKey(Paypoint,null=True, on_delete=models.CASCADE,related_name='general_result_payment')
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='general_results', null=True, blank=True)
    result_code = SerialNumberField(default="", editable=False,max_length=20,null=False,blank=True)
    cleared=models.BooleanField(default=False)
    result = QuillField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    nature_of_specimen = models.CharField(max_length=100, null=True, blank=True)
    collected = models.DateField(auto_now_add=True, null=True, blank=True)
    reported = models.DateField(auto_now=True, null=True, blank=True)
    collected_by = models.ForeignKey(User, null=True, blank=True, related_name='general_results_collected', on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name='general_results_reported', on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        if self.patient:
            return f"{self.patient} -{self.test} - {self.result}"

    def save(self, *args, **kwargs):
        if not self.result_code:
            last_instance = self.__class__.objects.order_by('result_code').last()

            if last_instance:
                last_result_code = int(last_instance.result_code.removeprefix('GEN'))
                new_result_code = f"GEN{last_result_code + 1:03d}"
            else:
                new_result_code = "GEN001"

            self.result_code = new_result_code

        super().save(*args, **kwargs)

    def __str__(self):
        if self.patient:
            return f"{self.patient} - {self.name} - {self.result}"