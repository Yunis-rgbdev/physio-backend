# medical_record/serializers.py
from rest_framework import serializers
from .models import MedicalRecord
from medical_file.models import MedicalFile
from patients.models import Patient
from operators.models import Operator  # Adjust if your app name is different

class MedicalFileSerializer(serializers.ModelSerializer):
    patient_national_code = serializers.CharField(write_only=True)
    operator_national_code = serializers.CharField(write_only=True)

    date_of_file = serializers.DateField(required=False)
    
    class Meta:
        model = MedicalFile
        fields = [
            'id', 
            'vas_score', 
            'doctor_notes', 
            'date_of_file',
            'patient_national_code',
            'operator_national_code'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        patient_national_code = validated_data.pop('patient_national_code')
        operator_national_code = validated_data.pop('operator_national_code')
        
        # Changed: Use user__national_code to search through relationship
        try:
            patient = Patient.objects.get(user__national_code=patient_national_code)
        except Patient.DoesNotExist:
            raise serializers.ValidationError(
                {"patient_national_code": f"Patient with national code {patient_national_code} not found"}
            )
        
        try:
            operator = Operator.objects.get(user__national_code=operator_national_code)
        except Operator.DoesNotExist:
            raise serializers.ValidationError(
                {"operator_national_code": f"Operator with national code {operator_national_code} not found"}
            )
        
        medical_record, created = MedicalRecord.objects.get_or_create(
            patient=patient,
            operator=operator,
            is_active=True,
            defaults={
                'document_id': f"MR-{patient.user.national_code}-{operator.user.national_code}"
            }
        )
        
        medical_file = MedicalFile.objects.create(
            medical_record=medical_record,
            **validated_data
        )
        
        return medical_file



# {
#   "patient_national_code": "0928019589",
#   "operator_national_code": "0928013456", 
#   "vas_score": 7,
#   "doctor_notes": "..."
# }