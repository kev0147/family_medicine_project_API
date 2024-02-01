import io
from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import *

# Create your tests here.
def json_to_dict(response):
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        return data


class TestPatient(APITestCase):
    # Nous stockons l’url de l'endpoint dans un attribut de classe pour pouvoir l’utiliser plus facilement dans chacun de nos tests
    url = reverse_lazy('patients')

    # test: inscription
    def test_inscription_patient(self):
        patient = {
            'profile':{
                'name':'Gouabga', 
                'firstname':'Kouka', 
                'email':'lol@lol.lol', 
                'phone_number':70077558
            },
            'gender':'M', 
            'birth_date':'1986-02-03'
        }
        
        response = self.client.post('/patientInscription/inscription', patient, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(response.content)
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        print(data)
        self.assertEqual(Patient.objects.count(), 1)
        self.assertEqual(Patient.objects.get().profile.name, 'Gouabga')
        self.assertFalse(Patient.objects.get().validated)
        self.assertFalse(Patient.objects.get().doctor)

    def test_validation_patient(self):
        profile = Profile.objects.create(name='Gouabga', firstname='Kouka', email='lol@lol.lol', phone_number=70077558)
        patient = Patient.objects.create(profile=profile, gender='F', birth_date='1986-02-03')
        patient.save()
        patient_id = str(patient.id)
        self.assertFalse(patient.validated)

        patient_expected = {
            'profile':{
                'name':'Gouabga', 
                'firstname':'Kouka', 
                'email':'lol@lol.lol', 
                'phone_number':70077558
            },
            'gender':'M', 
            'birth_date':'1986-02-03',
            'validated':True,
            'doctor':None,
            'id': patient_id
        }

        url = f'/patients/{patient_id}/validation'
        response = self.client.put(url)
        print(response.status_code)

             