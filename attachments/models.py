from django.db import models

# Create your models here.
class Attachment(models.Model):
    """
    Files are owned by the Patient, but can be linked to a specific MedicalFile.
    """
    patient = models.ForeignKey(
        Patient, 
        on_delete=models.CASCADE, 
        related_name='attachments'
    )
    
    # LINK: Now points to the specific MedicalFile (Layer 2), not the generic Record
    medical_file = models.ForeignKey(
        MedicalFile, 
        on_delete=models.SET_NULL, # If you delete the file, keep the attachment
        null=True, 
        blank=True, 
        related_name='attachments'
    )

    file = models.FileField(upload_to='uploads/%Y/%m/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment {self.id}"