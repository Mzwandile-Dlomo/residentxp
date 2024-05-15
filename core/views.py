from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required 


# Create your views here.
@login_required
def home_view(request):
    return render(request, 'core/home.html')

