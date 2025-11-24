from django.apps import AppConfig


class MedicalRecordsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'medical_records'

    def ready(self):
        # Import your signals here to register them
        import medical_records.signals