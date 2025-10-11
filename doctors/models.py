# doctors/models.py
# from django.db import models
# from authenticationapp.models import Auth

# class Doctor(models.Model):
#     auth = models.OneToOneField(Auth, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)  # Add name field to Doctor model
#     role = models.CharField(max_length=20, choices=(("PATIENT","Patient"),("DOCTOR","Doctor")), default="DOCTOR")  # Add role field
#     specialty = models.CharField(max_length=255, blank=True, null=True)
#     clinic_address = models.TextField(blank=True, null=True)
#     phone_number = models.CharField(max_length=15, blank=True, null=True)

#     def save(self, *args, **kwargs):
#         # Sync name and role from Auth model
#         if self.auth:
#             self.name = self.auth.name
#             self.role = self.auth.role
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.name} ({self.auth.national_code})"
