#medical_record/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from datetime import timedelta
from django.utils import timezone
from medical_file.models import MedicalFile

def update_patient_vas_average(patient):
    """
    Calculates the average VAS score for the last 5 days 
    for the given patient and updates the Patient model.
    """
    end_date = timezone.localdate()
    start_date = end_date - timedelta(days=4)
    
    recent_scores = MedicalFile.objects.filter(
        medical_record__patient=patient, 
        date_of_file__range=(start_date, end_date)
    ).aggregate(
        average_vas=Avg('vas_score')
    )
    
    new_average = recent_scores.get('average_vas')
    
    if patient.vas_5day_average != new_average:
        patient.vas_5day_average = new_average
        # FIXED: was 'vas_average', should be 'vas_5day_average'
        patient.save(update_fields=['vas_5day_average'])


@receiver([post_save, post_delete], sender=MedicalFile)
def recalculate_vas_on_change(sender, instance, **kwargs):
    """
    Triggered whenever a MedicalFile (daily score) is saved or deleted.
    """
    patient = instance.medical_record.patient
    update_patient_vas_average(patient)