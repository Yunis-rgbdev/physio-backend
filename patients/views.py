from django.shortcuts import render
from .models import Patient
from accounts.models import User;
from django.http import JsonResponse

# Create your views here.
def search_patients(request):
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
            'full_name': user.full_name,
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


def get_patients_by_operator(request):
    operator_national_code = request.GET.get('national_code')

    if not operator_national_code:
        return JsonResponse({'error': 'Operator national code is required'}, status=400)

    try:
        # Fetch the user and the related patient_profile in one query
        user = User.objects.select_related('patient_profile').get(national_code=operator_national_code)

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


    
