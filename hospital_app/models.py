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
