from django import forms
from .models import Patient, Contact
from django.forms.widgets import DateInput, TextInput, RadioSelect


class AddPatientForm(forms.ModelForm):
    class Meta:
      model = Patient
      #fields = ['first_name', 'last_name', 'date_of_birth', 'jmbg', 'gender', 'email', 'phone', 'address', 'city', 'state', 'zipcode', 'doctor', 'diagnose', 'anestezija']
      fields = '__all__'
      widgets = {
        'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
        'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
        'date_of_birth': DateInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        'jmbg': TextInput(attrs={'class': 'form-control', 'placeholder': 'JMBG'}),
        'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), 
        'phone': TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
        'address': TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
        'city': TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
        'state': TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
        'zipcode': TextInput(attrs={'class': 'form-control', 'placeholder': 'Zipcode'}),
        'doctor': TextInput(attrs={'class': 'form-control', 'placeholder': 'Doctor'}),
        'diagnose': TextInput(attrs={'class': 'form-control', 'placeholder': 'Diagnose'}),
      }
      labels = {
        'date_of_birth': "datum rođenja",
        'gender': "Pol",
        'anestezija': 'Opšta anestezija'
      }
      initials = {
        'city': "Beograd",
        'state': "Srbija",
        'anestezija': True,
      }


