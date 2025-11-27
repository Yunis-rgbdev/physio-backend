# medical_record/models.py
from django.db import models
from patients.models import Patient
from operators.models import Operator

class MedicalRecord(models.Model):
    """
    Bridge table: Links Patient + Operator to their medical files
    """
    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.CASCADE,
        related_name="medical_records"
    )
    operator = models.ForeignKey(
        "operators.Operator",
        on_delete=models.SET_NULL,
        null=True,
        related_name="medical_records"
    )
    document_id = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Case: {self.document_id} - Patient: {self.patient.national_code}"