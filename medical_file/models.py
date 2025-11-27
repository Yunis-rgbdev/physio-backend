from django.db import models
from django.utils import timezone

class MedicalFile(models.Model):
    medical_record = models.ForeignKey(
        "medical_record.MedicalRecord",
        on_delete=models.CASCADE,
        related_name="files"
    )
    date_of_file = models.DateField(default=timezone.now)
    
    # DAILY LOGS
    vas_score = models.IntegerField(help_text="Daily VAS score (0-10)")
    doctor_notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-date_of_file"]
        indexes = [
            models.Index(fields=["medical_record", "-date_of_file"]),
        ]

    def __str__(self):
        return f"Visit on {self.date_of_file} (VAS: {self.vas_score})"

    @property
    def patient(self):
        return self.medical_record.patient