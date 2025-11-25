# medical_file/models.py
from django.db import models
from django.utils import timezone

class MedicalFile(models.Model):
    """
    Represents a specific visit, treatment session, or sub-file inside a MedicalRecord.
    This is where daily VAS scores and visit notes are stored.
    """

    # Link to the main record
    medical_record = models.ForeignKey(
        "medical_record.MedicalRecord",
        on_delete=models.CASCADE,
        related_name="files"
    )

    date_of_file = models.DateField(default=timezone.now)

    # Daily log fields
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
        """Shortcut: access patient through the medical record."""
        return self.medical_record.patient
