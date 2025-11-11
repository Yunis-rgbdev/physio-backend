from django.db import models

# Create your models here.
from django.db import models
from accounts.models import Doctor
from patients.models import Patient

class MedicalRecord(models.Model):
    """Main medical record linking doctor and patient"""
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    # Foreign Keys
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name='medical_records')
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name='medical_records')
    
    # Record Information
    record_number = models.CharField(max_length=50, unique=True, editable=False)
    visit_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Chief Complaint
    chief_complaint = models.TextField(help_text="Patient's primary concern")
    
    # Vital Signs
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, help_text="°F")
    blood_pressure_systolic = models.IntegerField(null=True, blank=True)
    blood_pressure_diastolic = models.IntegerField(null=True, blank=True)
    heart_rate = models.IntegerField(null=True, blank=True, help_text="BPM")
    respiratory_rate = models.IntegerField(null=True, blank=True)
    oxygen_saturation = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, help_text="%")
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="kg")
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="cm")
    
    # Clinical Notes
    history_of_present_illness = models.TextField(blank=True)
    physical_examination = models.TextField(blank=True)
    assessment = models.TextField(blank=True)
    treatment_plan = models.TextField(blank=True)
    
    # Follow-up
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True, blank=True)
    follow_up_notes = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'medical_records'
        ordering = ['-visit_date']
        indexes = [
            models.Index(fields=['patient', '-visit_date']),
            models.Index(fields=['doctor', '-visit_date']),
            models.Index(fields=['record_number']),
        ]
    
    def __str__(self):
        return f"{self.record_number} - {self.patient.get_full_name()}"
    
    def save(self, *args, **kwargs):
        if not self.record_number:
            # Generate unique record number
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            self.record_number = f"MR{timestamp}{self.patient.id}"
        super().save(*args, **kwargs)


class Diagnosis(models.Model):
    """Diagnosis related to a medical record"""
    DIAGNOSIS_TYPES = (
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('differential', 'Differential'),
    )
    
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='diagnoses')
    diagnosis_type = models.CharField(max_length=20, choices=DIAGNOSIS_TYPES, default='primary')
    condition = models.CharField(max_length=200)
    icd_code = models.CharField(max_length=20, blank=True, help_text="ICD-10 Code")
    description = models.TextField(blank=True)
    severity = models.CharField(max_length=50, blank=True, help_text="Mild/Moderate/Severe")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'diagnoses'
        verbose_name_plural = 'Diagnoses'
    
    def __str__(self):
        return f"{self.condition} - {self.medical_record.record_number}"


class Prescription(models.Model):
    """Prescription related to a medical record"""
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('discontinued', 'Discontinued'),
    )
    
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='prescriptions')
    medication_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100, help_text="e.g., 500mg")
    frequency = models.CharField(max_length=100, help_text="e.g., Twice daily")
    duration = models.CharField(max_length=100, help_text="e.g., 7 days")
    quantity = models.IntegerField(help_text="Number of pills/units")
    instructions = models.TextField(help_text="Special instructions for patient")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'prescriptions'
    
    def __str__(self):
        return f"{self.medication_name} - {self.medical_record.record_number}"


class Appointment(models.Model):
    """Appointment scheduling"""
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    )
    
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name='appointments')
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name='appointments')
    medical_record = models.OneToOneField(MedicalRecord, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointment')
    
    appointment_date = models.DateTimeField()
    duration_minutes = models.IntegerField(default=30)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'appointments'
        ordering = ['appointment_date']
        indexes = [
            models.Index(fields=['doctor', 'appointment_date']),
            models.Index(fields=['patient', 'appointment_date']),
        ]
    
    def __str__(self):
        return f"{self.patient.get_full_name()} with Dr. {self.doctor.user.get_full_name()} on {self.appointment_date}"