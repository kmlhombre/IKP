from django.http import *
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.db import connection

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.hashers import make_password

from general_app.models import *


def index(request):
    return render(request, 'index.html')


def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/main/')

    return render(request, 'login.html')

@login_required(login_url='/general_app/login_user/')
def main(request):
    return HttpResponse("You are logged")

def check_password(request):
    passwd = make_password('admin')
    passwd2 = make_password('123')
    return HttpResponse(str('admin: = ' + passwd + '\n     123: = ' + passwd2))
