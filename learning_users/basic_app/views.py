# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from forms import UserForm, UserInfo
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def index(request):
    return render(request, 'basic_app/index.html')


@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required()
def special(request):
    return HttpResponse("You are logged in. Nice!")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('pa')
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Login failed")

            return HttpResponse("invalid details")
    else:
        return render(request, 'basic_app/login.html', {})

    return render(request, 'basic_app/login.html')

def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserInfo(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserInfo()
    return render(request, 'basic_app/registration.html', {
        'user_form': user_form,
        'profile_form':profile_form,
        'registered':registered
    })

