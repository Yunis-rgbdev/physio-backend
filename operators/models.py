# operators/models.py
import uuid
from django.db import models
from django.conf import settings

class Operator(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="operator_profile"
    )
    student_code = models.IntegerField(unique=True, blank=True, null=True)
    nezam_pezeshki_code = models.IntegerField(unique=True, blank=True, null=True)
    specialty = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    clinic_address = models.TextField(blank=True, null=True)
    national_code = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Operator: {self.user.full_name or self.user.national_code}"