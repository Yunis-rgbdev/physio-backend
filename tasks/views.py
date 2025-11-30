# tasks/views.py
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Tasks
from .serializer import (
    TaskSerializer,
    TaskListSerializer,
    TaskCreateUpdateSerializer
)


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing tasks.
    
    Provides CRUD operations and additional filtering capabilities.
    """
    queryset = Tasks.objects.all().select_related('patient', 'operator')
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'patient', 'operator', 'task_date']
    search_fields = ['title', 'description', 'patient__full_name']
    ordering_fields = ['task_date', 'last_update_at', 'status']
    ordering = ['-task_date']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return TaskListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return TaskCreateUpdateSerializer
        return TaskSerializer
    
    def get_queryset(self):
        """
        Optionally filter tasks by query parameters
        """
        queryset = super().get_queryset()
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            queryset = queryset.filter(task_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(task_date__lte=end_date)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def ongoing(self, request):
        """Get all ongoing tasks"""
        tasks = self.get_queryset().filter(status='ongoing')
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def completed(self, request):
        """Get all completed tasks"""
        tasks = self.get_queryset().filter(status='compelete')
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def ignored(self, request):
        """Get all ignored tasks"""
        tasks = self.get_queryset().filter(status='ignored')
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def complete(self, request, pk=None):
        """Mark a task as completed"""
        task = self.get_object()
        task.status = 'compelete'
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def ignore(self, request, pk=None):
        """Mark a task as ignored"""
        task = self.get_object()
        task.status = 'ignored'
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_patient(self, request):
        """Get all tasks for a specific patient"""
        patient_id = request.query_params.get('patient_id', None)
        
        if not patient_id:
            return Response(
                {'error': 'patient_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        tasks = self.get_queryset().filter(patient_id=patient_id)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_operator(self, request):
        """Get all tasks for a specific operator"""
        operator_id = request.query_params.get('operator_id', None)
        
        if not operator_id:
            return Response(
                {'error': 'operator_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        tasks = self.get_queryset().filter(operator_id=operator_id)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get all tasks scheduled for today"""
        today = timezone.now().date()
        tasks = self.get_queryset().filter(task_date=today)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get all overdue tasks (past date and not completed)"""
        today = timezone.now().date()
        tasks = self.get_queryset().filter(
            task_date__lt=today,
            status='ongoing'
        )
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)