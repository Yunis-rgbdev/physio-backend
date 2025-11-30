# tasks/serializer.py
from rest_framework import serializers
from .models import Tasks
from patients.models import Patient
from operators.models import Operator


class TaskSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    operator_name = serializers.CharField(source='operator.full_name', read_only=True)
    
    class Meta:
        model = Tasks
        fields = [
            'id',
            'patient',
            'patient_name',
            'operator',
            'operator_name',
            'last_update_at',
            'task_date',
            'title',
            'description',
            'status',
            'operator_note'
        ]
        read_only_fields = ['last_update_at']
    
    def validate_patient(self, value):
        """Ensure patient exists"""
        if not Patient.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Patient does not exist")
        return value
    
    def validate_operator(self, value):
        """Ensure operator exists if provided"""
        if value and not Operator.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Operator does not exist")
        return value


class TaskListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    operator_name = serializers.CharField(source='operator.full_name', read_only=True)
    
    class Meta:
        model = Tasks
        fields = [
            'id',
            'patient_name',
            'operator_name',
            'task_date',
            'title',
            'status',
            'last_update_at'
        ]


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating tasks"""
    
    class Meta:
        model = Tasks
        fields = [
            'patient',
            'operator',
            'task_date',
            'title',
            'description',
            'status',
            'operator_note'
        ]
    
    def validate_status(self, value):
        """Ensure status is valid"""
        valid_statuses = ['compelete', 'ongoing', 'ignored']
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            )
        return value