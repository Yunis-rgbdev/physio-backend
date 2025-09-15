# mongo_client.py
from pymongo import MongoClient
from django.conf import settings
from datetime import datetime
from datetime import timezone

class MongoDBConnection:
    _instance = None

    def __new__(cls): 
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)

            # Custom MongoDB config from Django settings
            mongo_config = settings.DATABASES.get('mongodb', {})

            # Strict validation: raise errors if critical values are missing
            mongo_uri = mongo_config.get('mongo_uri')
            mongo_db_name = mongo_config.get('mongo_db_name')

            if not mongo_uri: 
                raise ValueError("Missing 'mongo_uri' in DATABASES['mongodb'] settings.")

            if not mongo_db_name:
                raise ValueError("Missing 'mongo_db_name' in DATABASES['mongodb'] settings.")

            # Connect to MongoDB
            cls._instance.client = MongoClient(mongo_uri)
            cls._instance.db = cls._instance.client[mongo_db_name]

        return cls._instance
    
class PatientCollection:
    def __init__(self):
        connection = MongoDBConnection()
        self.collection = connection.db['patients']
        
    def get_all_patients(self):
        patients_result = list(self.collection.find({}, {'_id': 0,}))
        return patients_result
    
    def get_patient_by_id(self, code):
        patient_result = self.collection.find_one({'national_code': code}, {'_id': 0,})
        return patient_result
    
    def update_one_patient(self, _code, _new_status):
        update = self.collection.find_one_and_update(
            {"national_code": _code},
            {"$set": {"status": _new_status, "updated_at": datetime.now(timezone.utc)}}
        )
        return update
    
class DoctorCollection:
    def __init__(self):
        connection = MongoDBConnection()
        self.collection = connection.db['Doctor']

    def get_all_doctors(self):
        doctor_results = list(self.collection.find({}, {'_id': 0,}))
        return doctor_results
    
    def get_doctor_by_id(self, code):
        doctor_results = self.collection.find_one({'national_code': code}, {'id': 0,})
        return doctor_results
    
    def update_one_doctor(self, code, new_status):
        update = self.collection.find_one_and_update(
            {'national_code': code},
            {"$set": {"status": new_status, "updated_at": datetime.now(timezone.utc)}}
        )
        return update
    
