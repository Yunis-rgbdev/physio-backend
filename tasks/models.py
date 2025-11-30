# tasks/models.py
from django.db import models
from patients.models import Patient
from operators.models import Operator

# Create your models here.
class Tasks(models.Model):
    STATUS_CHOICES = {
        ('compelete', 'Completed'),
        ('ongoing', 'OnGoing'),
        ('ignored', 'Ignored'),
    }
    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    operator = models.ForeignKey(
        "operators.Operator",
        on_delete=models.SET_NULL,
        null=True,
        related_name="tasks"
    )
    last_update_at = models.DateTimeField(auto_now_add=True)
    task_date = models.DateField()
    title = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ongoing')
    operator_note = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"Task created on { self.last_update_at } for date { self.task_date }"