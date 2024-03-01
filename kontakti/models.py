from sys import modules
from unittest.util import _MAX_LENGTH
from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator, RegexValidator
from django.contrib.auth.models import User


class OU(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.description

class Patient(models.Model):
    ou = models.ForeignKey(OU, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    starost = models.CharField(blank=True, max_length=255)
    jmbg = models.CharField(
        max_length=13,
        blank=True,
        validators=[
            MaxLengthValidator(limit_value=13, message="JMBG must be 13 characters long"),
            MinLengthValidator(limit_value=13, message="JMBG must be 13 characters long"),
            #RegexValidator(r'^[0-9]{13}$', message="JMBG must be a number"),
            RegexValidator(r'^[0-9]+$', message="JMBG must be a number"),
        ]
    )
    gender = models.BooleanField()
    email = models.EmailField(max_length=254, blank=True)
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=20, blank=True)
    state = models.CharField(max_length=20, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    doctor = models.CharField(max_length=50)
    diagnose = models.CharField(max_length=100)
    anestezija = models.BooleanField()
    prijavljen = models.DateField()
    note = models.TextField(blank=True)
    active = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.first_name +' ' + self.last_name

class Contact(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    reserved_for = models.DateField()
    note = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.patient.first_name + ' ' + self.patient.last_name + ' ' + '\"' + self.note + '\"'
    
  
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ou = models.ForeignKey(OU, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username
