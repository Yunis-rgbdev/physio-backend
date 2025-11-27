from django.apps import AppConfig


class MedicalRecordConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'medical_record'

    def ready(self):
        import medical_record.signals  # Import signals when app is ready