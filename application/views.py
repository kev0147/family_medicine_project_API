from django.utils import timezone
from django.db.models import Q
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from .models import *
from .permissions import *

class PatientInscriptionViewSet(ModelViewSet):

    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    
    @action(detail=False, methods=['post'])
    def inscription(self, request):
        profile_data = request.data.pop('profile')
        profile_serializer = ProfileSerializer(data=profile_data)
        if(profile_serializer.is_valid()):
            profile_instance = profile_serializer.save()
        else: 
            raise ValidationError(profile_serializer.errors)

        patient = Patient.objects.create(profile=profile_instance, validated=False, **request.data)
         
        return Response(status=status.HTTP_201_CREATED,data=PatientSerializer(patient).data)
    


class DoctorInscriptionViewSet(ModelViewSet):

    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    
    @action(detail=False, methods=['post'])
    def inscription(self, request):
        profile_data = request.data.pop('profile')
        profile_serializer = ProfileSerializer(data=profile_data)
        if(profile_serializer.is_valid()):
            profile_instance = profile_serializer.save()
        else: 
            raise ValidationError(profile_serializer.errors)

        doctor = Doctor.objects.create(profile=profile_instance, validated=False, **request.data)
         
        return Response(DoctorSerializer(doctor).data)


class PatientViewSet(ModelViewSet):

    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAdmin]

    
    @action(detail=False, methods=['get'])
    def non_validated_patients(self, request):
        non_validated_patients = Patient.objects.filter(validated=False)
        return Response(PatientSerializer(non_validated_patients, many=True).data)
    

    @action(detail=False, methods=['get'])
    def validated_patients(self, request):
        validated_patients = Patient.objects.filter(validated=True)
        return Response(PatientSerializer(validated_patients, many=True).data)


    @action(detail=True, methods=['put'])
    def validation(self, request, pk):
        try:
            patient = Patient.objects.get(id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if(patient.validated):
            return Response(status=status.HTTP_208_ALREADY_REPORTED)
        
        patient = validate_patient(patient=patient)
        
        return Response(PatientSerializer(patient).data)
    
    @action(detail=True, methods=['put'])
    def doctor_attribution(self, request, pk):
        patient = self.get_object()
        doctor_id = request.query_params['doctor_id']
        
        try:
            doctor = Doctor.objects.get(pk=doctor_id)
        except Doctor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        patient.doctor = doctor
        patient.save()

        return Response(PatientSerializer(patient).data)
    
    @action(detail=False, methods=['get'])
    def get_patient_from_token(self, request):
        user = request.user
        try:
            profile = Profile.objects.get(user=user)
            patient = Patient.objects.get(profile=profile)
            return Response(PatientSerializer(patient).data)
        except Patient.DoesNotExist:
            return None




class DoctorViewSet(ModelViewSet):

    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAdmin]


    @action(detail=False, methods=['get'])
    def non_validated_doctors(self, request):
        non_validated_doctors = Doctor.objects.filter(validated=False)
        return Response(DoctorSerializer(non_validated_doctors, many=True).data)
    
    @action(detail=False, methods=['get'])
    def validated_doctors(self, request):
        validated_doctors = Doctor.objects.filter(validated=True)
        return Response(DoctorSerializer(validated_doctors, many=True).data)

    @action(detail=True, methods=['put'])
    def validation(self, request, pk):
        doctor = self.get_object()
        doctor_serializer = DoctorValidationSerializer(doctor)
        try:
            doctor_serializer.update(doctor)
        except:
            return Response("numero de telephone deja utilise")
        return Response(DoctorSerializer(doctor).data)
    
    @action(detail=True, methods=['put'])
    def patient_attribution(self, request, pk):
        doctor = self.get_object()
        patient_id = request.query_params['patient_id']
        try:
            patient = Patient.objects.get(pk=patient_id)
        except Patient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        doctor.patients.add(patient)
        doctor.save()

        return Response(DoctorSerializer(doctor).data)
    

class ProfileViewSet(ModelViewSet):

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = []


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []


class PrestationViewSet(ModelViewSet):

    queryset = Prestation.objects.all()
    serializer_class = PrestationSerializer
    permission_classes = []


class PrestationViewSet(ModelViewSet):

    queryset = Prestation.objects.all()
    serializer_class = PrestationSerializer
    permission_classes = []


class ServiceViewSet(ModelViewSet):

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = []

class AppointmentViewSet(ModelViewSet):

    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]


class MessageViewSet(ModelViewSet):

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = []

    @action(detail=False, methods=['post'])
    def send_message(self, request):
        sender_id = request.query_params['sender_id']
        receiver_id = request.query_params['receiver_id']

        try:
            sender_profile = Profile.objects.get(pk=sender_id)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        try:
            receiver_profile = Profile.objects.get(pk=receiver_id)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        message = Message.objects.create(sender=sender_profile, receiver=receiver_profile, **request.data)
        return Response(MessageSerializer(message).data)


    @action(detail=False, methods=['get'])
    def get_messages(self, request):
        profile_id = request.query_params['profile_id']
        try:
            profile = Profile.objects.get(pk=profile_id)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        messages = Message.objects.filter(Q(sender=profile) | Q(receiver=profile)).order_by('date')
        return Response(MessageSerializer(messages, many=True).data)


def validate_patient(patient):
    
    user = User.objects.create(
        username = str(patient.profile.phone_number),
        password = make_password(str(patient.profile.phone_number))
    )
    
    user.groups.add(Group.objects.get(name='patient'))
    user.user_permissions.add(Permission.objects.get(codename='patient_permission'))

    profile=patient.profile
    profile.user = user
    profile.save()
    print(f" patient of profile:{profile} validated successfully")

    prestation = Prestation.objects.get(id=1)
    service = Service(date=date.today(), patient=patient, prestation=prestation)
    service.save()

    patient.validated = True
    patient.save()
    return patient
