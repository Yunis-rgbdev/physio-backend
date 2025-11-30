from django.db import models

# Create your models here.

class MedicalRecord(models.Model):
    patient = models.ForeignKey(
        Patient, 
        on_delete=models.CASCADE, 
        related_name='medical_records'
    )
    created_at = models.DateTimeField(default=timezone.now)
    
    # The medical data you mentioned
    vas_score = models.IntegerField(help_text="Visual Analog Scale (0-10)")
    vas_average = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        blank=True, 
        null=True,
        help_text="Calculated average for this period"
    )
    doctor_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Record for {self.patient} on {self.created_at.date()}"