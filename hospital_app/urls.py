from django.urls import path
from .views import home
from . import views
urlpatterns = [
    path('',home, name="home"),
    path('registraion/',views.registration_detail,name="registration_detail"),
    path('api/register/',views.registration_store,name="register_api"),
    path('patient/login/',views.patient_login,name="patient_login"),
    path('patient/verify',views.patient_verify,name="patient_verify"),
]