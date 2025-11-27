from django.shortcuts import render
from .models import Operator
from accounts.models import User;
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from medical_file.models import MedicalFile
from medical_record.serializers import MedicalFileReadSeriallizer

# Create your views here.
# def search_operator(request):
    


class OperatorServiceView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, mode, national_code, *args, **kwargs):
        if mode == "srch":
            return self.post_operator(national_code)
        elif mode == "getvas":
            return self.post_active_sessions_vas(national_code)

    def post_operator(self, op_national_code):
        if op_national_code:
            operator = Operator.objects.get(user__national_code=op_national_code)

            data = {
                "full_name": operator.full_name,
                "speciality": operator.speciality,
                "phone": operator.phone,
                "email": operator.user.email,
                "national_code": operator.user.national_code
            }
            return Response(data, status=200)
        else:
            return Response({"error": "could not find operator"})
    
    def post_active_sessions_vas(self, op_national_code):
        try:
            if not op_national_code:
                return Response({"error": "Operator national code required"}, status=400)

            operator = Operator.objects.get(user__national_code=op_national_code)

            # Filter based on operator + only active medical records
            files = MedicalFile.objects.filter(
                medical_record__operator=operator,
                medical_record__is_active=True
            )

            serializer = MedicalFileReadSeriallizer(files, many=True)
            return Response(serializer.data, status=200)

        except Operator.DoesNotExist:
            return Response({"error": "Operator not found"}, status=404)

        except Exception as e:
            return Response({"error": str(e)}, status=500)









        # national_code = request.GET.get('national_code')

        # if not national_code:
        #     return JsonResponse({'error': 'national_code is required'}, status=400)

        # try:
        #     # Fetch the user and the related patient_profile in one query
        #     user = User.objects.select_related('operator_profile').get(national_code=national_code)

        #     # Prepare the response
        #     data = {
        #         'id': str(user.id),
        #         'national_code': user.national_code,
        #         'full_name': user.full_name,
        #         'role': user.role,
        #         'is_active': user.is_active,
        #         'is_staff': user.is_staff,
        #         'date_joined': user.date_joined,
        #         'last_login': user.last_login,
        #     }

        #     # If operator profile exists, sssssadd its data
        #     operator = getattr(user, 'operator_profile', None)
        #     if operator:
        #         data.update({
        #             'specialty': operator.specialty,
        #             'clinic_address': operator.clinic_address,
        #             'phone_number': operator.phone_number,
        #             'nezam_pezeshki_code': operator.nezam_pezeshki_code,
        #             'student_code': operator.student_code,         
        #         })

        #     return JsonResponse(data)

        # except User.DoesNotExist:
        #     return JsonResponse({'error': 'Patient not found'}, status=404)