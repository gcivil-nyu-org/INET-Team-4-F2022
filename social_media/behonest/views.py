from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login 
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("main:homepage")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="main/register.html", context={"register_form":form})
