# authenticationapp/models.py
from django.db import models                      # Django's ORM tools (fields, Model, etc.)
from django.contrib.auth.models import (
    AbstractBaseUser,    # gives password handling (but NO username field)
    PermissionsMixin,    # adds groups/permissions fields & helper methods
    BaseUserManager      # base class we extend to create custom user-manager methods
)

# A manager: helper object to create users and superusers cleanly
class CustomUserManager(BaseUserManager):
    def create_user(self, national_code, password=None, **extra_fields):
        """
        Create and save a regular user.
        national_code: required unique id for our users
        password: plain-text password (we'll hash it below)
        **extra_fields: any other model fields (name, phone_number, role, etc.)
        """
        if not national_code:
            raise ValueError("Users must have a national_code")

        # instantiate a user model but don't save yet
        user = self.model(national_code=national_code, **extra_fields)

        # hash the password and attach it to the user object
        user.set_password(password)

        # save to the database (use configured DB alias)
        user.save(using=self._db)
        return user

    def create_superuser(self, national_code, password=None, **extra_fields):
        """
        Create and save a superuser (admin).
        We set is_staff and is_superuser flags to True.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(national_code, password, **extra_fields)


# The custom user model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    national_code = models.CharField(max_length=20, unique=True)  # our login field
    name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    age = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(default="sleep") # pending for request

    ROLE_CHOICES = (
        ("PATIENT", "Patient"),
        ("DOCTOR", "Doctor"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="PATIENT")

    # standard admin flags
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # tell Django which field is used as the unique identifier
    USERNAME_FIELD = "national_code"
    REQUIRED_FIELDS = []  # if you add other required fields for createsuperuser, list them here

    # assign our manager
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.national_code} ({self.role})"
