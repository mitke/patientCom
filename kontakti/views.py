from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import Patient, Contact
from django.db.models import Max
from django.contrib import messages
from .forms import AddPatientForm, AddContactForm
from django.utils import timezone
from datetime import datetime

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


def add_patient(request):
  form = AddPatientForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      form.save()
      messages.success(request, 'Patient added Succesfully')
      return redirect('index')
  
  return render(request, 'kontakti/add-upd_pat.html', {'form': form})

def add_contact(request):
  form = AddContactForm(request)
  if request.method == 'POST':
    if form.is_valid:
      form.save()
      messages.success(request, "Contact added Siccesfully!")
      return redirect('index')
  return render(request, 'kontakti/add_contact', {'form': form})

