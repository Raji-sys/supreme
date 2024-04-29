from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils import timezone
from django.core.exceptions import ValidationError

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
    middle_name = models.CharField(max_length=300, blank=True, null=True)
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
        return f"{self.user.get_full_name()} {self.middle_name}"

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


# TEST = (
#         ('Hb- GENOTYPE-','Hb- GENOTYPE-'),('BLOOD GROUP','BLOOD GROUP'),('RHESUS','RHESUS'),('Hb','Hb'),('PCV','PCV'),('MCHC','MCHC'),
#         ('RBC','RBC'),('MCH','MCH'),('MCV','MCV'),('RETIC','RETIC'),('RETIC INDEX','RETIC INDEX'),('PLATELETS','PLATELETS'),
#         ('WBC','WBC'),('ESR','ESR'),('ANISCYTOSIS','ANISCYTOSIS'),('MACROXYTOSIS','MACROXYTOSIS'),('MICROCYTOSIS','MICROCYTOSIS'),('POIKILOCYTOSIS','POIKILOCYTOSIS'),('TARGET CELLS','TARGET CELLS'),
#         ('SICKLE CELL','SICKLE CELL'),('HYPOCHROMIA','HYPOCHROMIA'),('POLYCHROMASIA','POLYCHROMASIA'),('NUCLEATED RBC','NUCLEATED RBC'),('NUET','NUET'),('EOSIN','EOSIN'),
#         ('BASO','BASO'),('TRANS LYMPH','TRANS LYMPH'),('LYMP','LYMP'),('MONO','MONO')
#     )
class HematologyTest(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    reference_range = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.name}, {self.reference_range}"


class HematologyResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='hematology_result', null=True, blank=True)
    result_code = SerialNumberField(default="", editable=False,max_length=20,null=False,blank=True)
    test = models.ForeignKey(HematologyTest, max_length=100, null=True, blank=True, on_delete=models.CASCADE, related_name="results")
    result = models.CharField(max_length=50, null=True, blank=True)
    unit = models.CharField(max_length=50, null=True, blank=True)
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
            return f"{self.patient.surname} - {self.test} - {self.result}"
        

class HemaParameter(models.Model):
    result = models.ForeignKey(HematologyResult, on_delete=models.CASCADE, related_name='hema_parameters', null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    value = models.CharField(max_length=200, null=True, blank=True)

# CHEMPATH_TEST=[
#     ('UREA 1.7-8.3','UREA 1.7-8.3'),('NA 135-145','NA 135-145'),('K 3.8-5.4','K 3.8-5.4'),
#     ('HCO2 24-32','HCO2 24-32'),('CL 98-108','CL 98-108'),('FASTING','FASTING'),
#     ('RANDOM 3.89-6.11','RANDOM 3.89-6.11'),('2HR PP','2HR PP'),('CSF GLUCOSE 2.78-4.44','CSF CLUCOSE 2.78-4.44'),
#     ('CSF PROTEIN 150-400','CSF PROTEIN 150-400'),('CSF CHLORIDE 120-130','CSF CHLORIDE 120-130'),('CHOLESTEROL 3.89-6.21','CHOLESTEROL 3.89-6.21'),
#     ('TRIGLYCERIDE 0.00-1.92','TRIGLYCERIDE 0.00-1.92'),('HDL-CHOL >1.68(FEMALE) >1.68(MALE)','HDL-CHOL > 1.68(FEMALE) > 1.68(MALE)'),('LDL-CHOL < 3.90','LDL-CHOL < 3.90'),
#     ('ALKALINE PHOSPHATES 9-35(ADULT) 35-100(CHILD)','ALKALINE PHOSPHATES 9-35(ADULT) 35-100(CHILD)'),('SGOT 0-12','SGOT 0-12'),('SGPT 0-12','SGPT 0-12'),
#     ('GAMA G. T 10-40','GAMA G. T 10-40'),('BILLIRUBIN TOTAL= <17','BILLIRUBIN TOTAL= <17'),('BILLIRUBIN DIRECT= <4.3','BILLIRUBIN DIRECT= <4.3'),
#     ('T:PROTEIN 6.5-8.7','T:PROTEIN 6.5-8.7'),('ALBUMIN 3.8-4.4','ALBUMIN 3.8-4.4'),('GLOBULIN 2-3.9','GLOBULIN 2-3.9'),
#     ('ALKALINE PHOSPHATES 9-35(ADULT) 35-100(CHILDREN)','ALKALINE PHOSPHATES 9-35(ADULT) 35-100(CHILDREN)'),('CALCIUM 2.02-2.60','CALCIUM 2.02-2.60'),('INORG. PHOSPHATES 0.81-1.62(ADULT) 1.30-2.26(CHILDREN)','INORG. PHOSPHATES 0.81-1.62(ADULT) 1.30-2.26(CHILDREN)'),
#     ('URIC ACID 202-416(MALE) 142-339(FEMALE)','URIC ACID 202-416(MALE) 142-339(FEMALE)'),('CREATININE 53-97(MALE) 44-80(FEMALE)','CREATININE 53-97(MALE) 44-80(FEMALE)'),('SERUM ANYLASE','SERUM ANYLASE'),
#     ('ACID PHOSPHATES: TOTAL (<11U/L)','ACID PHOSPHATES: PROSTATIC (<11U/L)'),('ACID PHOSPHATES: TOTAL (<11U/L)','ACID PHOSPHATES: PROSTATIC (<11U/L)')
#     ]

class ChempathTestName(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    reference_range = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.name}, {self.reference_range}"
    

class ChemicalPathologyResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='chemical_pathology_results',null=True, blank=True)
    result_code = SerialNumberField(default="", editable=False,max_length=20,null=False,blank=True)
    test = models.ForeignKey(ChempathTestName, max_length=100, null=True, blank=True, on_delete=models.CASCADE, related_name="results")
    result = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=50, null=True, blank=True)
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
            return f"{self.patient.surname} - {self.test} - {self.result}"

class ChempathParameter(models.Model):
    result = models.ForeignKey(ChemicalPathologyResult, on_delete=models.CASCADE, related_name='chempath_parameters', null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    value = models.CharField(max_length=200, null=True, blank=True)


# class MicroTestCategory(models.Model):
#     name = models.CharField(max_length=100,null=True,blank=True)
#     def __str__(self):
#         return self.name
    

class MicrobiologyTest(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    # category=models.ForeignKey(MicroTestCategory,on_delete=models.CASCADE,null=True,blank=True)
    reference_range = models.CharField(max_length=200,null=True,blank=True)
    def __str__(self):
        return self.name


class MicrobiologyResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='microbiology_results',null=True, blank=True)
    result_code = SerialNumberField(default="", editable=False,max_length=20,null=False,blank=True)
    # category=models.ForeignKey(MicroTestCategory,on_delete=models.CASCADE,null=True,blank=True)
    test = models.ForeignKey(MicrobiologyTest, on_delete=models.CASCADE, null=True, blank=True)
    result = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=50, null=True, blank=True)
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

class MicroParameter(models.Model):
    result = models.ForeignKey(MicrobiologyResult, on_delete=models.CASCADE, related_name='micro_parameters', null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    value = models.CharField(max_length=200, null=True, blank=True)


    def __str__(self):
        return f"{self.name}: {self.value}"
    

class SerologyTestName(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    reference_range = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.name}, {self.reference_range}"

class SerologyTestResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='serology_results', null=True, blank=True)
    result_code = models.CharField(max_length=20, unique=True, editable=False, default="")
    test = models.ForeignKey(SerologyTestName, on_delete=models.CASCADE, null=True, blank=True, related_name='results')
    result = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=50, null=True, blank=True)
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
            last_instance = SerologyTestResult.objects.order_by('result_code').last()
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

class SerologyParameter(models.Model):
    result = models.ForeignKey(SerologyTestResult, on_delete=models.CASCADE, related_name='serology_parameters', null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    value = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.name}: {self.value}"



class GeneralTestResult(models.Model):
    name = models.CharField(max_length=100, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='general_results', null=True, blank=True)
    result_code = SerialNumberField(default="", editable=False,max_length=20,null=False,blank=True)
    result = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=50, null=True, blank=True)
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
            return f"{self.patient.surname} - {self.test} - {self.result}"