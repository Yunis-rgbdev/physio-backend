from django.shortcuts import render
from .models import Operator
from accounts.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.http import JsonResponse
from medical_file.models import MedicalFile
from medical_record.serializers import MedicalFileReadSeriallizer

# Create your views here.

class OperatorServiceView(ViewSet):
    permission_classes = [AllowAny]

    def get_operator(self, national_code):
        try:
            return Operator.objects.get(user__national_code=national_code)
        except Operator.DoesNotExist:
            return None

    def search(self, request, national_code=None):
        operator = self.get_operator(national_code)
        if not operator:
            return Response({"error": "Operator not found"}, status=404)

        data = {
            "full_name": operator.full_name,
            "speciality": operator.speciality,
            "phone": operator.phone,
            "email": operator.user.email,
            "national_code": operator.user.national_code,
        }
        return Response(data, status=200)

    def active_sessions(self, request, national_code=None):
        operator = self.get_operator(national_code)
        if not operator:
            return Response({"error": "Operator not found"}, status=404)

        files = MedicalFile.objects.filter(
            medical_record__operator=operator,
            medical_record__is_active=True
        )

        serializer = MedicalFileReadSeriallizer(files, many=True)
        return Response(serializer.data, status=200)