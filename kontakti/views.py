from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import Patient, Contact
from django.db.models import Max
from django.contrib import messages
from .forms import AddPatientForm, AddContactForm
from django.utils import timezone
from datetime import date, datetime
from django.contrib.auth.decorators import login_required

def index(request):
    patients = Patient.objects.annotate(
      last_contact_date_time=Max('contact__created_at')
    ).order_by('last_contact_date_time')[:40]

    for patient in patients:
      dob = patient.date_of_birth
      today = datetime.now().date()
      age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
      frac_year = (today-dob.replace(year=today.year)).days / 365.25
      age_with_dec = age + frac_year
      patient.age = age_with_dec
    
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


@login_required
def patient(request, patient_id):
  patient = Patient.objects.get(id=patient_id)
  contacts = Contact.objects.filter(patient=patient_id).order_by('-created_at')
  dob = patient.date_of_birth
  today = datetime.now().date()
  age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
  frac_years = (today - dob.replace(year=today.year)).days / 365.25
  age_with_dec = age + frac_years
  patient.age = age_with_dec # type: ignore
  return render(
    request, 'kontakti/patient.html', {
      'patient': patient, 
      'contacts': contacts,
      #'age_with_dec': age_with_dec,
      }
    )


@login_required
def add_patient(request):
  form = AddPatientForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      form.save()
      messages.success(request, 'Patient added Succesfully')
      return redirect('index')
  
  return render(request, 'kontakti/add-upd_pat.html', {'form': form})


@login_required
def edit_patient(request, patient_id):
  edit_mode = True
  patient_to_edit = get_object_or_404(Patient, id=patient_id)
  form = AddPatientForm(request.POST or None, instance=patient_to_edit)
  first_name = patient_to_edit.first_name
  
  if form.is_valid():
    form.save()
    messages.success(request, "Podaci o pacijentu su uspešno promenjeni")
    return redirect('patient', patient_id)
  

  return render(
    request, 
    'kontakti/add-upd_pat.html',
    {'form': form, 'first_name': first_name, 'edit_mode': edit_mode}
  ) 

  
@login_required
def delete_patient(request, patient_id):
  patient = get_object_or_404(Patient, pk=patient_id)
  patient.delete()
  messages.success(request, "Pacijent i svi kontakti sa njim su izrisani iz baze")
  return redirect('index')



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
        messages.success(request, "Uspešno dodat kontakt!")
        return redirect('patient', patient_id)
    else:
      form = AddContactForm()

    context = {'patient': pacijent, 'form': form}
    return render(request, 'kontakti/add_contact.html', context)
