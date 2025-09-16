from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)  
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=128)  
    age = models.IntegerField()  
    gender = models.CharField(max_length=10, choices=[('Male','Male'),('Female','Female'),('Other','Other')])

    def __str__(self):
        return self.name

class Doctor(models.Model):
    name=models.CharField(max_length=50)
    specialty=models.CharField(max_length=50)

    def __str__(self):
        return self.name
    



class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    time = models.TimeField()
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.name} -> {self.doctor.name} at {self.time}"
