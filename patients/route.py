from django.urls import path
from .views import FhirPatientView, FhirPatientDetail

urlpatterns = [
    path("patients/", FhirPatientView.as_view(), name="fhir_patient_create_or_upsert"),
    path("patients/<int:pk>/", FhirPatientDetail.as_view(), name="fhir_patient_detail"),
]