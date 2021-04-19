from abc import ABC
from django.shortcuts import render
from .forms import UserForm, UserProfileInfoForm

# for login - import
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request):
    return render(request, "basic_auth/index.html")


@login_required
def special(request):
    return HttpResponse("You are logged in, Nice !")


@login_required
def logoutUser(request):
   logout(request)
   return HttpResponseRedirect(reverse('basic_auth:index'))

def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)  # avoid overlaps
            profile.user = user  # One to One relationship

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    user_form = UserForm()
    profile_form = UserProfileInfoForm()

    return render(request, "basic_auth/registration.html", {
        "user_form": user_form,
        "profile_form": profile_form,
        "registered": registered
    })


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
       
        if user:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('basic_auth:index'))
            else:
                return HttpResponse("Your account is not activate .")
        else:
            print("someone tried to login and failed")
            print(f"Username : {username}, and password {password}")
            return HttpResponse("Invalid Login Details !")

    return render(request, "basic_auth/login.html")
