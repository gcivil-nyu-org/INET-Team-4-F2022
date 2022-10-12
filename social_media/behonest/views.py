from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def register(request):
    template = loader.get_template('behonest/register.html')
    return render(request, 'behonest/register.html')
    

