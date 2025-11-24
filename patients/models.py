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
    email = models.EmailField(blank=True, null=True)
    meta = models.JSONField(default=dict, blank=True)
    emergency_contact_name = models.CharField(max_length=200, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True)
    emergency_contact_relation = models.CharField(max_length=50, blank=True, null=True)
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # THE CACHED FIELD: Stores the calculated 5-day average
    vas_average = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Automatically calculated average of the last 5 VAS scores."
    )

    def __str__(self):
        return f"Patient: {self.user.full_name or self.user.national_code}"