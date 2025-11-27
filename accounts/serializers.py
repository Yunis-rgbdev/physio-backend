# accounts/serializers

from rest_framework import serializers
from django.db import transaction
from .models import User
from patients.models import Patient
from operators.models import Operator
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class RegisterSerializer(serializers.Serializer):
     # Fields for User
    full_name = serializers.CharField()
    national_code = serializers.CharField()
    password = serializers.CharField(write_only=True)
    role = serializers.IntegerField()

    # Operator-only fields
    specialty = serializers.CharField(required=False, allow_blank=True)
    student_code = serializers.IntegerField(required=False)
    nezam_pezeshki_code = serializers.IntegerField(required=False)
    clinic_address = serializers.CharField(required=False, allow_blank=True)
    

    # Patient-only fields
    birth_date = serializers.DateField(required=False)
    gender = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)

    @transaction.atomic
    def create(self, validated_data):
        password = validated_data.pop("password")
        role = validated_data.get("role")

        # Operator fields
        operator_fields = {
            key: validated_data.pop(key)
            for key in [
                "specialty",
                "student_code",
                "nezam_pezeshki_code",
                "clinic_address",
                "phone_number"
            ]
            if key in validated_data
        }
        operator_fields["national_code"] = validated_data.get("national_code")  # add user national_code

        # Patient fields
        patient_fields = {
            key: validated_data.pop(key)
            for key in ["birth_date", "gender", "phone_number", "full_name"]
            if key in validated_data
        }

        # Create user
        user = User.objects.create_user(password=password, **validated_data)

        # Create or update role-specific profile
        if role in [1, 3, 4]:
            Operator.objects.update_or_create(user=user, defaults=operator_fields)
        elif role == 2:
            Patient.objects.update_or_create(user=user, defaults=patient_fields)

        return user

class LoginSerializer(serializers.Serializer):
    national_code = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if not user:
            raise serializers.ValidationError("Invalid national code or password")
        if not user.is_active:
            raise serializers.ValidationError("User is inactive")
        data["user"] = user
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "national_code", "full_name", "role", "profile"]

    def get_profile(self, obj):
        if obj.is_patient:
            p = getattr(obj, "patient_profile", None)
            if not p:
                return None
            return {
                "id": str(p.id),
                "birth_date": p.birth_date,
                "gender": p.gender,
                "phone_number": p.phone_number,
            }
        elif obj.is_operator:
            o = getattr(obj, "operator_profile", None)
            if not o:
                return None
            return {
                "id": str(o.id),
                "specialty": o.specialty,
                "student_code": o.student_code,
                "nezam_pezeshki_code": o.nezam_pezeshki_code,
                "clinic_address": o.clinic_address,
                "phone_number": o.phone_number,
                "national_code": o.national_code,
            }

        return None