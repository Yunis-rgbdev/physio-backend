# patients/routing.py
from django.urls import path
from . import views

urlpatterns = [
    # path("operators/", FhirPatientView.as_view(), name="fhir_patient_create_or_upsert"),
    path("search/", views.search_operator, name="operator_detail"),
]