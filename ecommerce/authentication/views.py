from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from .forms import UserLoginForm, UserSignupForm


def signup(request):
    template_name = "authentication/signup.html"
    if request.method == 'POST':
        register_form = UserSignupForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            return redirect(reverse('login_view'))
    else:
        register_form = UserSignupForm()

    context = {'form': register_form}
    return render(request, template_name, context)


def login_view(request):
    template_name = "authentication/login.html"
    if request.method == 'POST':
        register_form = UserLoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
    else:
        register_form = UserLoginForm()
    context = {'form': register_form}
    return render(request, template_name, context)


def logout_view(request):
    logout(request)
    return redirect('/')