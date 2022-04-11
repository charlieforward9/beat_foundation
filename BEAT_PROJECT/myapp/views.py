from django.shortcuts import render, redirect
from django.db import models, connection, transaction
from myapp.models import Customer
from django.template import Context, loader
from django.http import HttpResponse
import pandas as pd
import json
import matplotlib.pyplot as plt
import io
import urllib, base64

# Login imports
from .forms import LoginForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .forms import form1, form2, form3, form4, form5

START_TIME = "00:00:00"
END_TIME = "23:59:59"

cursor = connection.cursor()

# Create your views here.
def customer_data(request):
    cursor.execute(
        """SELECT * FROM CRICHARDSON5.BEAT_CUSTOMER"""
    )
    df1 = pd.DataFrame(cursor, columns=['username', 'fullname', 'email', 'password'])
    # print(df)
    customer_list = df1.reset_index().to_json(orient ='records')
    customer_list_data = []
    customer_list_data =json.loads(customer_list)
    customer_context = {'d': customer_list_data}
    return render(request, 'customer_data.html', customer_context)


def calendar_data(request):
    cursor.execute(
        """SELECT * FROM CRICHARDSON5.BEAT_CALENDAR"""
    )
    df2 = pd.DataFrame(cursor, columns=['iCalID', 'start_date'])
    # print(df)
    calendar_list = df2.reset_index().to_json(orient ='records')
    calendar_list_data = []
    calendar_list_data =json.loads(calendar_list)
    calendar_context = {'d': calendar_list_data}
    return render(request, 'calendar_data.html', calendar_context)

def heartrate_data(request):
    cursor.execute(
        """SELECT * FROM CRICHARDSON5.BEAT_HEARTRATE"""
    )
    df3 = pd.DataFrame(cursor, columns=['username','time_stamp', 'deviceID', 'HRvalue'])
    # print(df)
    heartrate_list = df3.reset_index().to_json(orient ='records')
    heartrate_list_data = []
    heartrate_list_data =json.loads(heartrate_list)
    heartrate_context = {'d': heartrate_list_data}
    return render(request, 'heartrate_data.html', heartrate_context)

def event_data(request):
    cursor.execute(
        """SELECT * FROM CRICHARDSON5.BEAT_EVENT"""
    )
    df4 = pd.DataFrame(cursor, columns=['iCalID','event_date', 'start_time', 'end_time', 'cat'])
    # print(df)
    event_list = df4.reset_index().to_json(orient ='records')
    event_list_data = []
    event_list_data =json.loads(event_list)
    event_context = {'d': event_list_data}
    return render(request, 'event_data.html', event_context)


def about(request):
    cursor.execute(
        """ SELECT *
        FROM CRICHARDSON5.beat_heartrate
        WHERE username = 'Charbo' AND time_stamp < '2021-02-25 00:00:00' AND time_stamp > '2021-02-18 00:00:00' """
    )
    df5 = pd.DataFrame(cursor, columns=['username','time_stamp', 'deviceID', 'HRvalue'])
    df5 = df5[df5.username != 'cam']
    df5.drop(['username', 'deviceID'], axis=1, inplace=True)
    df5.plot(kind='line', x='time_stamp', y='HRvalue')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return render(request, 'about.html', {'data':uri})
    # return render(request, 'about.html')


def charts_test(request):
    cursor.execute(
        """SELECT * FROM CRICHARDSON5.BEAT_HEARTRATE"""
    )
    df6 = pd.DataFrame(cursor, columns=['username','time_stamp', 'deviceID', 'HRvalue'])
    df6.drop(['username', 'deviceID'], axis=1, inplace=True)
    # print(df5.head())
    return render(request, 'charts_test.html')

# imported functionallity
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

def getDay(input):
  temp = input.split(" ", 1)
  return temp[0]

@login_required
def trend1(request):
    if request.method == 'POST':
        form = form1(request.POST)
        if form.is_valid():
            activity = form.cleaned_data['activity']
            start = getDay(form.cleaned_data['start'])
            end = getDay(form.cleaned_data['end'])
            avg = form.cleaned_data['avg']
            high = form.cleaned_data['high']
            low = form.cleaned_data['low']
            print("================ TREND 1 =================")
            print("User:", request.user.get_username())
            print("Activity:", activity)
            print("Start:", start) 
            print("End:", end) 
            print("Avg:", avg) 
            print("High:", high) 
            print("Low:", low) 
            print("========================================")

            # Query
            
            # Graph 
            plt.plot(range(10))
            fig = plt.gcf()

            # Convert graph into dtring buffer and then we convert 64 bit code into image
            buf = io.BytesIO()
            fig.savefig(buf,format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            uri =  urllib.parse.quote(string)
            return render(request,'trend1.html',{'data1':uri, 'form':form})
    else:
        form = form1()
    return render(request, 'trend1.html', {'form': form})
    
@login_required
def trend2(request):
    if request.method == 'POST':
        form = form2(request.POST)
        if form.is_valid():
            activity1 = form.cleaned_data['activity1']
            activity2 = form.cleaned_data['activity2']
            start = getDay(form.cleaned_data['start'])
            end = getDay(form.cleaned_data['end'])
            avg = form.cleaned_data['avg']
            high = form.cleaned_data['high']
            low = form.cleaned_data['low']
            print("================ TREND 2 =================")
            print("User:", request.user.get_username())
            print("Activity1:", activity1)
            print("Activity2:", activity2)
            print("Start:", start) 
            print("End:", end) 
            print("Avg:", avg) 
            print("High:", high) 
            print("Low:", low) 
            print("========================================")

            # Query
            
            # Graph 
            plt.plot(range(20))
            fig = plt.gcf()

            # Convert graph into dtring buffer and then we convert 64 bit code into image
            buf = io.BytesIO()
            fig.savefig(buf,format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            uri =  urllib.parse.quote(string)
            return render(request,'trend2.html',{'data2':uri, 'form':form})
    else:
        form = form2()
    return render(request, 'trend2.html', {'form': form})

@login_required
def trend3(request):
    if request.method == 'POST':
        form = form3(request.POST)
        if form.is_valid():
            activity = form.cleaned_data['activity']
            start = getDay(form.cleaned_data['start'])
            end = getDay(form.cleaned_data['end'])
            avg = form.cleaned_data['avg']
            high = form.cleaned_data['high']
            low = form.cleaned_data['low']
            print("================ TREND 3 =================")
            print("User:", request.user.get_username())
            print("Activity:", activity)
            print("Start:", start) 
            print("End:", end) 
            print("Avg:", avg) 
            print("High:", high) 
            print("Low:", low) 
            print("========================================")

            # Query
            
            # Graph 
            plt.plot(range(30))
            fig = plt.gcf()
            #convert graph into dtring buffer and then we convert 64 bit code into image
            buf = io.BytesIO()
            fig.savefig(buf,format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            uri =  urllib.parse.quote(string)
            return render(request,'trend3.html',{'data3':uri, 'form':form})
    else:
        form = form3()
    return render(request, 'trend3.html', {'form': form})

@login_required
def trend4(request):
    if request.method == 'POST':
        form = form4(request.POST)
        if form.is_valid():
            start = getDay(form.cleaned_data['start'])
            end = getDay(form.cleaned_data['end'])
            avg = form.cleaned_data['avg']
            high = form.cleaned_data['high']
            low = form.cleaned_data['low']
            print("================ TREND 4 =================")
            print("User:", request.user.get_username())
            print("Start:", start) 
            print("End:", end) 
            print("Avg:", avg) 
            print("High:", high) 
            print("Low:", low) 
            print("========================================")

            # Query
            
            # Graph 
            plt.plot(range(40))
            fig = plt.gcf()
            #convert graph into dtring buffer and then we convert 64 bit code into image
            buf = io.BytesIO()
            fig.savefig(buf,format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            uri =  urllib.parse.quote(string)
            return render(request,'trend4.html',{'data4':uri, 'form':form})
    else:
        form = form4()
    return render(request, 'trend4.html', {'form': form})

@login_required
def trend5(request):
    if request.method == 'POST':
        form = form5(request.POST)
        if form.is_valid():
            start = getDay(form.cleaned_data['start'])
            end = getDay(form.cleaned_data['end'])
            print("================ TREND 5 =================")
            print("User:", request.user.get_username())
            print("Start:", start) 
            print("End:", end) 
            print("========================================")

            # Query
            
            # Graph 
            plt.plot(range(50))
            fig = plt.gcf()
            #convert graph into dtring buffer and then we convert 64 bit code into image
            buf = io.BytesIO()
            fig.savefig(buf,format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            uri =  urllib.parse.quote(string)
            return render(request,'trend5.html',{'data5':uri, 'form':form})
    else:
        form = form5()
    return render(request, 'trend5.html', {'form': form})
