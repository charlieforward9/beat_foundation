from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import matplotlib.pyplot as plt
import numpy as np
import io
import urllib, base64

from .forms import LoginForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm 


def home(request):
    return render(request, "home.html")

def signup(request):
    return render(request, "signup.html")

def registration(request): 
    form = SignUpForm(request.POST) 
    if form.is_valid(): 
        form.save() 
        _username = form.POST.get('username') 
        _password = form.POST.get('password') 
        user = authenticate(username=_username, password=_password) 
        login(request, user) 
        return redirect('trends') 
    context = { 
        'form': form 
    } 
    return render(request, 'signup.html', context) 
 
def userLogin(request):
    if request.method == "POST":
        _username=request.POST.get("username")
        _password=request.POST.get("password")
        user = authenticate(username=_username, password=_password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("home")
            else:
                return HttpResponse('Disabled account')
        else:
            return render(request, 'login.html')            
    return render(request, 'login.html',)

@login_required
def userLogout(request):
    logout(request)
    return redirect("home")

@login_required
def trends(request):

    # Fisrt graph
    plt.plot(range(10))
    fig = plt.gcf()
    #convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)

    # data = {'C':20, 'C++':15, 'Java':30,
    #         'Python':35}
    # courses = list(data.keys())
    # values = list(data.values())
    
    # fig2 = plt.figure(figsize = (5, 5))

    
    # # Second graph
    # plt.bar(courses, values, color ='maroon',
    #         width = 0.4)
    
    # plt.xlabel("Courses offered")
    # plt.ylabel("No. of students enrolled")
    # plt.title("Students enrolled in different courses")

    # plt.plot(range(20))
    # fig2 = plt.gcf()
    # buf2 = io.BytesIO()
    # fig2.savefig(buf2,format='png')
    # buf2.seek(0)
    # string2 = base64.b64encode(buf2.read())
    # uri2 =  urllib.parse.quote(string2)

    # Third graph

    # Fourth graph

    # Fifth graph

    # return render(request,'trends.html',{'data1':uri, 'data2':uri2})
    return render(request,'trends.html',{'data1':uri})

