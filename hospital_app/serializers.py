
from rest_framework import serializers
from .models import Patient,Appointment

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}  # password response me nahi dikhega
        }

class AppointmentSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source="doctor.name", read_only=True)
    patient_name = serializers.CharField(source="patient.name",read_only=True)
    # yaha par doctor ka name bhaj rhe hai serializer ki madad se
    class Meta:
        model = Appointment
        fields = ['id', 'time', 'date', 'status', 'doctor_name',"patient_name"]
        