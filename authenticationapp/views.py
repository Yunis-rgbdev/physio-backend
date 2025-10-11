# # authenticatationapp/views.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework import generics
# from rest_framework.permissions import AllowAny
# # from .models import Auth
# from .serializers import Patient_Register_Serializer, Doctor_Register_Serializer
# from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.utils import timezone


# class LoginView(APIView):
#     permission_classes = [AllowAny]
#     def post(self, request):
#         national_code = request.data.get("national_code")
#         password = request.data.get("password")
#         role = request.data.get("role")

#         user = authenticate(request, username=national_code, password=password)
#         if not user:
#             return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

#         if user.role != role:
#             return Response({"error": "Role mismatch"}, status=status.HTTP_400_BAD_REQUEST)

#         return Response({"success": True, "message": f"{role} logged in successfully"})

# class RegisterView(APIView):
#     permission_classes = [AllowAny]
#     def post(self, request):
#         role = request.data.get("role")
#         if role == "PATIENT":
#             serializer = Patient_Register_Serializer(data=request.data)
#         elif role == "DOCTOR":
#             serializer = Doctor_Register_Serializer(data=request.data)
#         else:
#             return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "success": True,
#                 "data": serializer.data
#             }, status=status.HTTP_201_CREATED)
#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )