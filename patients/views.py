# patients/views.py
from django.shortcuts import render
from .models import Patient
from accounts.models import User;
from django.http import JsonResponse
from operators.models import Operator
from rest_framework.permissions import AllowAny
from medical_file.models import MedicalFile

# Create your views here.
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from medical_file.models import MedicalFile
from medical_record.models import MedicalRecord

class PatientServiceView(ViewSet):
    permission_classes = [AllowAny]
    # @action(detail=True, methods=['patch'], url_path='active-session')
    def update_active_session(self, request, national_code=None):
        try:
            record = MedicalRecord.objects.get(patient__user__national_code=national_code)
        except MedicalRecord.DoesNotExist:
            return Response({"error": "Medical record not found"}, status=status.HTTP_404_NOT_FOUND)

        # 2. Get the active medical file
        try:
            active_file = MedicalFile.objects.get(medical_record=record, is_active=True)
        except MedicalFile.DoesNotExist:
            return Response({"error": "No active session exists"}, status=status.HTTP_404_NOT_FOUND)

        # 3. Update allowed fields directly
        allowed_fields = ["vas_score", "notes"]  # add more if needed
        for field in allowed_fields:
            if field in request.data:
                setattr(active_file, field, request.data[field])

        active_file.save()

        return Response({
            "message": "Active session updated successfully",
            "updated_data": {field: getattr(active_file, field) for field in allowed_fields}
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def search(self, request):
        national_code = request.GET.get('national_code')

        if not national_code:
            return JsonResponse({'error': 'national_code is required'}, status=400)

        try:
            # Fetch the user and the related patient_profile in one query
            user = User.objects.select_related('patient_profile').get(national_code=national_code)

            # Prepare the response
            data = {
                'id': str(user.id),
                'national_code': user.national_code,
                # 'full_name': user.full_name,
                'role': user.role,
                'is_active': user.is_active,
                'is_staff': user.is_staff,
                'date_joined': user.date_joined,
                'last_login': user.last_login,
            }

            # If patient profile exists, add its data
            patient = getattr(user, 'patient_profile', None)
            if patient:
                data.update({
                    'birth_date': patient.birth_date,
                    'gender': patient.gender,
                    'phone_number': patient.phone_number,
                    'full_name': patient.full_name,
                    'email': patient.email,
                    'emergency_contact_name': patient.emergency_contact_name,
                    'emergency_contact_phone': patient.emergency_contact_phone,
                    'emergency_contact_relation': patient.emergency_contact_relation,
                    'meta': patient.meta,
                    'patient_created_at': patient.created_at,
                    'patient_updated_at': patient.updated_at,
                })

            return JsonResponse(data)

        except User.DoesNotExist:
            return JsonResponse({'error': 'Patient not found'}, status=404)

    def get_patients_by_operator(request, op_national_code):
        if not op_national_code:
            return JsonResponse({'error': 'Operator national code is required'}, status=400)
        else:
            try:
                operator = Operator.objects.get(user__national_code=op_national_code)
            except Operator.DoesNotExist:
                return Response({"error": "Operator not found"}, status=404)
    
        files = MedicalFile.objects.filter(medical_record__operator=operator)

        try:

            data = {
                'national_code': user.national_code,
                'full_name': user.full_name,
                'is_active': user.is_active,
                'last_login': user.last_login
            }
        
            patient = getattr(user, 'patient_profile', None)
            if patient:
                data.update({
                    'vas_avg': patient.vas_average 
                })
            return JsonResponse(data)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Patient not found'}, status=404)



