from django.shortcuts import render,redirect
from rest_framework.decorators import api_view 
from .serializers import PatientSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Patient,Doctor,Appointment

# Create your views here.
def home(request):
    return render(request, "home.html")

def registration_detail(request):
    return render(request,"register_form.html")


@api_view(['POST'])
def registration_store(request):
    serializer=PatientSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return render(request,"registration_done.html")
    return redirect('register_api')



def patient_login(request):
    return render(request,"patient_login.html")


# ye without rest hai for easy
def patient_verify(request):
    errror=None
    if request.method=="POST":
        phone=request.POST.get("phone")
        password=request.POST.get("password")
        try:
            patient=Patient.objects.get(phone=phone,password=password)
            request.session['patient_id'] = patient.id
            return redirect("book_appointment")
        except Patient.DoesNotExist:
            errror="invalid username or password"
    return render(request,"register_form.html",{"errror":errror})



def book_appointment(request):
    doctors = Doctor.objects.all()
    
    # Patient fetch from session
    patient_id = request.session.get("patient_id")
    patient = None
    if patient_id:
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            patient = None
    
    if request.method == "POST":
        doctor_id = request.POST.get("doctor")
        appointment_time = request.POST.get("time")
        doctor = Doctor.objects.get(id=doctor_id)

        if patient:  # only save if patient is logged in
            Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                time=appointment_time
            )
            return redirect('appointment_success')
        else:
            message = "Patient not logged in!"

        return render(request, "book_appointment.html", {"doctors": doctors, "message": message})

    return render(request, "book_appointment.html", {"doctors": doctors})



def  appointment_success(request):
    return render(request,"appointment_sucess.html")

def status_verify(request):
    return render(request,"status_verify.html")

def status_check(request):
    if request.method=="POST":
        phone=request.POST.get("phone")
        password=request.POST.get("password")

        try:
            patient=Patient.objects.get(phone=phone,password=password)
            request.session['patient_id']=patient.id
            return redirect('status_page')
        except Patient.DoesNotExist:
            error="ivalid user name or paassword"
    return redirect('home')




def status_page(request):
    return render(request,"status_page.html")