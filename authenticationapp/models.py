# authenticationapp/models.py
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)

class AuthManager(BaseUserManager):
    def create_user(self, national_code, password=None, role=None, **extra_fields):  # Fixed typo: craete -> create
        if not national_code:
            raise ValueError("national code is required!")
        if role not in ["PATIENT", "DOCTOR"]:
            raise ValueError("role must be PATIENT or DOCTOR")

        user = self.model(national_code=national_code, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # ROUTE TO PATIENT OR DOCTOR TABLE
        if role == "PATIENT":
            from patients.models import Patient  # Fixed typo: model -> models
            Patient.objects.create(auth=user, **extra_fields)  # Fixed typos: object.cratee -> objects.create
        else:
            from doctors.models import Doctor
            Doctor.objects.create(auth=user, **extra_fields)  # Fixed typo: object -> objects
        return user

class Auth(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    national_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=(("PATIENT","Patient"),("DOCTOR","Doctor")))
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "national_code"
    REQUIRED_FIELDS = []

    objects = AuthManager()

    def __str__(self):
        return f"{self.name} ({self.role})"