from django.shortcuts import render,redirect,get_object_or_404
from rest_framework.decorators import api_view 
from .serializers import PatientSerializer
from .models import Patient,Doctor,Appointment,Admin
from django.utils import timezone
from django.contrib import messages




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
        date=request.POST.get("date")
        doctor = Doctor.objects.get(id=doctor_id)

        if patient:  # only save if patient is logged in
            Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                time=appointment_time,
                date=date if date else timezone.now().date()
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
            return redirect("status_page")
        except Patient.DoesNotExist:
            error="ivalid user name or paassword"
    return redirect('home')

def status_page(request):
    if "patient_id" not in request.session:
        return redirect("patient_login")  

    patient_id = request.session["patient_id"]
    appointments = Appointment.objects.filter(patient_id=patient_id).order_by("-id")

    return render(request, "status_page.html", {"appointments": appointments})



def admin_login(request):
    return render(request,"admin_login.html")


def admin_verify(request):
    error=None
    if request.method=='POST':
        phone=request.POST.get("phone")
        password=request.POST.get("password")

        try:
            admin=Admin.objects.get(phone=phone,password=password)
            request.session['admin_id']=admin.id
            return redirect("admin_home")
        except Admin.DoesNotExist:
            error="invlid phone and password"
    return render(request,"admin_login.html",{"error":error})


def admin_dashboard(request):
   
    if 'admin_id' not in request.session:
        return redirect('admin_login')

    appointments = Appointment.objects.all().order_by('-id')
    return render(request, "admin_dashboard.html", {"appointments": appointments})



def admin_home(request):
    if 'admin_id' not in request.session:
        return redirect('admin_login')
    return render(request, "admin_home.html")




def admin_logout(request):
    request.session.flush()   # puri session clear
    return redirect("admin_login")



def update_status(request, appointment_id, status):
    appt = get_object_or_404(Appointment, id=appointment_id)
    appt.status = status
    appt.save()
    return redirect('admin_dashboard')


def doctor_add_page(request):
    if 'admin_id' not in request.session:
         return redirect('admin_login')
    doctors=Doctor.objects.all().order_by('-id')
    return render(request,"doctor_add_page.html",{"doctors":doctors})


def delete_doctor(request,doctor_id):
     if 'admin_id' not in request.session:
         return redirect('admin_login')
     doc=get_object_or_404(Doctor,id=doctor_id)
     doc.delete()
     return redirect('doctor_add_page')

def manage_doctors(request):
    if 'admin_id' not in request.session:
        return redirect('admin_login')
    
    if request.method == 'POST':
        name = request.POST.get("name")
        specialty = request.POST.get("specialty")

        # Doctor object create karke save karna
        Doctor.objects.create(
            name=name,
            specialty=specialty
        )
        return redirect('doctor_add_page') 
    doctors= Doctor.objects.all()
    return render(request,"doctor_add_page.html",{"doctors":doctors})
    
