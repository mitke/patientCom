from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout

##def index(request):
##    return render(request, 'kontakti/index.html')

#def login(request):
def index(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'kontakti/index.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('index')