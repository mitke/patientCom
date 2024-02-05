from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator, RegexValidator
from django.contrib.auth.models import User

class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    jmbg = models.CharField(
        max_length=13,
        validators=[
            MaxLengthValidator(limit_value=13, message="JMBG must be 13 characters long"),
            MinLengthValidator(limit_value=13, message="JMBG must be 13 characters long"),
            #RegexValidator(r'^[0-9]{13}$', message="JMBG must be a number"),
            RegexValidator(r'^[0-9]+$', message="JMBG must be a number"),
        ]
    )
    gender = models.BooleanField()
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=18 )
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=10)
    doctor = models.CharField(max_length=50)
    diagnose = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name +' ' + self.last_name

class Contact(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    reserved_for = models.DateField()
    note = models.TextField()

    def __str__(self) -> str:
        return self.patient.first_name + ' ' + self.patient.last_name + ' ' + '\"' + self.note + '\"'
