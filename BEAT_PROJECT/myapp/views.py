from xml.etree.ElementInclude import include
from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
import pandas as pd
import json
import matplotlib.pyplot as plt
from plotly.offline import plot
import plotly.graph_objects as go
from .forms import form1, form2, form3, form4, form5
from datetime import datetime, timedelta

# Login imports
from .forms import LoginForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .forms import form1, form2, form3, form4, form5

START_TIME = "00:00:00"
END_TIME = "23:59:59"

cursor = connection.cursor()

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

# developing the trends
@login_required
def trend1(request):
    if request.method == 'POST':
        form = form1(request.POST)
        if form.is_valid():
            activity = form.cleaned_data['activity']
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
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
            # set the username
            if request.user.get_username() == 'Charbo':
                userid = '0.8302870117189518'
            else: # Cam
                userid = '0.26777655249889387'

            # Query
            activity = activity.lower()
            # Graph 
            date_time = start.strftime("%Y-%m-%d %H:%M:%S")
            date_time = date_time[0:10]
            print(date_time)
            all_days = []
            avg_days = []
            min_days = []
            max_days = []
            day_start_test = date_time + ' 00:00:00'
            day_end_test = date_time + ' 23:59:59'

            real_query = """SELECT ROUND(AVG(CRICHARDSON5.beat_heartrate.HRVALUE)) AS AVG_HR, MIN(CRICHARDSON5.beat_heartrate.HRVALUE) as MIN_HR, MAX(CRICHARDSON5.beat_heartrate.HRVALUE) AS MAX_HR
                            FROM CRICHARDSON5.beat_event JOIN CRICHARDSON5.beat_heartrate
                            ON (
                                crichardson5.beat_event.USERID = crichardson5.beat_heartrate.USERID AND
                                crichardson5.beat_heartrate.TIME_STAMP BETWEEN crichardson5.beat_event.TSTART AND crichardson5.beat_event.TEND
                                )
                            WHERE crichardson5.beat_event.USERID = %s AND
                                crichardson5.beat_event.TSTART BETWEEN %s AND %s AND
                                    crichardson5.beat_event.CAT = %s """

            cursor.execute(real_query, (userid, day_start_test, day_end_test, activity,))
            # cursor.execute(test_query_1,(test_userid, test_day_start, test_day_end,))
            day_df = pd.DataFrame(cursor, columns=['AVG_HR','MIN_HR', 'MAX_HR'])
            # day_df = day_df.loc[day_df['CAT'] == activity]
            print(day_df)
            if not day_df['AVG_HR'][0] == None:
                print(day_df)
                # print(day_df.loc[day_df['CAT'] == activity])
                # print(day_df['AVG_HR'][0])
                all_days.append(date_time)
                # test = day_df['AVG_HR']
                # print('testing: ', day_df['AVG_HR'][0])
                avg_days.append(day_df['AVG_HR'][0])
                min_days.append(day_df['MIN_HR'][0])
                max_days.append(day_df['MAX_HR'][0])


            while start != end:
                if start > end:
                    break
                start = start + timedelta(days=1)
                date_time = start.strftime("%Y-%m-%d %H:%M:%S")
                date_time = date_time[0:10]
                day_start = date_time + ' 00:00:00'
                day_end = date_time + ' 23:59:59'
                # print(day_start)
                # print(day_end)
                cursor.execute(real_query, (userid, day_start, day_end, activity,))
                day_df = pd.DataFrame(cursor, columns=['AVG_HR','MIN_HR', 'MAX_HR'])

                if not day_df['AVG_HR'][0] == None:
                    # print(day_df)
                    # day_df = day_df.loc[day_df['CAT'] == activity]
                    all_days.append(date_time)
                    avg_days.append(day_df['AVG_HR'][0])
                    min_days.append(day_df['MIN_HR'][0])
                    max_days.append(day_df['MAX_HR'][0])

            
            graphs = []
            # add the bar graph
            if avg:
                graphs.append(
                    go.Scatter(
                        x=all_days,
                        y=avg_days,
                        name='Mean Heart Rate',
                    )
                )
            if low:
                graphs.append(
                    go.Scatter(
                        x=all_days,
                        y=min_days,
                        name='Min Heart Rate',
                    )
                )
            if high:
                graphs.append(
                    go.Scatter(
                        x=all_days,
                        y=max_days,
                        name='Max Heart Rate',
                    )
                )
            layout = {
                'title': 'Aggregate Trends',
                'xaxis_title': 'Max, Min, Avg',
                'yaxis_title': 'Heart Rate',
                'height': 600,
                'width': 1000,
            }

            
            plot_div = plot({'data': graphs, 'layout': layout}, 
                            output_type='div')
            
            return render(request,'trend1.html',context = {'plot_div': plot_div, 'form':form})
    else:
        form = form1()
    return render(request, 'trend1.html', {'form': form})


@login_required
def trend2(request):
    if request.method == 'POST':
        form = form2(request.POST)
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
