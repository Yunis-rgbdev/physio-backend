from django.shortcuts import render
from .models import Operator
from accounts.models import User;
from django.http import JsonResponse

# Create your views here.
def search_operator(request):
    national_code = request.GET.get('national_code')

    if not national_code:
        return JsonResponse({'error': 'national_code is required'}, status=400)

    try:
        # Fetch the user and the related patient_profile in one query
        user = User.objects.select_related('operator_profile').get(national_code=national_code)

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

        # If operator profile exists, sssssadd its data
        operator = getattr(user, 'operator_profile', None)
        if operator:
            data.update({
                'specialty': operator.specialty,
                'clinic_address': operator.clinic_address,
                'phone_number': operator.phone_number,
                'nezam_pezeshki_code': operator.nezam_pezeshki_code,
                'student_code': operator.student_code,         
            })

        return JsonResponse(data)

    except User.DoesNotExist:
        return JsonResponse({'error': 'Patient not found'}, status=404)