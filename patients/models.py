# patients/models.py
from django.db import models
from authenticationapp.models import Auth

class Patient(models.Model):
    auth = models.OneToOneField(Auth, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)  # Add name field to Patient model
    role = models.CharField(max_length=20, choices=(("PATIENT","Patient"),("DOCTOR","Doctor")), default="PATIENT")  # Add role field
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    status = models.CharField(max_length=20, choices=(("idle", "Idle"), ("pending","Pending Meeting"), ("active","In Meeting")), default="idle")

    def save(self, *args, **kwargs):
        # Sync name and role from Auth model
        if self.auth:
            self.name = self.auth.name
            self.role = self.auth.role
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.auth.national_code})"
