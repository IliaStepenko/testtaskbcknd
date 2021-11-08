from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from users.forms import RegistraionForm


def register_view(request):
    if request.method == 'POST':
        form = RegistraionForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = RegistraionForm()
    return render(request, 'registration/register.html', {'form': form})