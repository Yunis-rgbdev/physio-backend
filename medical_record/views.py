# medical_records/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from .serializers import MedicalFileSerializer
from patients.models import Patient
from medical_file.models import MedicalFile

class AddVASScoreView(APIView):
    """
    POST endpoint to create a new medical file entry
    Expected JSON format:
    {
        "patient_national_code": "1234567890",
        "operator_national_code": "0987654321",
        "vas_score": 7,
        "doctor_notes": "Patient shows improvement",
        "date_of_file": "2025-11-27"  // optional, defaults to today
    }
    """
    permission_classes = [AllowAny]  # Changed from AllowAny for security
    
    def post(self, request, *args, **kwargs):
        serializer = MedicalFileSerializer(data=request.data)
    
        if serializer.is_valid():
            medical_file_instance = serializer.save()
        
            # Return success response with manually constructed data
            return Response(
                {
                    "message": "Medical file created successfully",
                    "data": {
                        "id": medical_file_instance.id,
                        "vas_score": medical_file_instance.vas_score,
                        "doctor_notes": medical_file_instance.doctor_notes,
                        "date_of_file": str(medical_file_instance.date_of_file),
                    }
                },
                status=status.HTTP_201_CREATED
            )
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def get(self, request, national_code, *args, **kwargs):
        try:
            patient = Patient.objects.get(user__national_code=national_code)
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found"}, status=404)

        files = MedicalFile.objects.filter(medical_record__patient=patient)

        serializer = MedicalFileReadSeriallizer(files, many=True)
        return Response(serializer.data, status=200)