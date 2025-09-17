from django.urls import path
from .views import home
from . import views
urlpatterns = [
    path('',home, name="home"),
    path('registraion/',views.registration_detail,name="registration_detail"),
    path('api/register/',views.registration_store,name="register_api"),
    path('patient/login/',views.patient_login,name="patient_login"),
    path('patient/verify',views.patient_verify,name="patient_verify"),
    path('book/appointment/', views.book_appointment, name="book_appointment"),
    path('appointment/success',views.appointment_success,name="appointment_success"),
    path('status/verify',views.status_verify,name="status_verify") ,
    path('status/check',views.status_check,name="status_check"),
    path('status/page',views.status_page,name="status_page")
]
