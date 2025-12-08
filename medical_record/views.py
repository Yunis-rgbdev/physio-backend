# medical_records/views.py
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import MedicalRecordReadSerializer
from patients.models import Patient
from operators.models import Operator
from .models import MedicalRecord
from medical_file.models import MedicalFile

class MedicalRecordViewSet(ViewSet):
    permission_classes= [AllowAny]

    @action(detail=False, methods=['get'], url_path=r'operator/(?P<national_code>\w+)')
    def get_by_operator(self, request, national_code=None):
        try:
            op = Operator.objects.get(user__national_code=national_code)
        except Operator.DoesNotExist:
            return Response({"error": "Operator Not Found"}, status=status.HTTP_404_NOT_FOUND)

        record = MedicalRecord.objects.filter(operator=op)
        serializer = MedicalRecordReadSerializer(record, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path=r'patient/(?P<national_code>\w+)')
    def get_by_patient(self, request, national_code=None):
        try:
            pa = Patient.objects.get(user__national_code=national_code)
        except Patient.DoesNotExist:
            return Response({"error": "Patient Not Found"})

        record = MedicalRecord.objects.filter(patient=pa)
        serializer = MedicalRecordReadSerializer(record, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #INCOMPLETE UPDATE FUNCTION
    
    def update(self, request, pk=None):
        try:
            medical_record = MedicalRecord.objects.get(pk=pk)
        except MedicalRecord.DoesNotExist:
            return Response({"error": "Medical record not found"}, status=status.HTTP_404_NOT_FOUND)
         
        serializer = MedicalRecordSerializer(medical_record, data=request.data, partial=True)
        if serializer.is_valid():
            updated_instance = serializer.save()
            read_serializer = MedicalRecordReadSerializer(updated_instance)
            return Response(
                {
                    "message": f"Medical Record { pk } updated successfully",
                    "data": read_serializer.data
                },
                status=status.HTTP_200_OK
            )

    def destroy(self, request, pk=None):
        try: 
            record = MedicalRecord.objects.get(pk=pk)
        except MedicalRecord.DoesNotExist:
            return Response({"error": f"Medical record with ID {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        record.delete()

        return Response(
            {"message": f"Medical record {pk} deleted successfully"}, 
            status=status.HTTP_204_NO_CONTENT
        )
