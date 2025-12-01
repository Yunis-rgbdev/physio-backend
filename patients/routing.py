# patients/routing.py
from django.urls import path
from .views import PatientServiceView

patient_view = PatientServiceView.as_view({
    "get": "search",
})

update_active_medical_file_view = PatientServiceView.as_view({
    "post": "update_active_session",
})

urlpatterns = [
    # path("patients/", FhirPatientView.as_view(), name="fhir_patient_create_or_upsert"),
    path("search/", patient_view, name="patient_detail"),
    path("odpatients/<str:national_code>/", update_active_medical_file_view, name="patient_fetch")
]