from importlib.metadata import requires
#from colorama import init
from django import forms
#from matplotlib import widgets
#from matplotlib.offsetbox import TextArea
from .models import Patient, Contact
from django.forms.widgets import DateInput, TextInput, CheckboxInput#, ChoiceWidget

class AddPatientForm(forms.ModelForm):
    
  class Meta:
    model = Patient
    fields = '__all__'

    requires = {
        'jmbg': 'False',
        'email': 'False',
        'address': 'False',
        'zipcode': 'False',
    }
    
    widgets = {
      'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ime'}),
      'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Prezime'}),
      'date_of_birth': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
      'jmbg': TextInput(attrs={'class': 'form-control', 'placeholder': 'JMBG'}),
      'gender': CheckboxInput(attrs={'class': 'form-check-input'}),
      'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
      'phone': TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefon'}),
      'address': TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresa'}),
      'city': TextInput(attrs={'class': 'form-control', 'placeholder': 'Grad'}),
      'state': TextInput(attrs={'class': 'form-control', 'placeholder': 'Država'}),
      'zipcode': TextInput(attrs={'class': 'form-control', 'placeholder': 'Poštanski broj'}),
      'doctor': TextInput(attrs={'class': 'form-control', 'placeholder': 'Doktor'}),
      'diagnose': TextInput(attrs={'class': 'form-control', 'placeholder': 'Dijagnoza'}),
      'anestezija': CheckboxInput(attrs={'class': 'form-check-input'}),
      'prijavljen': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    }
    
    labels = {
      'first_name': '',
      'last_name': '',
      'jmbg': '',
      'email': '',
      'phone': '',
      'address': '',
      'city': '',
      'state': '',
      'zipcode': '',
      'doctor': '',
      'diagnose': '',
      'date_of_birth': 'Datum rođenja',
      'gender': 'Muško',
      'anestezija': 'Opšta anestezija',
      'prijavljen': 'Datum prijavljivanja'
    }
  
  def save(self, commit=True):
    instance = super(AddPatientForm, self).save(commit=False)
    instance.first_name = self.cleaned_data['first_name'].title()
    instance.last_name = self.cleaned_data['last_name'].title()
    instance.doctor = self.cleaned_data['doctor'].title()
    instance.diagnose = self.cleaned_data['diagnose'].lower()
    if commit:
      instance.save()
    return instance

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.initial['jmbg'] = "0000000000000"
    #self.initial['gender'] = True
    self.initial['city'] = "Beograd"
    self.initial['state'] = "Srbija"
    self.initial['zipcode'] = '11000'
    #self.initial['anestezija'] = True

class AddContactForm(forms.ModelForm):
  class Meta:
    model = Contact
    fields = ['reserved_for', 'note']

    widgets = {
      'reserved_for': DateInput(attrs={'type': 'date'}),
      'note': forms.Textarea(attrs={'class': "form-control", 'placeholder': 'Zabeleška', 'cols': 200, 'rows': 4, 'style': 'width: 100%'})
    }
    labels = {
      'reserved_for': 'Zakazano za:',
      'note': ''
    }
