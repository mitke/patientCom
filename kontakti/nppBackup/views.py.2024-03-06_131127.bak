from unittest import mock
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from .models import Patient, Contact, OU, UserProfile
from django.db.models import Max, Min, Q
from django.contrib import messages
from .forms import AddPatientForm, AddContactForm
from django.utils import timezone
from datetime import date, datetime
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
  """
  Index view function for the application. Requires the user to be logged in. If the user is authenticated, it retrieves the user profile and a list of patients associated with the user's organization unit. It then calculates the age of each patient and retrieves reservation information. Finally, it renders the 'kontakti/index.html' template with the list of patients. If the user is not authenticated, it redirects to the login page.
  """
  if request.user.is_authenticated:
    user_profile = request.user.userprofile
    patients = Patient.objects.filter(ou=user_profile.ou, active=True)
    '''patients = patients.annotate(
      last_contact_date_time=Max('contact__created_at')
    ).order_by('last_contact_date_time')#[:40]'''
    patients = patients.annotate(
      last_rezervisana_operacija=Min('contact__reserved_for')
    ).order_by('last_rezervisana_operacija')

    for patient in patients:
      patient.age = calculate_age(patient.date_of_birth)
      try:
        patient.rez = Contact.objects.filter(patient=patient).first().reserved_for
      except AttributeError:
        patient.rez = None
      

    return render(request, 'kontakti/index.html', {'patients': patients})
  else:
    return redirect('login')  # Redirect to login page if user is not authenticated
  

@login_required
def reserved(request):
  """
  This function requires the user to be logged in. It retrieves the user's organizational unit (ou), then retrieves a list of reserved contacts for patients in that ou, ordered by reservation date. It then calculates the age of each patient and returns a context containing the patients for rendering the 'reserved.html' template.
  """
  user_ou = request.user.userprofile.ou
  latest_contacts = {}
  patients = Contact.objects.filter(patient__ou=user_ou, reserved_for__gt=date.today()).order_by('reserved_for')
  for contact in patients:
    patient_id = contact.patient.id
    if patient_id not in latest_contacts or contact.reserved_for > latest_contacts[patient_id].reserved_for:
      latest_contacts[patient_id] = contact
  
  for contact in latest_contacts.values():
    dob = contact.patient.date_of_birth
    contact.patient.age = calculate_age(dob)
  
  context = {'patients': latest_contacts.values()}
  return render (request, 'kontakti/reserved.html', context)


def user_login(request):
  if request.method == 'POST':
    form = AuthenticationForm(request, data=request.POST)
    
    if form.is_valid():
      user = form.get_user()
      login(request, user)
      return redirect('index')
    else:
      messages.success(request, "Postoji greška pri logovanju. Pokušajte ponovo...")
  else:
      form = AuthenticationForm()
  return render(request, 'kontakti/login.html', {'form': form})


def user_logout(request):
  logout(request)
  return redirect('index')


@login_required
def patient(request, patient_id):
  patient = Patient.objects.get(id=patient_id)
  contacts = Contact.objects.filter(patient=patient_id).order_by('-created_at')
  patient.age = calculate_age(patient.date_of_birth) 
  return render(
    request, 'kontakti/patient.html', {
      'patient': patient, 
      'contacts': contacts,
      }
    )


@login_required
def add_patient(request):
  
  if request.method == 'POST':
    form = AddPatientForm(request.POST)
    if form.is_valid():
      patient = form.save(commit=False)
      patient.ou = request.user.userprofile.ou
      patient.save()
      messages.success(request, 'Pacijent je uspešno dodat')
      return redirect('index')
  else:
    form = AddPatientForm()
  
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
  patient.active = False
  patient.save()
  messages.success(request, "Pacijent i svi kontakti sa njim su izbrisani iz baze")
  return redirect('index')


def search_patient(request):
  """
  Search for patients based on the search term provided in the request.
  
  Parameters:
  - request: The request object containing the search term in the POST data.
  
  Returns:
  - Renders the 'kontakti/index.html' template with the filtered patients.
  """
  if request.method == 'POST':
    search_term = request.POST.get('search_term')
    patients = Patient.objects.filter(Q(active=True) & (Q(first_name__icontains=search_term) | Q(last_name__icontains=search_term)))
    for patient in patients:
      patient.age = calculate_age(patient.date_of_birth)
      try:
        patient.rez = Contact.objects.filter(patient=patient).first().reserved_for
      except AttributeError:
        patient.rez = None 
  return render(request, 'kontakti/index.html', {'patients': patients})


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

    
def calculate_age(dob):
  """
  Calculate the age based on the provided date of birth.

  Parameters:
  dob (datetime): The date of birth in datetime format.

<<<<<<< HEAD
  Returns:
  tuple: A tuple containing the calculated age in years and months.
  """
  today = datetime.now().date()
  try:
    """years = today.year - dob.year
=======
    Returns:
    tuple: A tuple containing the age in years and months (e.g. (years, months)),
           or (None, None) if there was an error.
    """
    '''today = datetime.now().date()
    try:
      years = today.year - dob.year
>>>>>>> 8d5210e009ffcf5d21f13e91de703dc9e3d7d35a
      months = today.month - dob.month
      if today.day < dob.day:
          months -= 1
      while months < 0:
          years -= 1
<<<<<<< HEAD
          months += 12"""
=======
          months += 12
      return years, months
    except (AttributeError, TypeError):
      return None, None'''
    
def calculate_age(dob):
  today = datetime.now().date()
  try:
>>>>>>> 8d5210e009ffcf5d21f13e91de703dc9e3d7d35a
    yearsFrac = (today-dob).days / 365.25
    year = int(yearsFrac)
    months = round((yearsFrac - year) * 12)
    return (year, months)
  except (AttributeError, TypeError):
    return None



  