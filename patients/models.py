# patients/models.py
import uuid
from django.db import models
from django.conf import settings


class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_profile"
    )
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    meta = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Patient: {self.user.full_name or self.user.national_code}"