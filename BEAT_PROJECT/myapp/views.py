from xml.etree.ElementInclude import include
from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
import pandas as pd
import json
import matplotlib.pyplot as plt
import io
import urllib, base64
from plotly.offline import plot
import plotly.graph_objects as go
from .forms import form1, form2, form3, form4, form5
from datetime import datetime, timedelta

# Login imports
from .forms import LoginForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

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
    # cursor.execute(
    #     """SELECT * FROM CRICHARDSON5.BEAT_HEARTRATE"""
    # )
    # df6 = pd.DataFrame(cursor, columns=['username','time_stamp', 'deviceID', 'HRvalue'])
    # df6.drop(['username', 'deviceID'], axis=1, inplace=True)
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


# developing the trends
def trend_one(request):
    # getting the low, high, and avg for three days
    # need to be format YEAR-MM-DD
    day1 = '2021-02-11'
    # need to create time range
    day1_start = day1 + ' 00:00:00'
    day1_end = day1 + ' 23:59:59'
    day2 = "2021-02-12"
    day2_start = day2 + ' 00:00:00'
    day2_end = day2 + ' 23:59:59'
    day3 = "2021-02-13"
    day3_start = day3 + ' 00:00:00'
    day3_end = day3 + ' 23:59:59'

    query = """SELECT * FROM CRICHARDSON5.BEAT_HEARTRATE WHERE time_stamp > %s AND time_stamp < %s"""
    cursor.execute(query, (day1_start, day1_end, ))
    day1_df = pd.DataFrame(cursor, columns=['username','time_stamp', 'deviceID', 'HRvalue'])
    day1_df = day1_df.describe()
    day1_df.drop(['count', 'std', '25%', '50%', '75%'], inplace=True)
    print(day1_df)

    cursor.execute(query, (day2_start, day2_end, ))
    day2_df = pd.DataFrame(cursor, columns=['username','time_stamp', 'deviceID', 'HRvalue'])
    day2_df = day2_df.describe()
    day2_df.drop(['count', 'std', '25%', '50%', '75%'], inplace=True)
    print(day2_df)

    cursor.execute(query, (day3_start, day3_end, ))
    day3_df = pd.DataFrame(cursor, columns=['username','time_stamp', 'deviceID', 'HRvalue'])
    day3_df = day3_df.describe()
    day3_df.drop(['count', 'std', '25%', '50%', '75%'], inplace=True)
    print(type(day3_df))

    final_df = pd.concat([day1_df, day2_df, day3_df])

    # print(day1_df)
    # print(day2_df)
    # print(day3_df)
    # print("trend_one -- testing")


    # container for all the graphs
    graphs = []
    groups = ['mean','min','max']
    # add the bar graph
    graphs.append(
        go.Bar(
            x=groups,
            y=day1_df['HRvalue'],
            name=day1,
        )
    )
    graphs.append(
        go.Bar(
            x=groups,
            y=day2_df['HRvalue'],
            name=day2,
        )
    )
    graphs.append(
        go.Bar(
            x=groups,
            y=day3_df['HRvalue'],
            name=day3,
        )
    )
    layout = {
        'title': 'Aggregate Trends',
        'xaxis_title': 'Max, Min, Avg',
        'yaxis_title': 'Heart Rate',
        'height': 600,
        'width': 1000,
    }
    # Getting HTML needed to render the plot.
    plot_div = plot({'data': graphs, 'layout': layout}, 
                    output_type='div')

    return render(request, 'trend_one.html', context = {'plot_div': plot_div})

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

            # print("userid: ", userid)

            # Query
            activity = activity.lower()
            # print("Activity:", activity)
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
            # print(day_start_test)
            # print(day_end_test)



            real_query = """SELECT crichardson5.beat_event.cat, ROUND(AVG(CRICHARDSON5.beat_heartrate.HRVALUE)) AS AVG_HR, MIN(CRICHARDSON5.beat_heartrate.HRVALUE) as MIN_HR, MAX(CRICHARDSON5.beat_heartrate.HRVALUE) AS MAX_HR
                            FROM CRICHARDSON5.beat_event JOIN CRICHARDSON5.beat_heartrate
                            ON (
                                crichardson5.beat_event.USERID = crichardson5.beat_heartrate.USERID AND
                                crichardson5.beat_heartrate.TIME_STAMP BETWEEN crichardson5.beat_event.TSTART AND crichardson5.beat_event.TEND
                                )
                            WHERE crichardson5.beat_event.USERID = %s AND
                                crichardson5.beat_event.TSTART BETWEEN %s AND %s
                            GROUP BY crichardson5.beat_event.cat"""


            cursor.execute(real_query, (userid, day_start_test, day_end_test,))
            # cursor.execute(test_query_1,(test_userid, test_day_start, test_day_end,))
            day_df = pd.DataFrame(cursor, columns=['CAT','AVG_HR','MIN_HR', 'MAX_HR'])
            if not day_df.empty:
                # print(day_df)
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
                cursor.execute(real_query, (userid, day_start, day_end,))
                day_df = pd.DataFrame(cursor, columns=['CAT','AVG_HR','MIN_HR', 'MAX_HR'])
                if not day_df.empty:
                    all_days.append(date_time)
                    avg_days.append(day_df['AVG_HR'][0])
                    min_days.append(day_df['MIN_HR'][0])
                    max_days.append(day_df['MAX_HR'][0])

            # print(all_days)
            # print(avg_days)
            # print(min_days)
            # print(max_days)

            
            graphs = []
            groups = ['mean','min','max']
            # add the bar graph
            graphs.append(
                go.Scatter(
                    x=all_days,
                    y=avg_days,
                    name='Mean Heart Rate',
                )
            )
            graphs.append(
                go.Scatter(
                    x=all_days,
                    y=min_days,
                    name='Min Heart Rate',
                )
            )
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

            # getting the low, high, and avg for three days
            # need to be format YEAR-MM-DD
            day1 = '2021-02-11'
            # need to create time range
            day1_start = day1 + ' 00:00:00'
            day1_end = day1 + ' 23:59:59'
            day2 = "2021-02-12"
            day2_start = day2 + ' 00:00:00'
            day2_end = day2 + ' 23:59:59'
            day3 = "2021-02-13"
            day3_start = day3 + ' 00:00:00'
            day3_end = day3 + ' 23:59:59'

            query = """SELECT * FROM CRICHARDSON5.BEAT_HEARTRATE WHERE time_stamp > %s AND time_stamp < %s"""

  

            cursor.execute(query, (day1_start, day1_end, ))
            day1_df = pd.DataFrame(cursor, columns=['USERID','time_stamp','HRvalue'])
            day1_df = day1_df.describe()
            day1_df.drop(['count', 'std', '25%', '50%', '75%'], inplace=True)
            # print(day1_df)

            cursor.execute(query, (day2_start, day2_end, ))
            day2_df = pd.DataFrame(cursor, columns=['USERID','time_stamp','HRvalue'])
            day2_df = day2_df.describe()
            day2_df.drop(['count', 'std', '25%', '50%', '75%'], inplace=True)
            # print(day2_df)

            cursor.execute(query, (day3_start, day3_end, ))
            day3_df = pd.DataFrame(cursor, columns=['USERID','time_stamp','HRvalue'])
            day3_df = day3_df.describe()
            day3_df.drop(['count', 'std', '25%', '50%', '75%'], inplace=True)
            # print(type(day3_df))

            final_df = pd.concat([day1_df, day2_df, day3_df])
            # print(final_df)
            
            # container for all the graphs
            # graphs = []
            # groups = ['mean','min','max']
            # add the bar graph
            # graphs.append(
            #     go.Bar(
            #         x=groups,
            #         y=day1_df['HRvalue'],
            #         name=day1,
            #     )
            # )
            # graphs.append(
            #     go.Bar(
            #         x=groups,
            #         y=day2_df['HRvalue'],
            #         name=day2,
            #     )
            # )
            # graphs.append(
            #     go.Bar(
            #         x=groups,
            #         y=day3_df['HRvalue'],
            #         name=day3,
            #     )
            # )
            # layout = {
            #     'title': 'Aggregate Trends',
            #     'xaxis_title': 'Max, Min, Avg',
            #     'yaxis_title': 'Heart Rate',
            #     'height': 600,
            #     'width': 1000,
            # }
            # Getting HTML needed to render the plot.
            plot_div = plot({'data': graphs, 'layout': layout}, 
                            output_type='div')
            
            return render(request,'trend1.html',context = {'plot_div': plot_div, 'form':form})
    else:
        form = form1()
    return render(request, 'trend1.html', {'form': form})