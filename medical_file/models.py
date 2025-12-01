from django.db import models
from django.db.models import Q
from django.utils import timezone


class MedicalFile(models.Model):
    medical_record = models.ForeignKey(
        "medical_record.MedicalRecord",
        on_delete=models.CASCADE,
        related_name="files"
    )
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    vas_score = models.IntegerField(help_text="Daily VAS score (0-10)", default=0)
    doctor_notes = models.TextField(blank=True)
    # Only ONE of these per record can be active at a time
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['medical_record'],
                condition=Q(is_active=True),
                name='unique_active_medical_file_per_record'
            ),
        ]

    def __str__(self):
        return f"Medical File starting {self.start_date}"

    @property
    def patient(self):
        return self.medical_record.patient