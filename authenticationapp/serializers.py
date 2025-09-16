# authenticationapp/serializers.py
from rest_framework import serializers
from patients.models import Patient
from doctors.models import Doctor
from .models import Auth

class Patient_Register_Serializer(serializers.ModelSerializer):
    national_code = serializers.IntegerField(source="auth.national_code")
    name = serializers.CharField(source="auth.name")
    password = serializers.CharField(write_only=True, source="auth.password")

    class Meta:
        model = Patient
        fields = ["national_code", "name", "age", "gender", "phone_number", "password"]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        auth_data = validated_data.pop("auth")
        password = auth_data.pop("password")

        # create Auth user first
        user = Auth.objects.create(
            national_code=auth_data["national_code"],
            name=auth_data["name"],
            role="PATIENT",
        )
        user.set_password(password)
        user.save()

        # link Patient to Auth - the name and role will be set automatically via save() method
        patient = Patient.objects.create(auth=user, **validated_data)
        return patient

class Doctor_Register_Serializer(serializers.ModelSerializer):
    national_code = serializers.IntegerField(source="auth.national_code")
    name = serializers.CharField(source="auth.name")
    password = serializers.CharField(write_only=True, source="auth.password")

    class Meta:
        model = Doctor
        fields = ["national_code", "name", "phone_number", "specialty", "clinic_address", "password"]
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        auth_data = validated_data.pop("auth")
        password = auth_data.pop("password")

        # create Auth user first
        user = Auth.objects.create(
            national_code=auth_data["national_code"],
            name=auth_data["name"],
            role="DOCTOR",
        )
        user.set_password(password)
        user.save()

        # link Doctor to Auth - the name and role will be set automatically via save() method
        doctor = Doctor.objects.create(auth=user, **validated_data)
        return doctor
