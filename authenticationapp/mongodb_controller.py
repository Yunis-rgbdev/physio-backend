from pymongo import MongoClient
from django.conf import settings

class MongoDBController:
    _instance = None

    def __new__(cls):
        if cls._insatance is None:
            cls._instanc = super(MongoDBController, cls).__new__(cls)

            mongo_config = settings.DATABASES.get('mongodb', {})

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
        connection = MongoDBController()
        self.collection = connection.db['Patients']
        
    def get_all_patients(self):
        patients_result = list(self.collection.find({}, {'_id': 0,}))
        return patients_result
    
    def get_patient_by_code(self, code):
        patient_result = self.collection.find_one({'national_code': code}, {'_id': 0,})
        return patient_result
    
    def add_patient(self, patient_data):
        add_result = self.collection.insert_one(patient_data)
        return add_result

class DoctorCollection:
    def __init__(self):
        connection = MongoDBController()
        self.connection = connection.db['Doctors']

    def get_doctor_by_code(self, code):
        doctor_result = self.connection.find_one({"national_code": code, "_id": 0,})
        return doctor_result
    
    def add_doctor(self, doctor_data):
        add_result = self.connection.insert_one(doctor_data)
        return add_result
