from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import Patient, Contact
from django.db.models import Max

##def index(request):
##    return render(request, 'kontakti/index.html')

#def login(request):
def index(request):
    patients = Patient.objects.annotate(
        last_contact_date_time=Max('contact__created_at')
    ).order_by('last_contact_date_time')
    if request.method == 'POST':
        
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'kontakti/index.html', {'patients': patients})


def user_logout(request):
    logout(request)
    return redirect('index')
