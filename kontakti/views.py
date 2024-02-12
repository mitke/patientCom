from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import Patient, Contact
from django.db.models import Max
from django.contrib import messages
from .forms import AddPatientForm, AddContactForm
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required

def index(request):
    patients = Patient.objects.annotate(
      last_contact_date_time=Max('contact__created_at')
    ).order_by('last_contact_date_time')[:40]
    
    if request.method == 'POST':
      form = AuthenticationForm(request, data=request.POST)
      
      if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('index')
      else:
        messages.success(request, "There Was An Error Logging In. Please Try Again...")
        return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'kontakti/index.html', {'patients': patients})


def user_logout(request):
  logout(request)
  return redirect('index')


def patient(request, patient_id):
  patient = Patient.objects.get(id=patient_id)
  contacts = Contact.objects.filter(patient=patient_id)
  return render(
    request, 'kontakti/patient.html', {
      'patient': patient, 
      'contacts': contacts
      }
    )


def add_patient(request):
  form = AddPatientForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      form.save()
      messages.success(request, 'Patient added Succesfully')
      return redirect('index')
  
  return render(request, 'kontakti/add-upd_pat.html', {'form': form})


def edit_patient(request, patient_id):
  edit_mode = True
  patient_to_edit = get_object_or_404(Patient, id=patient_id)
  form = AddPatientForm(request.POST or None, instance=patient_to_edit)
  first_name = patient_to_edit.first_name
  
  if form.is_valid():
    form.save()
    messages.success(request, "Podaci o pacijentu su uspešno promenjeni")
    return redirect('patient', patient_id)
  

  return render(request, 'kontakti/add-upd_pat.html', {'form': form, 'first_name': first_name, 'edit_mode': edit_mode}) 

  
"""
def add_contact(request, patient_id):
  patient = Patient.objects.get(pk=patient_id) 
  if request.method == 'POST':
    form = AddContactForm(request.POST)
    if form.is_valid:
      contact=form.save(commit=False)
      contact.patient = patient_id
      contact.user=request.user
      form = contact.save()
      messages.success(request, "Contact added Siccesfully!")
      return redirect('patient', patient_id)
  return render(request, 'kontakti/add_contact.html', {'form': form})
"""

@login_required
def add_contact(request, patient_id):
    pacijent = Patient.objects.get(pk=patient_id)

    if request.method == 'POST':
        form = AddContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.patient = pacijent  # Ensure association with the specified patient
            contact.user = request.user
            contact.save()
            return redirect('patient', patient_id)
    else:
      #form = AddContactForm(initial={'patient': patient})
      form = AddContactForm()  # Pre-populate patient field

    context = {'patient': pacijent, 'form': form}
    return render(request, 'kontakti/add_contact.html', context)
