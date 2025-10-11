import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, national_code, password, **extra_fields):
        if not national_code:
            raise ValueError("national_code requiered")

        user = self.model(national_code=national_code, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, national_code, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        return self._create_user(national_code, password, **extra_fields)

    def create_superuser(self, national_code, password, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        return self._create_user(national_code, password, **extra_fields)

    
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    national_code = models.IntegerField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    ROLE_SUPERVISOR = 1
    ROLE_PATIENT = 2
    ROLE_PHYSIOTHERAPIST = 3
    ROLE_INTERNSHIP = 4

    ROLE_CHOICES = [
        (ROLE_SUPERVISOR, "SUPERVISOR"),
        (ROLE_PATIENT, "PATIENT"),
        (ROLE_PHYSIOTHERAPIST, "PHYSIOTHERAPIST"),
        (ROLE_INTERNSHIP, "INTERNSHIP"),
    ]

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=ROLE_PATIENT)

    USERNAME_FIELD = "national_code"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        indexes = [models.Index(fields=["national_code"])]

    def __str__(self):
        return f"{self.national_code} ({self.get_role_display()})"

    # role helpers
    @property
    def is_patient(self):
        return self.role == self.ROLE_PATIENT

    @property
    def is_operator(self):
        return self.role in [self.ROLE_SUPERVISOR, self.ROLE_PHYSIOTHERAPIST, self.ROLE_INTERNSHIP]

    def get_profile(self):
        """Return the related profile object depending on role"""
        if self.is_patient:
            return getattr(self, "patient_profile", None)
        elif self.is_operator:
            return getattr(self, "operator_profile", None)
        return None






        


