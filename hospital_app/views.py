from django.shortcuts import render,redirect,get_object_or_404
from rest_framework.decorators import api_view 
from .serializers import PatientSerializer,AppointmentSerializer
from .models import Patient,Doctor,Appointment,Admin
from django.utils import timezone
from .decorators import admin_required,doctor_required
from rest_framework.response import Response
from rest_framework import status 
from rest_framework import viewsets
from .models import Patient
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework import status as drf_status


# Create your views here.
def home(request):
    return render(request, "home.html")

def registration_detail(request):
    return render(request,"register_form.html")


@api_view(['POST'])
def registration_store(request):
    serializer = PatientSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Registration successful!"}, status=201)
    return Response(serializer.errors, status=400)

def register_done(request):
    return render(request, "registration_done.html")





def patient_login(request):
    return render(request,"patient_login.html")


@csrf_exempt
def patient_verify_api(request):
    if request.method == "POST":
        import json
        try:
            data = json.loads(request.body.decode('utf-8'))  
            phone = data.get("phone")
            password = data.get("password")
            patient = Patient.objects.get(phone=phone, password=password)
            request.session['patient_id'] = patient.id
            return JsonResponse({"success": True, "message": "Login successful!"})
        except Patient.DoesNotExist:
            return JsonResponse({"success": False, "message": "Invalid username or password."})
        except Exception as e:
            print("Error:", e)
            return JsonResponse({"success": False, "message": "Internal server error."})
    return JsonResponse({"success": False, "message": "Only POST allowed."})

def book_appointment_render(request):
    return render(request,"book_appointment.html")

@api_view(['POST','GET'])
def book_appointment(request):
   if request.method=='GET':
       doctors = Doctor.objects.all().values('id','name','specialty')
       return Response({"doctors":list(doctors)},status=status.HTTP_200_OK)
   
   if request.method=='POST':
       patient_id=request.session.get("patient_id")
       if not patient_id :
           return Response({"success":False,"message":"invalid user"},status=status.HTTP_400_BAD_REQUEST)
       try:
           patient = Patient.objects.get(id=patient_id)
       except Patient.DoesNotExist:
           return Response({"success":False,"message":"invalid patient"},status=status.HTTP_404_NOT_FOUND)
       
       doctor_id =request.data.get("doctor")
       appointment_time=request.data.get("time")
       date =request.data.get("date") 

       try:
           doctor=Doctor.objects.get(id=doctor_id)
       except Doctor.DoesNotExist:
           return Response({"success":False,"message":"invalid doctor id"},status=status.HTTP_400_BAD_REQUEST)
       
    #    appointment creation here 
       Appointment.objects.create(
           patient=patient,
           doctor=doctor,
           time=appointment_time,
           date=date

        )
       return Response({"success":True,"message":"appointment booked successfull!"},status=status.HTTP_201_CREATED)




def  appointment_success(request):
    return render(request,"appointment_sucess.html")



def status_verify(request):
    return render(request,"status_verify.html")


@api_view(['POST'])
def status_check(request):
    try:
        # request.data automatically parses JSON
        phone = request.data.get("phone")
        password = request.data.get("password")

        patient = Patient.objects.get(phone=phone, password=password)
        request.session['patient_id'] = patient.id

        return Response({"success": True, "patient_id": patient.id}, status=status.HTTP_200_OK)

    except Patient.DoesNotExist:
        return Response({"success": False, "error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Error:", e)
        return Response({"success": False, "error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
def status_page(request):
    if "patient_id" not in request.session:
        return Response({"error":"patient unauthorized "},status=status.HTTP_401_UNAUTHORIZED)

    patient_id = request.session["patient_id"]
    appointments = Appointment.objects.filter(patient_id=patient_id).order_by("-id")
    serializers =AppointmentSerializer(appointments,many=True)
    return Response(serializers.data,status=status.HTTP_200_OK)



def status_dashboard(request):
    return render(request,"status_page.html")



def admin_login(request):
    return render(request,"admin_login.html")

@api_view(['POST'])
def admin_verify(request):
    
        phone=request.data.get("phone")
        password=request.data.get("password")

        try:
            admin=Admin.objects.get(phone=phone,password=password)
            request.session['admin_id']=admin.id
            return Response({"success":True,"admin_id":admin.id},status=status.HTTP_200_OK)
        except Admin.DoesNotExist:
            return Response({"success":False,"error":"admin invalid "},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("error",e)
            return Response({"success":False,"error":"internal error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
            


# def admin_dashboard(request):
#     appointments = Appointment.objects.all().order_by('-id')
#     return render(request, "admin_dashboard.html", {"appointments": appointments})

@api_view(['GET'])
def admin_dashboard (request):
    if 'admin_id' not in request.session:
        return Response({"error" : "unauthorized admin"},status=status.HTTP_401_UNAUTHORIZED)
    
    appointments = Appointment.objects.all().order_by('-id')
    serializers=AppointmentSerializer(appointments,many=True)
    return Response(serializers.data,status=status.HTTP_200_OK)



@admin_required
def admin_home(request):
    return render(request, "admin_home.html")




def admin_logout(request):
    request.session.flush()   # puri session clear
    return redirect("admin_login")


@api_view(['POST'])
def update_status(request, appointment_id, status):
    appt = get_object_or_404(Appointment, id=appointment_id)
    appt.status = status
    appt.save()
    serializers=AppointmentSerializer(appt)
    return Response({
        "success": True,
        "message": f"Appointment status updated to {status}",
        "appointment": serializers.data
    }, status=drf_status.HTTP_200_OK)


def adminpage_show (request):
    return render(request,"admin_dashboard.html")


@admin_required 
def doctor_add_page(request):
    doctors=Doctor.objects.all().order_by('-id')
    return render(request,"doctor_add_page.html",{"doctors":doctors})

@admin_required 
def delete_doctor(request,doctor_id):
     doc=get_object_or_404(Doctor,id=doctor_id)
     doc.delete()
     return redirect('doctor_add_page')


@admin_required 
def manage_doctors(request):
    
    if request.method == 'POST':
        name = request.POST.get("name")
        specialty = request.POST.get("specialty")
        phone=request.POST.get("phone")
        password=request.POST.get("password")

        # Doctor object create karke save 
        Doctor.objects.create(
            name=name,
            specialty=specialty,
            phone=phone,
            password=password
        )
        return redirect('doctor_add_page') 
    doctors= Doctor.objects.all()
    return render(request,"doctor_add_page.html",{"doctors":doctors})
    

def admin_home_page(request):
    return render("admin_home.html")

def patient_adminpage(request):
    return render(request,"patient_add_page.html")


@api_view(['GET','POST'])
def manage_patient_api(request):
  if  request.method=='GET':
      patients=Patient.objects.all()
      serializer=PatientSerializer(patients,many=True)
      return Response(serializer.data)
  elif request.method=='POST':
      serializer=PatientSerializer(data=request.data)
      if serializer.is_valid():
          serializer.save()
          return Response(serializer.data,status=status.HTTP_201_CREATED)
      return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
     

@api_view(['DELETE'])
def delete_patient_api(request,pk):
    patient=get_object_or_404(Patient,id=pk)
    patient.delete()
    return Response({"message":"patient delete successfully"},status=status.HTTP_204_NO_CONTENT)



def doctor_login(request):
    return render (request,"doctor_login.html")




def doctor_verify(request):
    if request.method == 'POST':
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        try:
            doctor = Doctor.objects.get(phone=phone, password=password)
            request.session['doctor_id'] = doctor.id
            return redirect("doctor_home")  
        except Doctor.DoesNotExist:
            error = "Invalid phone or password"
            return render(request, "doctor_login.html", {"error": error})

    return render(request, "doctor_login.html")


@doctor_required
def doctor_home(request):
    doctor_id=request.session.get('doctor_id')
    doctor=get_object_or_404(Doctor,id=doctor_id)
    appointments=Appointment.objects.filter(doctor=doctor).order_by('-date','-time')
    return render(request,"doctor_home.html",{"doctor":doctor,"appointments":appointments})

def update_status_doctor(request, appointment_id, status):
    appt = get_object_or_404(Appointment, id=appointment_id)
    appt.status = status
    appt.save()
    return redirect('doctor_home')

def doctor_logout(request):
    request.session.flush()
    return redirect('doctor_login')


def patient_guide(request):
    return render(request,"patient_guide.html")
