from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils import timezone
from django.core.exceptions import ValidationError
from django_quill.fields import QuillField
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.validators import MinValueValidator, MaxValueValidator


    
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

    def full_name(self):
        return f"{self.user.get_full_name()}"

    def __str__(self):
        if self.user:
            return f"{self.full_name()}"

        
class Patient(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    file_no = SerialNumberField(default="", editable=False,max_length=20,null=False,blank=True)
    surname = models.CharField(max_length=300, blank=True, null=True)
    other_names = models.CharField(max_length=300, blank=True, null=True)
    sex = (('MALE', 'MALE'), ('FEMALE', 'FEMALE'))
    gender = models.CharField(choices=sex, max_length=10, null=True, blank=True)
    lab_no = models.CharField(max_length=10, null=True, blank=True)
    clinical_diagnosis = models.CharField(max_length=100, null=True, blank=True)
    hospital_clinic= models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField('date of birth', null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True, unique=True)
    created = models.DateTimeField('date added', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.file_no:
            last_instance = self.__class__.objects.order_by('file_no').last()

            if last_instance:
                last_file_no = int(last_instance.file_no)
                new_file_no = f"{last_file_no + 1:06d}"
            else:
                new_file_no = "000001"

            self.file_no = new_file_no

        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('patient_details', args=[self.file_no])

    def full_name(self):
        return f"{self.surname} {self.other_names}"

    def __str__(self):
        if self.surname:
            return f"{self.full_name()}"


class Paypoint(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    patient=models.ForeignKey(Patient,null=True, on_delete=models.CASCADE,related_name="patient_payments")
    unit = models.CharField(max_length=100, null=True, blank=True)
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
    comments=models.CharField(max_length=500,null=True, blank=True)
    nature_of_specimen = models.CharField(max_length=100, null=True, blank=True)
    collected = models.DateField(auto_now=True, null=True,blank=True)

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
        

class ChempathTest(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    reference_range = models.CharField(max_length=200, null=True, blank=True)
    unit = models.CharField(max_length=200, null=True, blank=True)

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
    comments=models.CharField(max_length=500,null=True, blank=True)
    nature_of_specimen = models.CharField(max_length=1-0, null=True, blank=True)
    collected = models.DateField(auto_now=True, null=True,blank=True)
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
    comments=models.CharField(max_length=500, null=True, blank=True)
    nature_of_specimen = models.CharField(max_length=1-0, null=True, blank=True)
    collected = models.DateField(auto_now=True, null=True,blank=True)

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
    comments = models.CharField(max_length=500,null=True, blank=True)
    nature_of_specimen = models.CharField(max_length=100, null=True, blank=True)
    collected = models.DateField(auto_now_add=True, null=True, blank=True)

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
    comments = models.CharField(max_length=500,null=True, blank=True)
    nature_of_specimen = models.CharField(max_length=100, null=True, blank=True)
    collected = models.DateField(auto_now_add=True, null=True, blank=True)
    collected_by = models.ForeignKey(User, null=True, blank=True, related_name='general_results_collected', on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name='general_results_reported', on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
 
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
        parts = []
        if self.patient:
            parts.append(str(self.patient))
        if self.name:
            parts.append(str(self.name))
        if self.result:
            parts.append(str(self.result))
        return " - ".join(parts)

    def __str__(self):
        if self.patient:
            return f"{self.patient} - {self.name} - {self.result}"
        else:
            return f"{self.name} - {self.result}"



class GenericTest(models.Model):
    labs=(('Chemical Pathology','Chemical Pathology'),('Hematology','Hematology'),('Microbiology','Microbiology'),('Serology','Serology'))
    lab=models.CharField(choices=labs, max_length=300,null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True,unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)

    def __str__(self):
        return f"{self.name}-{self.price}"

class UreaAndElectrolyte(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='urea_electrolyte', null=True, blank=True)    
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True, related_name='results')
    urea = models.FloatField(null=True, blank=True, validators=[MinValueValidator(1.7), MaxValueValidator(8.3)])
    sodium = models.FloatField(null=True, blank=True,validators=[MinValueValidator(135), MaxValueValidator(145)])
    potassium = models.FloatField(null=True, blank=True,validators=[MinValueValidator(3.8), MaxValueValidator(5.4)])
    bicarbonate = models.FloatField(null=True, blank=True,validators=[MinValueValidator(24), MaxValueValidator(32)])
    chloride = models.FloatField(null=True, blank=True,validators=[MinValueValidator(98), MaxValueValidator(108)])
    payment=models.ForeignKey(Paypoint,null=True, on_delete=models.CASCADE,related_name='chempath_payment')
    code = SerialNumberField(default="", editable=False, max_length=20, null=False,blank=True)
    cleared=models.BooleanField(default=False,null=True)
    comments=models.CharField(max_length=500,null=True, blank=True)
    nature_of_specimen = models.CharField(max_length=1-0, null=True, blank=True)
    collected = models.DateField(auto_now=True, null=True,blank=True)
    collected_by = models.ForeignKey(User, null=True, blank=True, related_name='chempath_collected_by', on_delete=models.SET_NULL)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True, related_name='chempath_approved_by')
    created = models.DateTimeField(auto_now_add=True,null=True)
    updated = models.DateTimeField(auto_now=True,null=True)

    def save(self, *args, **kwargs):
        if not self.code:
            last_instance = self.__class__.objects.order_by('code').last()

            if last_instance:
                last_code = int(last_instance.code.removeprefix('CHP'))
                new_code = f"CHP{last_code + 1:03d}"
            else:
                new_code = "CHP001"

            self.code = new_code

        super().save(*args, **kwargs)

    def __str__(self):
        return f"U&E Test for {self.patient} - {self.updated}"