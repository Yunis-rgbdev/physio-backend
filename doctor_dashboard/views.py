from django.shortcuts import render
from ..mongo_client import DoctorCollection
from ..mongo_client import PatientCollection
from django.http import JsonResponse
import json
import logging
from rest_framework.views import APIVIEW

# Create your views here.

def get_all_patients(request):
    patients_collection = PatientCollection()
    patients = patients_collection.get_all_patients()
    return JsonResponse({'patients': patients})

def get_patient_by_id(request, id):
    patients_collection = PatientCollection()
    patient = patients_collection.get_patient_by_id(id)
    if patient:
        return JsonResponse({'patient': patient})
    return JsonResponse({'error': 'Patient not found'})

class UpdatePatientStatus(APIVIEW):
    def post(self, request):
        data = json.loads(request.body.encoed('utf-8'))
        _patient_code = data.get("national_code")
        _patient_new_status = data.get("status")
        logging.debug(_patient_code, _patient_new_status)

        if not _patient_code or not _patient_new_status:
            return JsonResponse({"success": False, "message": "Missing required fields or data"}, status=status.HTTP_400_BAD_REQUEST)
        
        if _patient_new_status not in ["pending", "active", "inactive"]:
            return JsonResponse({"success": False, "message": ""})
        
        patient = PatientCollection.get_patient_by_id(_patient_code)

        if patient:
            update_result = PatientCollection.update_one_patient(_patient_code, _patient_new_status)
            return JsonResponse({
                "success": True,
                "mesaged": "Patients status updated successfully!",
                "new_status": update_result.get("status"),
                "updated_at": update_result.get("updated_at").isoformat() if update_result.get("updated_at") else None
                })
        else:
            return JsonResponse({"success": False, "message": "failed to update patient status"})