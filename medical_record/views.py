# medical_records/views.py

from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import MedicalFileSerializer, MedicalFileReadSeriallizer
from patients.models import Patient
from operators.models import Operator
from medical_file.models import MedicalFile

class MedicalFilesViewSet(ViewSet):
    # Set to IsAuthenticated for security, as you noted in the original code.
    # You may need to refine this with custom permissions (e.g., is the user the doctor/patient?).
    permission_classes = [AllowAny]
    
    # --- CRUD: CREATE (POST) ---
    
    def create(self, request):
        """Creates a new MedicalFile instance."""
        serializer = MedicalFileSerializer(data=request.data)
    
        if serializer.is_valid():
            medical_file_instance = serializer.save()
        
            # Use the Read Serializer for consistent output data structure
            read_serializer = MedicalFileReadSeriallizer(medical_file_instance)
            
            return Response(
                {
                    "message": "Medical file created successfully",
                    "data": read_serializer.data,
                },
                status=status.HTTP_201_CREATED
            )
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # --- CUSTOM ACTIONS: RETRIEVE (GET) ---
    
    @action(detail=False, methods=['get'], url_path=r'patient/(?P<national_code>\w+)')
    def get_by_patient(self, request, national_code=None):
        """Retrieves all medical files associated with a specific patient by national_code."""
        try:
            patient = Patient.objects.get(user__national_code=national_code)
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

        # Assuming 'medical_record' is a ForeignKey on MedicalFile pointing to a record that links to Patient
        files = MedicalFile.objects.filter(medical_record__patient=patient)

        serializer = MedicalFileReadSeriallizer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path=r'operator/(?P<national_code>\w+)')
    def get_by_operator(self, request, national_code=None):
        """Retrieves all medical files associated with a specific operator by national_code."""
        try:
            operator = Operator.objects.get(user__national_code=national_code)
        except Operator.DoesNotExist:
            return Response({"error": "Operator not found"}, status=status.HTTP_404_NOT_FOUND)

        # Assuming 'medical_record' is a ForeignKey on MedicalFile pointing to a record that links to Operator
        files = MedicalFile.objects.filter(medical_record__operator=operator)

        serializer = MedicalFileReadSeriallizer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # --- CRUD: UPDATE (PUT/PATCH) ---
    
    def update(self, request, pk=None):
        """Updates a medical file by its ID (pk)."""
        try:
            medical_file = MedicalFile.objects.get(pk=pk)
        except MedicalFile.DoesNotExist:
            return Response({"error": "Medical file not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Use the MedicalFileSerializer for updating
        serializer = MedicalFileSerializer(medical_file, data=request.data, partial=True) # partial=True allows PATCH requests
        
        if serializer.is_valid():
            updated_instance = serializer.save()
            
            # Use the Read Serializer for the response
            read_serializer = MedicalFileReadSeriallizer(updated_instance)
            
            return Response(
                {
                    "message": f"Medical file {pk} updated successfully",
                    "data": read_serializer.data,
                },
                status=status.HTTP_200_OK
            )
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # --- CRUD: DESTROY (DELETE) ---
    
    def destroy(self, request, pk=None):
        """Deletes a medical file by its ID (pk)."""
        try:
            medical_file = MedicalFile.objects.get(pk=pk)
        except MedicalFile.DoesNotExist:
            return Response({"error": f"Medical file with ID {pk} not found"}, status=status.HTTP_404_NOT_FOUND)
            
        medical_file.delete()
        
        return Response(
            {"message": f"Medical file {pk} deleted successfully"}, 
            status=status.HTTP_204_NO_CONTENT
        )