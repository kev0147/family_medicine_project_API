from datetime import date
from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission, Group

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        #fields = ['username']
    
class ProfileUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ['user', 'name', 'firstname', 'email', 'phone_number']  

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = Doctor
        fields = ['profile','speciality','doctors_order_number', 'id', 'validated']  

class PatientSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    doctor = DoctorSerializer()
    class Meta:
        model = Patient
        fields = ['profile', 'id', 'birth_date', 'gender', 'validated', 'doctor']

class PatientInformationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [ 'id', 'birth_date', 'gender', 'validated']

class PatientValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = []

    def update(self, instance):
        user_data = {
            'username': str(instance.profile.phone_number),
            'password': make_password(str(instance.profile.phone_number)) # For demo purposes,I have to improve password handling
        }
        user = User.objects.create(**user_data)
        user.groups.add(Group.objects.get(name='patient'))
        user.user_permissions.add(Permission.objects.get(codename='patient_permission'))
        profile=instance.profile
        profile.user = user
        profile.save()
        print(f"{profile} updated successfully")

        prestation = Prestation.objects.get(id=1)
        service = Service(date=date.today(), patient=instance, prestation=prestation)
        service.save()

        instance.validated = True
        instance.save()

        return instance

class DoctorValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = []

    def update(self, instance):
        user_data = {
            'username': str(instance.profile.phone_number),
            'password': make_password(str(instance.profile.phone_number)) # For demo purposes,I have to improve password handling
        }
        
        user = User.objects.create(**user_data)
        user.groups.add(Group.objects.get(name='doctor'))
        user.user_permissions.add(Permission.objects.get(codename='doctor_permission'))
        profile=instance.profile
        profile.user = user
        profile.save()
        print(f"{profile} updated successfully")

        instance.validated = True
        instance.save()

        return instance

class PrestationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestation
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    prestation = PrestationSerializer()
    patient = PatientSerializer()
    report = ReportSerializer()
    class Meta:
        model = Service
        fields = ['prestation', 'patient', 'date', 'report']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'