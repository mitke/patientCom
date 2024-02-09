from django import forms
from .models import Patient, Contact

class AddPatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'

class AddContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ['created_at']
