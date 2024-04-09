from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils import timezone


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
            return f"{self.full_name}"

        
class Patient(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
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
        if not self.created:
            self.created = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('file_details', args=[self.phone])

    def full_name(self):
        return f"{self.user.get_full_name()} {self.other_name}"

    def __str__(self):
        if self.user:
            return f"{self.full_name}"


class HematologyTest(models.Model):
    HEMATOLOGY_TEST_CHOICES = [
        ('Hb- GENOTYPE-','Hb- GENOTYPE-'),('BLOOD GROUP','BLOOD GROUP'),('RHESUS','RHESUS'),
        ('Hb','Hb'),('PCV','PCV'),('MCHC','MCHC'),
        ('RBC','RBC'),('MCH','MCH'),('MCV','MCV'),
        ('RETIC','RETIC'),('RETIC INDEX','RETIC INDEX'),('PLATELETS','PLATELETS'),
        ('WBC','WBC'),('ESR','ESR'),('ANISCYTOSIS','ANISCYTOSIS'),('MACROXYTOSIS','MACROXYTOSIS'),
        ('MICROCYTOSIS','MICROCYTOSIS'),('POIKILOCYTOSIS','POIKILOCYTOSIS'),('TARGET CELLS','TARGET CELLS'),
        ('SICKLE CELL','SICKLE CELL'),('HYPOCHROMIA','HYPOCHROMIA'),('POLYCHROMASIA','POLYCHROMASIA'),
        ('NUCLEATED RBC','NUCLEATED RBC'),('NUET','NUET'),('EOSIN','EOSIN'),
        ('BASO','BASO'),('TRANS LYMPH','TRANS LYMPH'),('LYMP','LYMP'),('MONO','MONO')
    ]
    name = models.CharField(max_length=100, choices=HEMATOLOGY_TEST_CHOICES)
    reference_range = models.TextField()

class HematologyResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='hematology_results',null=True, blank=True)
    test = models.ForeignKey(HematologyTest, on_delete=models.CASCADE, null=True, blank=True)
    result = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=50, null=True, blank=True)
    comments=models.TextField(null=True, blank=True)
    natured_of_specimen = models.CharField(max_length=1-0, null=True, blank=True)
    date_collected = models.DateField(null=True, blank=True)
    approved_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='hematology_results', null=True, blank=True)
    date_reported = models.DateTimeField(auto_now_add=True)
