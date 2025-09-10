from django.shortcuts import render,redirect
from rest_framework.decorators import api_view 
from .serializers import PatientSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Patient

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
            return redirect("patient_dashboard")
        except Patient.DoesNotExist:
            errror="invalid username or password"
    return render(request,"register_form.html",{"errror":errror})