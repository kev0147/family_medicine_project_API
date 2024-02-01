from django.urls import path, include
from rest_framework.routers import SimpleRouter

from application import views

# Create a router and register our ViewSets with it.
router = SimpleRouter(trailing_slash=False)
router.register(r'patientInscription', views.PatientInscriptionViewSet, basename='patient_inscription')
router.register(r'doctorInscription', views.DoctorInscriptionViewSet, basename='doctor_inscription')
router.register(r'patients', views.PatientViewSet, basename='patient')
router.register(r'doctors', views.DoctorViewSet, basename='doctor')
router.register(r'profiles', views.ProfileViewSet, basename='profile')
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'services', views.ServiceViewSet, basename='service')
router.register(r'prestations', views.PrestationViewSet, basename='prestation')
router.register(r'messages', views.MessageViewSet, basename='message')

# The API URLs are now determined automatically by the router.
urlpatterns = router.urls