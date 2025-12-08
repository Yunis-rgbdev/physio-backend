# medical_file/serializers.py
from rest_framework import serializers
from .models import MedicalFile
from medical_record.models import MedicalRecord
from .models import MedicalFile
from patients.models import Patient
from operators.models import Operator  # Adjust if your app name is different

class MedicalFileSerializer(serializers.ModelSerializer):
    patient_national_code = serializers.CharField(write_only=True)
    operator_national_code = serializers.CharField(write_only=True)

    start_date = serializers.DateField(required=False)
    
    class Meta:
        model = MedicalFile
        fields = [
            'id', 
            'vas_score', 
            'doctor_notes', 
            'start_date',
            'end_date',
            'patient_national_code',
            'operator_national_code'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        patient_national_code = validated_data.pop('patient_national_code')
        operator_national_code = validated_data.pop('operator_national_code')

        patient = Patient.objects.get(user__national_code=patient_national_code)
        operator = Operator.objects.get(user__national_code=operator_national_code)

        medical_record, _ = MedicalRecord.objects.get_or_create(
            patient=patient,
            operator=operator,
            defaults={'document_id': f"MR-{patient.user.national_code}-{operator.user.national_code}"}
        )

        # Deactivate any previous active session
        MedicalFile.objects.filter(
            medical_record=medical_record,
            is_active=True
        ).update(is_active=False)

        # Create the new active session
        medical_file = MedicalFile.objects.create(
            medical_record=medical_record,
            **validated_data,
            is_active=True
        )

        return medical_file




class MedicalFileReadSeriallizer(serializers.ModelSerializer):
    patient_national_code = serializers.CharField(source="medical_record.patient.user.national_code", read_only=True)
    operator_national_code = serializers.CharField(source="medical_record.operator.user.national_code", read_only=True)

    class Meta:
        model = MedicalFile
        fields = [
            "id",
            "start_date",
            "end_date",
            'doctor_notes',
            "vas_score",
            "patient_national_code",
            "operator_national_code",
            "is_active"
        ]


# {
#   "patient_national_code": "0928019589",
#   "operator_national_code": "0928013456", 
#   "vas_score": 5,
#   "doctor_notes": "updated note"
# }