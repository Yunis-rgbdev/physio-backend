from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from datetime import timedelta
from django.utils import timezone

from medical_file.models import MedicalFile # The model that holds the daily score

# Function to calculate and update the patient's 5-day average
def update_patient_vas_average(patient):
    """
    Calculates the average VAS score for the last 5 days 
    for the given patient and updates the Patient model.
    """
    # 1. Calculate the 5-day time window
    end_date = timezone.localdate()
    # The last 5 days means today (day 1) and the 4 preceding days.
    start_date = end_date - timedelta(days=4) 

    # 2. Query the daily scores for the patient within the window
    recent_scores = MedicalFile.objects.filter(
        # Traverse up from MedicalFile -> MedicalRecord -> Patient
        medical_record__patient=patient, 
        date_of_file__range=(start_date, end_date)
    ).aggregate(
        # Perform the average calculation on the database side
        average_vas=Avg('vas_score')
    )
    
    # 3. Update the cached field on the Patient model
    new_average = recent_scores.get('average_vas')
    
    if patient.vas_5day_average != new_average:
        patient.vas_5day_average = new_average
        patient.save(update_fields=['vas_5day_average']) # Save ONLY the average field


@receiver([post_save, post_delete], sender=MedicalFile)
def recalculate_vas_on_change(sender, instance, **kwargs):
    """
    Triggered whenever a MedicalFile (daily score) is saved or deleted.
    """
    # Get the patient instance through the MedicalRecord
    patient = instance.medical_record.patient
    update_patient_vas_average(patient)