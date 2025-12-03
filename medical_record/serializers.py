# medical_record/serializers.py
from rest_framework import serializers
from .models import MedicalRecord
from patients.models import Patient
from operators.models import Operator

class MedicalRecordSerializer(serializers.ModelSerializer):
    pass

class MedicalRecordReadSerializer(serializers.ModelSerializer):
    patient_national_code = serializers.CharField(source="medical_record.patient.user.national_code", read_only=True)
    operator_national_code = serializers.CharField(source="medical_record.operator.user.natioanl_code", read_only=True)

    class Meta:
        model = MedicalRecord
        fields = [
            "id",
            "document_id",
            "is_active",
            "patient_id",
            "operator_id",
            "patient_national_code",
            "operator_national_code"
        ]