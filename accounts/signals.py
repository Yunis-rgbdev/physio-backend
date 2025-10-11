# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import User
from patients.models import Patient
from operators.models import Operator

@receiver(post_save, sender=User)
def create_role_profile(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.is_patient:
        Patient.objects.create(user=instance)
    elif instance.is_operator:
        Operator.objects.create(user=instance)
