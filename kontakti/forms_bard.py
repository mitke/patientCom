#from django.core.validators import validate_unique
from django import forms
from .models import Patient, Contact
from django.contrib.auth.models import User
from django.forms.widgets import DateInput, TextInput, RadioSelect



class AddPatientForm01(forms.ModelForm):
    class Meta:
      model = Patient
      fields = ['first_name', 'last_name', 'date_of_birth', 'jmbg', 'gender', 'email', 'phone', 'address', 'city', 'state', 'zipcode', 'doctor', 'diagnose', 'anestezija']
      #fields = '__all__'
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
      '''
      initials = {
        'city': "Beograd",
        'state': "Srbija",
        'anestezija': True,
      }
      '''

class AddPatientForm(forms.ModelForm):
  class Meta:
    model = Patient
    fields = '__all__'  # Include all fields from the model

  date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['city'].initial = 'Belgrade'
    self.fields['state'].initial = 'Serbia'

    # Set placeholders for required fields (excluding ones specified)
    for field_name in self.fields:
        if field_name not in ('jmbg', 'email', 'zipcode'):
            self.fields[field_name].widget.attrs['placeholder'] = field_name.title()

    # Add labels for specific fields
    self.fields['first_name'].label = ''
    self.fields['date_of_birth'].label = 'Date of Birth'
    self.fields['gender'].label = 'Gender'
    self.fields['anestezija'].label = 'Anesthesia'

    # Convert gender field to radio buttons
    self.fields['gender'] = forms.ChoiceField(
        choices=((False, 'Female'), (True, 'Male')),
        widget=forms.RadioSelect(attrs={'class': 'form-check-inline'})
    )

    # Convert anestezija field to checkbox
    self.fields['anestezija'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})

    # Add validation for unique JMBG (if not already in your model)
    #self.clean_jmbg = forms.validate_unique(field_name='jmbg', message='JMBG must be unique')



