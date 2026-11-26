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

    
class SerialNumberField(models.CharField):
    description = "A unique serial number field with leading zeros"

    def __init__(self, *args, **kwargs):
        kwargs['unique'] = True
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["unique"]
        return name, path, args, kwargs


def next_serial(model, field, prefix, width):
    """Next code after the highest NUMBER already used, e.g. GEN724 after GEN723.

    Do not use order_by(field).last() for this: codes are text, and as text
    'GEN1000' sorts BEFORE 'GEN999', so after 999 the "last" code would stay
    GEN999 forever, every new record would get GEN1000 again, and the unique
    constraint would reject it. Comparing numbers keeps working past 999/9999.
    """
    numbers = [
        int(code[len(prefix):])
        for code in model.objects.filter(**{f'{field}__startswith': prefix}).values_list(field, flat=True)
        if code[len(prefix):].isdigit()
    ]
    return f"{prefix}{(max(numbers) + 1) if numbers else 1:0{width}d}"


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
    gender = models.CharField(choices=sex, max_length=100, null=True, blank=True)
    lab_no = models.CharField(max_length=100, null=True, blank=True)
    clinical_diagnosis = models.CharField(max_length=1000, null=True, blank=True)
    hospital_clinic= models.CharField('hospital/clinic',max_length=1000, null=True, blank=True)
    age = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=101, null=True, blank=True, unique=True)
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
    unit = models.CharField(max_length=1000, null=True, blank=True)
    service = models.CharField(max_length=1000, null=True, blank=True)
    price = models.DecimalField(max_digits=100, decimal_places=2, null=True,blank=True)
    status=models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateField(auto_now=True)


class GeneralTestResult(models.Model):
    test_1 = models.CharField(max_length=1000, null=True)
    result_1 = models.TextField(null=True)
    reference_range_test_1a = models.CharField(max_length=100,null=True,blank=True)
    reference_range_test_1b = models.TextField(null=True)

    test_2 = models.CharField(max_length=1000, null=True)
    result_2 = models.TextField(null=True)
    reference_range_test_2a = models.CharField(max_length=100,null=True,blank=True)
    reference_range_test_2b = models.TextField(null=True)

    test_3 = models.CharField(max_length=1000, null=True)
    result_3 = models.TextField(null=True)
    reference_range_test_3a = models.CharField(max_length=100,null=True,blank=True)
    reference_range_test_3b = models.TextField(null=True)

    test_4 = models.CharField(max_length=1000, null=True)
    result_4 = models.TextField(null=True)
    reference_range_test_4a = models.CharField(max_length=100,null=True,blank=True)
    reference_range_test_4b = models.TextField(null=True)

    test_5 = models.CharField(max_length=1000, null=True)
    result_5 = models.TextField(null=True)
    reference_range_test_5a = models.CharField(max_length=100,null=True,blank=True)
    reference_range_test_5b = models.TextField(null=True)

    test_6 = models.CharField(max_length=1000, null=True)
    result_6 = models.TextField(null=True)
    reference_range_test_6a = models.CharField(max_length=100,null=True,blank=True)
    reference_range_test_6b = models.TextField(null=True)
    
    test_7 = models.CharField(max_length=1000, null=True)
    result_7 = models.TextField(null=True)
    reference_range_test_7a = models.CharField(max_length=100,null=True,blank=True)
    reference_range_test_7b = models.TextField(null=True)

    test_8 = models.CharField(max_length=1000, null=True)
    result_8 = models.TextField(null=True)
    reference_range_test_8a = models.CharField(max_length=100,null=True,blank=True)
    reference_range_test_8b = models.TextField(null=True)
    
    test_9 = models.CharField(max_length=1000, null=True)
    result_9 = models.TextField(null=True)
    reference_range_test_9a = models.CharField(max_length=100,null=True,blank=True)
    reference_range_test_9b = models.TextField(null=True)
    
    test_10 = models.CharField(max_length=1000, null=True)
    result_10 = models.TextField(null=True)
    reference_range_test_10a = models.CharField(max_length=100,null=True,blank=True)
    reference_range_test_10b = models.TextField(null=True)

    test_11 = models.CharField(max_length=1000, null=True)
    result_11 = models.TextField(null=True)
    reference_range_test_11a = models.CharField(max_length=100,null=True,blank=True)
    reference_range_test_11b = models.TextField(null=True)

    test_12 = models.CharField(max_length=1000, null=True)
    result_12 = models.TextField(null=True)
    reference_range_test_12a = models.CharField(max_length=100,null=True,blank=True)
    reference_range_test_12b = models.TextField(null=True)

    test_13 = models.CharField(max_length=1000, null=True)
    result_13 = models.TextField(null=True)
    reference_range_test_13a = models.CharField(max_length=100,null=True,blank=True)
    reference_range_test_13b = models.TextField(null=True)

    test_14 = models.CharField(max_length=1000, null=True)
    result_14 = models.TextField(null=True)
    reference_range_test_14a = models.CharField(max_length=100,null=True,blank=True)
    reference_range_test_14b = models.TextField(null=True)

    test_15 = models.CharField(max_length=1000, null=True)
    result_15 = models.TextField(null=True)
    reference_range_test_15a = models.CharField(max_length=100,null=True,blank=True)
    reference_range_test_15b = models.TextField(null=True)
    
    payment=models.ForeignKey(Paypoint,null=True, on_delete=models.CASCADE,related_name='general_result_payment')
    price = models.DecimalField(max_digits=100, decimal_places=2, null=True,blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='general_results', null=True, blank=True) 
    result_code = SerialNumberField(default="", editable=False,max_length=20,null=False,blank=True)
    cleared=models.BooleanField(default=False)

    comments = models.CharField(max_length=500,null=True, blank=True)
    nature_of_specimen = models.CharField(max_length=300, null=True, blank=True)
    collected = models.DateField(auto_now_add=True, null=True, blank=True)
    collected_by = models.ForeignKey(User, null=True, blank=True, related_name='general_results_collected', on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name='general_results_reported', on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
 
    def save(self, *args, **kwargs):
        if not self.result_code:
            self.result_code = next_serial(GeneralTestResult, 'result_code', 'GEN', 3)

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
            return f"{self.patient}"

class GenericTest(models.Model):
    LABS = [
        ('Chemical Pathology', 'Chemical Pathology'),
        ('Hematology', 'Hematology'),
        ('Microbiology', 'Microbiology'),
        ('Serology', 'Serology'),
        ('General', 'General')
    ]
    lab = models.CharField(choices=LABS, max_length=300,null=True, blank=True)
    name = models.CharField(max_length=1000, unique=True,null=True, blank=True)
    price = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True)
    def __str__(self):        
        return f"{self.name} - {self.price}"

        
class Testinfo(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='test_info',null=True, blank=True)
    payment = models.ForeignKey(Paypoint, on_delete=models.CASCADE, related_name='test_payments',null=True,blank=True)
    code = models.CharField(max_length=20, unique=True, editable=False)
    cleared = models.BooleanField(default=False)
    comments = models.CharField(max_length=500, null=True, blank=True)
    nature_of_specimen = models.CharField(max_length=300, null=True, blank=True)
    collected = models.DateField(auto_now=True)
    collected_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='collected_tests')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_tests')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = next_serial(Testinfo, 'code', 'SUP', 4)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} for {self.patient} - {self.updated}"
    def __str__(self):
        return f"{self.code} - {self.patient}"


# HEMATOLOGY TEST 
class FBC(models.Model):
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='fbc_test', null=True, blank=True)
    hb = models.CharField(max_length=10, null=True, blank=True)  # Hemoglobin
    pcv = models.CharField(max_length=10, null=True, blank=True)  # Packed Cell Volume
    mchc = models.CharField(max_length=10, null=True, blank=True)  # Mean Corpuscular Hemoglobin Concentration
    rbc = models.CharField(max_length=10, null=True, blank=True)  # Red Blood Cells
    mch = models.CharField(max_length=10, null=True, blank=True)  # Mean Corpuscular Hemoglobin
    mcv = models.CharField(max_length=10, null=True, blank=True)  # Mean Corpuscular Volume

    retic = models.CharField(max_length=10, null=True, blank=True)  # Reticulocyte Count
    retic_index = models.CharField(max_length=10, null=True, blank=True)  # Reticulocyte Index
    platelets = models.CharField(max_length=6,  null=True, blank=True)  # Platelets
    wbc = models.CharField(max_length=6, null=True, blank=True)  # White Blood Cells
    esr = models.CharField(max_length=6, null=True, blank=True)  # Erythrocyte Sedimentation Rate

    Opt= [
    ('+', '+'),
    ('++', '++'),
    ('+++', '+++'),
    ('None', 'None')
]

    sickle_cells = models.CharField(choices=Opt, max_length=100, null=True, blank=True)  # Sickle Cells
    hypochromia = models.CharField(choices=Opt, max_length=100, null=True, blank=True)  # Hypochromia
    polychromasia = models.CharField(choices=Opt, max_length=100, null=True, blank=True)  # Polychromasia
    nucleated_rbc = models.CharField(choices=Opt, max_length=100, null=True, blank=True)  # Nucleated RBC
    anisocytosis = models.CharField(choices=Opt, max_length=100, null=True, blank=True)  # Anisocytosis
    macrocytosis = models.CharField(choices=Opt, max_length=100, null=True, blank=True)  # Macrocytosis
    microcytosis = models.CharField(choices=Opt, max_length=100, null=True, blank=True)  # Microcytosis
    poikilocytosis = models.CharField(choices=Opt, max_length=100, null=True, blank=True)  # Poikilocytosis
    target_cells = models.CharField(choices=Opt, max_length=100, null=True, blank=True)  # Target Cells

    neutrophils = models.CharField(max_length=5,null=True, blank=True)  # Neutrophils %
    eosinophils = models.CharField(max_length=5,null=True, blank=True)  # Eosinophils %
    basophils = models.CharField(max_length=5, null=True, blank=True)  # Basophils %
    trans_lymph = models.CharField(max_length=10, null=True, blank=True)  # Transitional Lymphocytes %
    lymphocytes = models.CharField(max_length=10, null=True, blank=True)  # Lymphocytes %
    mid = models.CharField(max_length=10, null=True, blank=True)  # mid  %
    monocytes = models.CharField(max_length=10, null=True, blank=True)  # Monocytes %
    rbc_comments=models.CharField("RBC's",max_length=3000,null=True, blank=True)
    wbc_comments=models.CharField("WBC's",max_length=3000,null=True, blank=True)
    platelets_comments=models.CharField("Platelet's",max_length=3000,null=True, blank=True)
    comment = models.CharField(max_length=3000,null=True, blank=True)


# FBC 2: the 3-part differential analyser printout (WBC/Lymph/Mid/Gran ...).
# One row per parameter, in the order the analyser prints them:
#   (field name, label, unit, reference low, reference high)
# These drive the entry form, the patient folder and the PDF. To change a
# reference range, change it HERE - nowhere else needs touching.
FBC2_PARAMETERS = [
    ('wbc',         'WBC',     'x10^9/L',  '4.0',   '11.0'),
    ('lymph_count', 'Lymph#',  'x10^9/L',  '0.8',   '4.0'),
    ('mid_count',   'Mid#',    'x10^9/L',  '0.1',   '1.2'),
    ('gran_count',  'Gran#',   'x10^9/L',  '2.0',   '7.0'),
    ('lymph_pct',   'Lymph%',  '%',        '25.0',  '45.0'),
    ('mid_pct',     'Mid%',    '%',        '3.0',   '14.0'),
    ('gran_pct',    'Gran%',   '%',        '45.0',  '75.0'),
    ('hgb',         'HGB',     'g/dL',     '11.0',  '16.0'),
    ('rbc',         'RBC',     'x10^12/L', '3.50',  '5.50'),
    ('hct',         'HCT',     '%',        '33.0',  '47.0'),
    ('mcv',         'MCV',     'fL',       '80.0',  '100.0'),
    ('mch',         'MCH',     'pg',       '27.0',  '34.0'),
    ('mchc',        'MCHC',    'g/dL',     '32.0',  '36.0'),
    ('rdw_cv',      'RDW-CV',  '%',        '11.0',  '16.0'),
    ('rdw_sd',      'RDW-SD',  'fL',       '35.0',  '56.0'),
    ('plt',         'PLT',     'x10^9/L',  '150',   '400'),
    ('mpv',         'MPV',     'fL',       '6.5',   '12.0'),
    ('pdw',         'PDW',     '',         '9.0',   '17.0'),
    ('pct',         'PCT',     '%',        '0.108', '0.282'),
]


_SUPERSCRIPT = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')


def fbc2_unit_text(unit):
    """'x10^9/L' -> 'x10⁹/L' for the browser."""
    if '^' not in unit:
        return unit
    head, tail = unit.split('^', 1)
    digits = ''.join(ch for ch in tail if ch.isdigit())
    return head + digits.translate(_SUPERSCRIPT) + tail[len(digits):]


def _unit_html(unit):
    """'x10^9/L' -> 'x10<sup>9</sup>/L' for the PDF (its font has no superscript glyphs)."""
    if '^' not in unit:
        return unit
    head, tail = unit.split('^', 1)
    digits = ''.join(ch for ch in tail if ch.isdigit())
    return f"{head}<sup>{digits}</sup>{tail[len(digits):]}"


def _fbc2_result_field():
    # Labels and reference ranges are applied by FBC2Form from FBC2_PARAMETERS,
    # so changing a range never needs a migration.
    return models.CharField(max_length=20, null=True, blank=True)


class FBC2(models.Model):
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='fbc2_test', null=True, blank=True)

    wbc = _fbc2_result_field()
    lymph_count = _fbc2_result_field()
    mid_count = _fbc2_result_field()
    gran_count = _fbc2_result_field()
    lymph_pct = _fbc2_result_field()
    mid_pct = _fbc2_result_field()
    gran_pct = _fbc2_result_field()
    hgb = _fbc2_result_field()
    rbc = _fbc2_result_field()
    hct = _fbc2_result_field()
    mcv = _fbc2_result_field()
    mch = _fbc2_result_field()
    mchc = _fbc2_result_field()
    rdw_cv = _fbc2_result_field()
    rdw_sd = _fbc2_result_field()
    plt = _fbc2_result_field()
    mpv = _fbc2_result_field()
    pdw = _fbc2_result_field()
    pct = _fbc2_result_field()
    comment = models.CharField(max_length=3000, null=True, blank=True)

    class Meta:
        verbose_name = 'FBC 2'
        verbose_name_plural = 'FBC 2'

    def rows(self, include_empty=False):
        """Parameters ready for display: label, value, unit, range text and
        flag ('H', 'L' or ''). By default only parameters that have a result;
        include_empty=True lists all of them (blank result until entered)."""
        out = []
        for field, label, unit, low, high in FBC2_PARAMETERS:
            value = getattr(self, field)
            if value in (None, '') and not include_empty:
                continue
            value = value or ''
            flag = ''
            try:
                number = float(str(value).strip())
            except ValueError:
                number = None  # blank, or free text such as "<0.1": never flagged
            if number is not None:
                if number < float(low):
                    flag = 'L'
                elif number > float(high):
                    flag = 'H'
            out.append({'label': label, 'value': value,
                        'unit': fbc2_unit_text(unit), 'unit_html': _unit_html(unit),
                        'range': f"{low} - {high}", 'flag': flag})
        return out

    def all_rows(self):
        """Every parameter, blank where no result yet - for the printed report."""
        return self.rows(include_empty=True)

    def __str__(self):
        return f"FBC 2 - {self.test_info}"


class BloodGroup(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='bg_test', null=True, blank=True)
    result = models.CharField(null=True, max_length=3, choices=BLOOD_GROUP_CHOICES)


class Genotype(models.Model):
    GENOTYPE_CHOICES = [
        ('AA', 'AA'),
        ('AS', 'AS'),
        ('SS', 'SS'),
        ('AC', 'AC'),
        ('SC', 'SC'),
    ]

    test=models.ForeignKey(GenericTest,on_delete=models.CASCADE,null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='gt_test',null=True, blank=True)
    result = models.CharField(null=True,choices=GENOTYPE_CHOICES,max_length=2)


# class RhesusFactor(models.Model):
#     RHESUS_CHOICES = [
#         ('Positive', 'Positive'),
#         ('Negative', 'Negative'),
#     ]    
#     test=models.ForeignKey(GenericTest,on_delete=models.CASCADE,null=True, blank=True)
#     test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='rh_test',null=True, blank=True)
#     rhesus_d = models.CharField('rhesus (D)',max_length=8, choices=RHESUS_CHOICES, null=True)


# CHEMICAL PATHOLOGY TESTS
class UreaAndElectrolyte(models.Model):
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='ue_test',null=True, blank=True)
    urea = models.CharField(max_length=100,null=True, blank=True)
    sodium = models.CharField(max_length=100,null=True, blank=True)
    potassium = models.CharField(max_length=100,null=True, blank=True)
    bicarbonate = models.CharField(max_length=100,null=True, blank=True)
    chloride = models.CharField(max_length=100,null=True, blank=True)
    creatinine = models.CharField(max_length=100,null=True, blank=True)
    comment = models.CharField(max_length=3000,null=True, blank=True)


class LiverFunction(models.Model):
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='lf_test',null=True, blank=True)
    alkaline_phosphatase = models.CharField(max_length=100,null=True, blank=True)
    sgot = models.CharField(max_length=100,null=True, blank=True)
    sgpt = models.CharField(max_length=100,null=True, blank=True)
    gamma_gt = models.CharField(max_length=100,null=True, blank=True)
    total_bilirubin = models.CharField(max_length=100,null=True, blank=True)
    direct_bilirubin = models.CharField(max_length=100,null=True, blank=True)
    t_protein = models.CharField(max_length=10, help_text="Total Protein (g/dL)", null=True)
    albumin = models.CharField(max_length=10, help_text="Albumin (g/dL)", null=True)
    globulin = models.CharField(max_length=10, help_text="Globulin (g/dL)", null=True)
    comment = models.CharField(max_length=3000,null=True, blank=True)


class LipidProfile(models.Model):
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='lp_test',null=True, blank=True)
    cholesterol = models.CharField(max_length=100,null=True, blank=True)
    triglyceride = models.CharField(max_length=100,null=True, blank=True)
    hdl_cholesterol = models.CharField(max_length=100,null=True, blank=True)
    ldl_cholesterol = models.CharField(max_length=100,null=True, blank=True)
    comment = models.CharField(max_length=3000,null=True, blank=True)


class BloodGlucose(models.Model):
    GLUCOSE_TEST_TYPES = [
        ('FASTING', 'Fasting'),
        ('RANDOM', 'Random'),
        ('2HR_PP', '2 Hour Post Prandial'),
    ]
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='bgl_test',null=True, blank=True)
    test_type = models.CharField(max_length=100, choices=GLUCOSE_TEST_TYPES,null=True)
    result = models.CharField(max_length=100,null=True)
    comment = models.CharField(max_length=3000,null=True, blank=True)


class SerumProteins(models.Model):
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='sp_test',null=True, blank=True)
    t_protein = models.CharField(max_length=10, help_text="Total Protein (g/dL)", null=True)
    albumin = models.CharField(max_length=10, help_text="Albumin (g/dL)", null=True)
    globulin = models.CharField(max_length=10, help_text="Globulin (g/dL)", null=True)
    comment = models.CharField(max_length=3000,null=True, blank=True)


class CerebroSpinalFluid(models.Model):
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='csf_test',null=True, blank=True)
    csf_glucose = models.CharField(max_length=10, help_text="CSF Glucose (mmol/L)", null=True)
    csf_protein = models.CharField(max_length=10, help_text="CSF Protein (mg/dL)", null=True)
    csf_chloride = models.CharField(max_length=10, help_text="CSF Chloride (mmol/L)", null=True)
    comment = models.CharField(max_length=3000,null=True, blank=True)


class BoneChemistry(models.Model):
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='bc_test',null=True, blank=True)
    alkaline_phosphatase = models.CharField(max_length=10, help_text="Alkaline Phosphatase (U/L)", null=True)
    calcium = models.CharField(max_length=10, help_text="Calcium (mmol/L)", null=True)
    inorganic_phosphate = models.CharField(max_length=10, help_text="Inorganic Phosphate (mmol/L)", null=True)
    comment = models.CharField(max_length=3000,null=True, blank=True)


class MiscellaneousChempathTests(models.Model):
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='misc_test',null=True, blank=True)
    uric_acid = models.CharField(max_length=10, help_text="Uric Acid (umol/L)", null=True,blank=True)
    serum_amylase = models.CharField(max_length=10, help_text="Serum Amylase (U/L)", null=True,blank=True)
    acid_phosphatase_total = models.CharField(max_length=10, help_text="Acid Phosphatase Total (U/L)", null=True,blank=True)
    acid_phosphatase_prostatic = models.CharField(max_length=10, help_text="Acid Phosphatase Prostatic (U/L)", null=True,blank=True)
    psa=models.CharField(max_length=10,null=True, blank=True, help_text="Prostate Specific Antigen (PSA)")
    comment = models.CharField(max_length=3000,null=True, blank=True)

# MICROBIOLOGY TEST 
SEVERITY_CHOICES = [
    ('s+', 's+'),
    ('s++', 's++'),
    ('s+++', 's+++'),
    ('R', 'R')
]
CULTURE_CHOICES = [
    ('Scanty Growth', 'Scanty Growth'),
    ('Moderate Growth', 'Moderate Growth'),
    ('Heavy Growth', 'Heavy Growth'),
]
SWAB_PUS = [
    ('swab', 'swab'),
    ('pus', 'pus'),
    ('aspirate', 'aspirate'),
]
class Swab_Pus_Aspirate_MCS(models.Model):
    options=models.CharField(max_length=20,choices=SWAB_PUS,blank=True,null=True)
    test = models.ForeignKey('GenericTest', on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='swab_pus_aspirate_test', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated = models.DateTimeField(auto_now=True,null=True,blank=True)
    comment = models.CharField(max_length=3000,null=True, blank=True)

    # Culture yield fields with Yes/No options
    no_growth = models.BooleanField(default=False)
    e_coli = models.BooleanField(default=False)
    coliform = models.BooleanField(default=False)
    proteus = models.BooleanField(default=False)
    staph_aureus = models.BooleanField(default=False)
    pseudomonas = models.BooleanField(default=False)
    streptococcus = models.BooleanField(default=False)
    klebsiella = models.BooleanField(default=False)
    salmonella = models.BooleanField(default=False)
    str_feacalis = models.BooleanField(default=False)
    shigella = models.BooleanField(default=False)
    c_diphtheriae = models.BooleanField(default=False)
    neisseria = models.BooleanField(default=False)
    candida = models.BooleanField(default=False)
    haemophilus = models.BooleanField(default=False)
    str_pneumonia = models.BooleanField(default=False)
    str_pyogenes = models.BooleanField(default=False)
    staph_albus = models.BooleanField(default=False)
    usual_flora = models.BooleanField(default=False)
    stage_of_bacteria_growth = models.CharField(max_length=20, choices=CULTURE_CHOICES, blank=True, null=True)
    
    # Antibiotics Sensitivity with Severity (1-4 and Resistant)
    cloxacillin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ciprofloxacin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    lincomycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    flucloxacillin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    tetracycline = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ampicillin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    erythromycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    roxithromycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    augmentin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    cotrimoxazole = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    cephalexin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    dalacin_c = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    gentamycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    streptomycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ceftriaxone = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    chloramphenicol = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    nitrofurantoin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    nalidixic_acid = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    cefuroxime = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ceftazidime = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ofloxacin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    pefloxacin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)


class UrineMicroscopy(models.Model):
    test = models.ForeignKey('GenericTest', on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='urine_test', null=True, blank=True)
    pus_cells = models.CharField(max_length=50, blank=True, null=True)
    rbc = models.CharField(max_length=50, blank=True, null=True)
    epithelial_cells = models.CharField(max_length=50, blank=True, null=True)
    casts = models.CharField(max_length=50, blank=True, null=True)
    crystals = models.CharField(max_length=50, blank=True, null=True)
    ova = models.CharField(max_length=50, blank=True, null=True)
    comment = models.CharField(max_length=3000,null=True, blank=True)

    # Culture yield fields with Yes/No options
    no_growth = models.BooleanField(default=False)
    e_coli = models.BooleanField(default=False)
    coliform = models.BooleanField(default=False)
    proteus = models.BooleanField(default=False)
    staph_aureus = models.BooleanField(default=False)
    pseudomonas = models.BooleanField(default=False)
    streptococcus = models.BooleanField(default=False)
    klebsiella = models.BooleanField(default=False)
    salmonella = models.BooleanField(default=False)
    str_feacalis = models.BooleanField(default=False)
    shigella = models.BooleanField(default=False)
    c_diphtheriae = models.BooleanField(default=False)
    neisseria = models.BooleanField(default=False)
    candida = models.BooleanField(default=False)
    haemophilus = models.BooleanField(default=False)
    str_pneumonia = models.BooleanField(default=False)
    str_pyogenes = models.BooleanField(default=False)
    staph_albus = models.BooleanField(default=False)
    usual_flora = models.BooleanField(default=False)
    stage_of_bacteria_growth = models.CharField(max_length=20, choices=CULTURE_CHOICES, blank=True, null=True)
    
    # Antibiotics Sensitivity with Severity (1-4 and Resistant)
    cloxacillin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ciprofloxacin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    lincomycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    flucloxacillin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    tetracycline = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ampicillin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    erythromycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    roxithromycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    augmentin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    cotrimoxazole = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    cephalexin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    dalacin_c = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    gentamycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    streptomycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ceftriaxone = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    chloramphenicol = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    nitrofurantoin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    nalidixic_acid = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    cefuroxime = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ceftazidime = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ofloxacin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    pefloxacin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)


class HVS(models.Model):
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='hvs_test',null=True, blank=True)
    pus_cells = models.CharField(max_length=50, blank=True, null=True)
    rbc = models.CharField(max_length=50, blank=True, null=True)
    epithelial_cells = models.CharField(max_length=50, blank=True, null=True)
    t_vaginalis = models.CharField(max_length=50, blank=True, null=True)
    yeast_cells = models.CharField(max_length=50, blank=True, null=True)
    comment = models.CharField(max_length=3000,null=True, blank=True)

    # Culture yield fields with Yes/No options
    no_growth = models.BooleanField(default=False)
    e_coli = models.BooleanField(default=False)
    coliform = models.BooleanField(default=False)
    proteus = models.BooleanField(default=False)
    staph_aureus = models.BooleanField(default=False)
    pseudomonas = models.BooleanField(default=False)
    streptococcus = models.BooleanField(default=False)
    klebsiella = models.BooleanField(default=False)
    salmonella = models.BooleanField(default=False)
    str_feacalis = models.BooleanField(default=False)
    shigella = models.BooleanField(default=False)
    c_diphtheriae = models.BooleanField(default=False)
    neisseria = models.BooleanField(default=False)
    candida = models.BooleanField(default=False)
    haemophilus = models.BooleanField(default=False)
    str_pneumonia = models.BooleanField(default=False)
    str_pyogenes = models.BooleanField(default=False)
    staph_albus = models.BooleanField(default=False)
    usual_flora = models.BooleanField(default=False)
    stage_of_bacteria_growth = models.CharField(max_length=20, choices=CULTURE_CHOICES, blank=True, null=True)
    
    # Antibiotics Sensitivity with Severity (1-4 and Resistant)
    cloxacillin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ciprofloxacin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    lincomycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    flucloxacillin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    tetracycline = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ampicillin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    erythromycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    roxithromycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    augmentin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    cotrimoxazole = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    cephalexin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    dalacin_c = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    gentamycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    streptomycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ceftriaxone = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    chloramphenicol = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    nitrofurantoin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    nalidixic_acid = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    cefuroxime = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ceftazidime = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ofloxacin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    pefloxacin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)


class Stool(models.Model):
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='stool_test',null=True, blank=True)
    consistency = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    mucus = models.CharField(max_length=50, blank=True, null=True)
    blood = models.CharField(max_length=50, blank=True, null=True)
    ova = models.CharField(max_length=50, blank=True, null=True)
    cyst = models.CharField(max_length=50, blank=True, null=True)
    others = models.CharField(max_length=50, blank=True, null=True)
    comment = models.CharField(max_length=3000,null=True, blank=True)

    # Culture yield fields with Yes/No options
    no_growth = models.BooleanField(default=False)
    e_coli = models.BooleanField(default=False)
    coliform = models.BooleanField(default=False)
    proteus = models.BooleanField(default=False)
    staph_aureus = models.BooleanField(default=False)
    pseudomonas = models.BooleanField(default=False)
    streptococcus = models.BooleanField(default=False)
    klebsiella = models.BooleanField(default=False)
    salmonella = models.BooleanField(default=False)
    str_feacalis = models.BooleanField(default=False)
    shigella = models.BooleanField(default=False)
    c_diphtheriae = models.BooleanField(default=False)
    neisseria = models.BooleanField(default=False)
    candida = models.BooleanField(default=False)
    haemophilus = models.BooleanField(default=False)
    str_pneumonia = models.BooleanField(default=False)
    str_pyogenes = models.BooleanField(default=False)
    staph_albus = models.BooleanField(default=False)
    usual_flora = models.BooleanField(default=False)
    stage_of_bacteria_growth = models.CharField(max_length=20, choices=CULTURE_CHOICES, blank=True, null=True)

    # Antibiotics Sensitivity with Severity (1-4 and Resistant)
    cloxacillin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ciprofloxacin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    lincomycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    flucloxacillin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    tetracycline = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ampicillin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    erythromycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    roxithromycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    augmentin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    cotrimoxazole = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    cephalexin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    dalacin_c = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    gentamycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    streptomycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ceftriaxone = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    chloramphenicol = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    nitrofurantoin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    nalidixic_acid = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    cefuroxime = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ceftazidime = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ofloxacin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    pefloxacin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)



class BloodCulture(models.Model):
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='blood_culture_test',null=True, blank=True)
    result=models.CharField(max_length=300,null=True,blank=True)
    comment = models.CharField(max_length=3000,null=True, blank=True)

    # Culture yield fields with Yes/No options
    no_growth = models.BooleanField(default=False)
    e_coli = models.BooleanField(default=False)
    coliform = models.BooleanField(default=False)
    proteus = models.BooleanField(default=False)
    staph_aureus = models.BooleanField(default=False)
    pseudomonas = models.BooleanField(default=False)
    streptococcus = models.BooleanField(default=False)
    klebsiella = models.BooleanField(default=False)
    salmonella = models.BooleanField(default=False)
    str_feacalis = models.BooleanField(default=False)
    shigella = models.BooleanField(default=False)
    c_diphtheriae = models.BooleanField(default=False)
    neisseria = models.BooleanField(default=False)
    candida = models.BooleanField(default=False)
    haemophilus = models.BooleanField(default=False)
    str_pneumonia = models.BooleanField(default=False)
    str_pyogenes = models.BooleanField(default=False)
    staph_albus = models.BooleanField(default=False)
    usual_flora = models.BooleanField(default=False)
    stage_of_bacteria_growth = models.CharField(max_length=20, choices=CULTURE_CHOICES, blank=True, null=True) 
    
    # Antibiotics Sensitivity with Severity (1-4 and Resistant)
    cloxacillin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ciprofloxacin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    lincomycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    flucloxacillin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    tetracycline = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ampicillin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    erythromycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    roxithromycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    augmentin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    cotrimoxazole = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    cephalexin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    dalacin_c = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    gentamycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    streptomycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ceftriaxone = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    chloramphenicol = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    nitrofurantoin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    nalidixic_acid = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    cefuroxime = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ceftazidime = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ofloxacin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    pefloxacin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)



class OccultBlood(models.Model):
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='occult_blood_test',null=True, blank=True)
    result = models.CharField(max_length=30, choices=[('Positive', 'Positive'), ('Negative', 'Negative')])
    comment = models.CharField(max_length=3000,null=True, blank=True)

class SputumMCS(models.Model):
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='sputum_mcs_test',null=True, blank=True)
    comment = models.CharField(max_length=3000,null=True, blank=True)

    # Culture yield fields with Yes/No options
    no_growth = models.BooleanField(default=False)
    e_coli = models.BooleanField(default=False)
    coliform = models.BooleanField(default=False)
    proteus = models.BooleanField(default=False)
    staph_aureus = models.BooleanField(default=False)
    pseudomonas = models.BooleanField(default=False)
    streptococcus = models.BooleanField(default=False)
    klebsiella = models.BooleanField(default=False)
    salmonella = models.BooleanField(default=False)
    str_feacalis = models.BooleanField(default=False)
    shigella = models.BooleanField(default=False)
    c_diphtheriae = models.BooleanField(default=False)
    neisseria = models.BooleanField(default=False)
    candida = models.BooleanField(default=False)
    haemophilus = models.BooleanField(default=False)
    str_pneumonia = models.BooleanField(default=False)
    str_pyogenes = models.BooleanField(default=False)
    staph_albus = models.BooleanField(default=False)
    usual_flora = models.BooleanField(default=False)
    stage_of_bacteria_growth = models.CharField(max_length=20, choices=CULTURE_CHOICES, blank=True, null=True)
    
    # Antibiotics Sensitivity with Severity (1-4 and Resistant)
    cloxacillin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ciprofloxacin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    lincomycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    flucloxacillin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    tetracycline = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ampicillin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    erythromycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    roxithromycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    augmentin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    cotrimoxazole = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    cephalexin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    dalacin_c = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    gentamycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    streptomycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ceftriaxone = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    chloramphenicol = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    nitrofurantoin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    nalidixic_acid = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    cefuroxime = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ceftazidime = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ofloxacin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    pefloxacin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)


class GramStain(models.Model):
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='gram_stain_test',null=True, blank=True)
    # Sample Types
    urine = models.BooleanField(default=False)
    hvs = models.BooleanField("High Vaginal Swab", default=False)
    swab = models.BooleanField(default=False)
    pus = models.BooleanField(default=False)
    aspirate = models.BooleanField(default=False)
    sputum = models.BooleanField(default=False)

    # Gram Stain Findings
    gram_positive_cocci = models.BooleanField(default=False)
    gram_negative_cocci = models.BooleanField(default=False)
    gram_positive_rods = models.BooleanField(default=False)
    gram_negative_rods = models.BooleanField(default=False)
    gram_positive_clusters = models.BooleanField(default=False)
    gram_negative_clusters = models.BooleanField(default=False)
    gram_positive_chains = models.BooleanField(default=False)
    gram_negative_chains = models.BooleanField(default=False)
    other_findings = models.CharField(max_length=2000,blank=True, null=True)

    comment = models.CharField(max_length=3000,null=True, blank=True)


class ZNStain(models.Model):
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='zn_stain_test',null=True, blank=True)
    first_sample = models.CharField(max_length=50, blank=True, null=True,choices=[('Positive', 'Positive'), ('Negative', 'Negative')])
    second_sample = models.CharField(max_length=50, blank=True, null=True,choices=[('Positive', 'Positive'), ('Negative', 'Negative')])
    third_sample = models.CharField(max_length=50, blank=True, null=True,choices=[('Positive', 'Positive'), ('Negative', 'Negative')])
    comment = models.CharField(max_length=3000,null=True, blank=True)


class SemenAnalysis(models.Model):
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='semen_analysis_test',null=True, blank=True)
    comment = models.CharField(max_length=3000,null=True, blank=True)
    time_produced = models.CharField(max_length=300, blank=True, null=True)
    time_examined = models.CharField(max_length=300, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    volume = models.CharField(max_length=10, help_text="Volume (ml)", blank=True, null=True)
    viscosity = models.CharField(max_length=50, blank=True, null=True)
    consistency = models.CharField(max_length=50, blank=True, null=True)
    motility_active = models.CharField(max_length=100, help_text="Active Motility (%)", blank=True, null=True)
    motility_moderate = models.CharField(max_length=100, help_text="Moderate Motility (%)", blank=True, null=True)
    motility_sluggish = models.CharField(max_length=100, help_text="Sluggish Motility (%)", blank=True, null=True)
    morphology_normal = models.CharField(max_length=100, help_text="Normal Morphology (%)", blank=True, null=True)
    morphology_abnormal = models.CharField(max_length=100, help_text="Abnormal Morphology (%)", blank=True, null=True)
    total_sperm_count = models.CharField(max_length=100, help_text="Total Sperm Count (x10^6/ml)", blank=True, null=True)
    
    # semen microscopy
    pus_cell=models.CharField(max_length=100,null=True, blank=True)
    rbc=models.CharField("RBC's",max_length=100,null=True, blank=True)
    epithelial_cells=models.CharField(max_length=100,null=True, blank=True)
    others=models.TextField(null=True)

    # Culture yield fields with Yes/No options
    no_growth = models.BooleanField(default=False)
    e_coli = models.BooleanField(default=False)
    coliform = models.BooleanField(default=False)
    proteus = models.BooleanField(default=False)
    staph_aureus = models.BooleanField(default=False)
    pseudomonas = models.BooleanField(default=False)
    streptococcus = models.BooleanField(default=False)
    klebsiella = models.BooleanField(default=False)
    salmonella = models.BooleanField(default=False)
    str_feacalis = models.BooleanField(default=False)
    shigella = models.BooleanField(default=False)
    c_diphtheriae = models.BooleanField(default=False)
    neisseria = models.BooleanField(default=False)
    candida = models.BooleanField(default=False)
    haemophilus = models.BooleanField(default=False)
    str_pneumonia = models.BooleanField(default=False)
    str_pyogenes = models.BooleanField(default=False)
    staph_albus = models.BooleanField(default=False)
    usual_flora = models.BooleanField(default=False)
    stage_of_bacteria_growth = models.CharField(max_length=20, choices=CULTURE_CHOICES, blank=True, null=True)
    
    # Antibiotics Sensitivity with Severity (1-4 and Resistant)
    cloxacillin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ciprofloxacin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    lincomycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    flucloxacillin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    tetracycline = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ampicillin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    erythromycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    roxithromycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    augmentin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    cotrimoxazole = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    cephalexin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    dalacin_c = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    gentamycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    streptomycin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ceftriaxone = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    chloramphenicol = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    nitrofurantoin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    nalidixic_acid = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    cefuroxime = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ceftazidime = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    ofloxacin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    pefloxacin = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)


class Urinalysis(models.Model):
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='urinalysis_test',null=True, blank=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    appearance = models.CharField(max_length=50, blank=True, null=True)
    specific_gravity = models.CharField(max_length=5, blank=True, null=True)
    ph = models.CharField(max_length=3, blank=True, null=True)
    protein = models.CharField(max_length=50, blank=True, null=True)
    glucose = models.CharField(max_length=50, blank=True, null=True)
    ketones = models.CharField(max_length=50, blank=True, null=True)
    bilirubin = models.CharField(max_length=50, blank=True, null=True)
    urobilinogen = models.CharField(max_length=50, blank=True, null=True)
    nitrites = models.CharField(max_length=50, blank=True, null=True)
    leukocyte = models.CharField(max_length=50, blank=True, null=True)
    blood = models.CharField(max_length=50, blank=True, null=True)
    comment = models.CharField(max_length=3000,null=True, blank=True)

class Pregnancy(models.Model):
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='pregnancy_test',null=True, blank=True)
    result = models.CharField(max_length=100, choices=[('Positive', 'Positive'), ('Negative ', 'Negative')],null=True)
    # method = models.CharField(max_length=50, choices=[('Urine', 'Urine Test'), ('Blood', 'Blood Test')],null=True)
    # comment = models.CharField(max_length=3000,null=True, blank=True)


# SEROLOGY TEST 
class Widal(models.Model):
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='widal_test',null=True, blank=True)
    o_antigen_s_typhi_d = models.CharField(max_length=100, blank=True, null=True)
    o_antigen_s_paratyphi_a = models.CharField(max_length=100, blank=True, null=True)
    o_antigen_s_paratyphi_b = models.CharField(max_length=100, blank=True, null=True)
    o_antigen_s_paratyphi_c = models.CharField(max_length=100, blank=True, null=True)    
    h_antigen_s_typhi_d = models.CharField(max_length=100, blank=True, null=True)
    h_antigen_s_paratyphi_a = models.CharField(max_length=100, blank=True, null=True)
    h_antigen_s_paratyphi_b = models.CharField(max_length=100, blank=True, null=True)
    h_antigen_s_paratyphi_c = models.CharField(max_length=100, blank=True, null=True)
    diagnostic_titre = models.CharField(max_length=20, blank=True, null=True,default='> 1/80')
    mp_options = (('seen +', 'seen +'),('seen ++', 'seen ++'),('seen +++', 'seen +++'), ('not seen', 'not seen'))
    malaria_parasite=models.CharField(choices=mp_options, null=True, blank=True, max_length=100)
    comment = models.CharField(max_length=3000,null=True, blank=True)

class RheumatoidFactor(models.Model):
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='rheumatoid_factor_test',null=True, blank=True)
    result = models.CharField(max_length=100, blank=True, null=True)
    comment = models.CharField(max_length=3000,null=True, blank=True)

class HPB(models.Model):
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='hpb_test',null=True, blank=True)
    result = models.CharField(max_length=100, blank=True, null=True)
    comment = models.CharField(max_length=3000,null=True, blank=True)

class HCV(models.Model):
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='hcv_test',null=True, blank=True)
    result = models.CharField(max_length=100, blank=True, null=True)
    comment = models.CharField(max_length=3000,null=True, blank=True)

class VDRL(models.Model):
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='vdrl_test',null=True, blank=True)
    result = models.CharField(max_length=100, blank=True, null=True)
    comment = models.CharField(max_length=3000,null=True, blank=True)

class Mantoux(models.Model):
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='mantoux_test',null=True, blank=True)
    result = models.CharField(max_length=100, blank=True, null=True)
    comment = models.CharField(max_length=3000,null=True, blank=True)

class AsoTitre(models.Model):
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='aso_titre_test',null=True, blank=True)
    result = models.CharField(max_length=100, blank=True, null=True)
    comment = models.CharField(max_length=3000,null=True, blank=True)

class CRP(models.Model):
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='crp_test',null=True, blank=True)
    result = models.CharField(max_length=100, blank=True, null=True)
    comment = models.CharField(max_length=3000,null=True, blank=True)

class HIVScreening(models.Model):
    test = models.ForeignKey(GenericTest, on_delete=models.CASCADE, null=True, blank=True)
    test_info = models.OneToOneField(Testinfo, on_delete=models.CASCADE, related_name='hiv_test',null=True, blank=True)
    result = models.CharField(max_length=100, blank=True, null=True)
    comment = models.CharField(max_length=3000,null=True, blank=True)

class Ultrasound(models.Model):
    result = models.TextField(null=True, blank=True)
    payment = models.ForeignKey(Paypoint, null=True, on_delete=models.CASCADE, related_name='ultrasound_result_payment')
    price = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='ultrasound_results', null=True, blank=True)
    result_code = models.CharField(max_length=20, editable=False, unique=True)  # store ULTS1000 etc.
    cleared = models.BooleanField(default=False)
    collected = models.DateField(auto_now_add=True, null=True, blank=True)
    collected_by = models.ForeignKey(User, null=True, blank=True, related_name='ultrasound_collected', on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name='ultrasound_reported', on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.result_code:
            last = Ultrasound.objects.all().order_by('-id').first()  # safer than result_code sort
            # Or extract max number correctly:
            existing = Ultrasound.objects.filter(result_code__startswith='ULTS')
            if existing.exists():
                nums = existing.exclude(result_code='').values_list('result_code', flat=True)
                max_num = max(int(rc[4:]) for rc in nums if rc[4:].isdigit())
                next_num = max_num + 1
            else:
                next_num = 1000
            self.result_code = f"ULTS{next_num:04d}"
        super().save(*args, **kwargs)

    def get_result_code_number(self):
        """Returns the numeric part of result_code as integer."""
        if self.result_code and self.result_code.startswith('ULTS'):
            return int(self.result_code[4:])
        return None

    def __str__(self):
        if self.patient:
            return f"{self.patient}"
        return f"Ultrasound Report {self.result_code}"


class LetterMessage(models.Model):
    subject = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(help_text="Enter the message you want to include on the letterhead.")
    recipient_name = models.CharField("Recipient Name", max_length=200, blank=True, null=True)
    recipient_address = models.TextField("Recipient Address", blank=True, null=True, help_text="Use line breaks for multi-line address.")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject or f"Message {self.id}"

    class Meta:
        ordering = ['-created']