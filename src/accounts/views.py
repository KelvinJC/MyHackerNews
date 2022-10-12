from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse

from accounts.forms import RegisterUserForm

# Create your views here.
def sign_up_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        try:
            if form.is_valid:
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                # user is automatically signed in after successful sign up
                login(request, user)
                messages.success(request, ("Sign up successful"))
                return redirect('home')
        except ValueError:
            return render(request, 'authenticate/sign_up.html', {'form': form})
    else:
        form = RegisterUserForm()
    return render(request, 'authenticate/sign_up.html', {'form': form})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, ("There was an error loggin in. Try again"))
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You were logged out."))
    return redirect('home')