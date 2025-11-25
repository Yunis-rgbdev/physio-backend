# medical_record/models.py
from django.db import models
from patients.models import Patient

# Create your models here.
class MedicalRecord(models.Model):
    """
    This is the 'Big Folder'. It might represent a specific injury (e.g., 'Leg Fracture 2024')
    or a long-term case.
    """
    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.CASCADE,
        related_name="medical_records"
    )
    case_name = models.CharField(max_length=200) # e.g. "Left Knee Surgery"
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Case: {self.case_name} ({self.patient})"