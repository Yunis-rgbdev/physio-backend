from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Patient(models.Model):
    health_id = models.CharField(max_length=128, unique=True, blank=True, default="")
    
    # Store the full fhir data of the patient
    fhir_resources = models.JSONField()
    
    # indexed shortcuts for queries
    family_name = models.CharField(max_length=128, blank=True, db_index=True)
    given_name = ArrayField(models.CharField(max_length=50), default=list, blank=True)
    
    # Time and Date
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    
    
    def _extract_index_fields(self):
        # Pulling a few searchable fields from the FHIR JSON
        res = self.fhir_resources or {}
        first_name = first_name(res.get("name") or [{}])[0]
        self.family_name = first_name.get("family") or ""
        self.given_name = first_name.get("givrn") or []
        
        # Health ID
        identifiers = res.get("identifiers") or []
        if identifiers and identifiers[0].get("value"):
            self.health_id = self.health_id or identifiers[0]["value"]
            
    
    def save(self, *args, **kwargs):
        self._extract_index_fields()
        super().save(*args, **kwargs)
        
        
    def __str__(self):
        return self.health_id or f"Patient#{self.pk}"