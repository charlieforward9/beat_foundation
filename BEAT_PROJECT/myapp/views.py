from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
import pandas as pd
import matplotlib.pyplot as plt
from plotly.offline import plot
import plotly.graph_objects as go
from .forms import form1, form2, form3, form4, form5
from datetime import timedelta

# Login imports
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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

# Trends 1-5 as individual functions below
@login_required
def trend1(request):
    if request.method == 'POST':
        form = form1(request.POST)
        if form.is_valid():
            activity = form.cleaned_data['activity'].lower()
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            avg = form.cleaned_data['avg']
            high = form.cleaned_data['high']
            low = form.cleaned_data['low']
            print("================ TREND 1 =================") #Display trend stats in terminal (no particular reason, just to show)
            print("User:", request.user.get_username())
            print("Activity:", activity)
            print("Start:", start) 
            print("End:", end) 
            print("Avg:", avg) 
            print("High:", high) 
            print("Low:", low) 
            print("========================================")
            if request.user.get_username() == 'Charbo': # set the username variable based on who is logged in
                userid = '0.8302870117189518'
            else: # Cam
                userid = '0.26777655249889387'

            
            # Query
            # Graph 
            date_time = start.strftime("%Y-%m-%d %H:%M:%S")
            date_time = date_time[0:10]
            all_days = []
            avg_days = []
            min_days = []
            max_days = []
            day_start = date_time + ' 00:00:00'
            day_end = date_time + ' 23:59:59'

            real_query = """SELECT ROUND(AVG(CRICHARDSON5.beat_heartrate.HRVALUE)) AS AVG_HR, MIN(CRICHARDSON5.beat_heartrate.HRVALUE) as MIN_HR, MAX(CRICHARDSON5.beat_heartrate.HRVALUE) AS MAX_HR
                            FROM CRICHARDSON5.beat_event JOIN CRICHARDSON5.beat_heartrate
                            ON (
                                crichardson5.beat_event.USERID = crichardson5.beat_heartrate.USERID AND
                                crichardson5.beat_heartrate.TIME_STAMP BETWEEN crichardson5.beat_event.TSTART AND crichardson5.beat_event.TEND
                                )
                            WHERE crichardson5.beat_event.USERID = %s AND
                                crichardson5.beat_event.TSTART BETWEEN %s AND %s AND
                                    crichardson5.beat_event.CAT = %s """

            cursor.execute(real_query, (userid, day_start, day_end, activity,))
            day_df = pd.DataFrame(cursor, columns=['AVG_HR','MIN_HR', 'MAX_HR'])
            if not day_df.empty: 
                if not day_df['AVG_HR'][0] == None:
                    all_days.append(date_time)
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
                cursor.execute(real_query, (userid, day_start, day_end, activity,))
                day_df = pd.DataFrame(cursor, columns=['AVG_HR','MIN_HR', 'MAX_HR'])
                if not day_df.empty:
                    if not day_df['AVG_HR'][0] == None:
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

            #Display graph and return
            plot_div = plot({'data': graphs, 'layout': layout}, output_type='div')
            return render(request,'trend1.html',context = {'plot_div': plot_div, 'form':form})
    else:
        form = form1()
    return render(request, 'trend1.html', {'form': form})


@login_required
def trend2(request):
    if request.method == 'POST':
        form = form2(request.POST)
        if form.is_valid():
            activity1 = form.cleaned_data['activity1'].lower()
            activity2 = form.cleaned_data['activity2'].lower()
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            avg = form.cleaned_data['avg']
            high = form.cleaned_data['high']
            low = form.cleaned_data['low']
            print("================ TREND 2 =================") #Display trend stats in terminal (no particular reason, just to show)
            print("User:", request.user.get_username())
            print("Activity 1:", activity1)
            print("Activity 2:", activity2)
            print("Start:", start) 
            print("End:", end) 
            print("Avg:", avg) 
            print("High:", high) 
            print("Low:", low) 
            print("========================================")
            
            if request.user.get_username() == 'Charbo': # set the username variable based on who is logged in
                userid = '0.8302870117189518'
            elif request.user.get_username() == 'Cam': # Cam
                userid = '0.26777655249889387'
            else:
                userid = '0.8302870117189518' #Charbo
            
            date_time = start.strftime("%Y-%m-%d %H:%M:%S")
            date_time = date_time[0:10]
            day_start = date_time + ' 00:00:00'
            day_end = date_time + ' 23:59:59'

            data = dict(uuid=userid, catone=activity1, cattwo=activity2, daystart=day_start, dayend=day_end)
            real_query = """SELECT ce.tstart STIME, round(avg(hr.hrvalue)) AVGHR, max(hr.hrvalue) MAXHR ,min(hr.hrvalue) MINHR
                            FROM (
                                SELECT ROW_NUMBER() OVER (ORDER BY tstart) i1, tstart, cat, userid, tend
                                FROM crichardson5.beat_event 
                                WHERE cat = :catone or cat = :cattwo ) ce
                                INNER JOIN 
                                (SELECT ROW_NUMBER() OVER (ORDER BY tstart) i2, tstart, cat, userid 
                                FROM crichardson5.beat_event 
                                WHERE cat=:catone or cat = :cattwo ) pe 
                                ON ce.i1 = pe.i2 + 1,
                                crichardson5.beat_heartrate hr
                            WHERE
                                ce.userid = pe.userid AND
                                ce.userid = hr.userid AND
                                ce.userid = :uuid AND
                                pe.cat = :catone AND 
                                ce.cat = :cattwo AND 
                                ce.tstart BETWEEN :daystart AND :dayend AND
                                hr.time_stamp BETWEEN ce.tstart AND ce.tend      
                            GROUP BY ce.tstart 
                            ORDER BY ce.tstart
                        """
 
            cursor.execute(real_query, data)


            day_df = pd.DataFrame(cursor, columns=['STIME', 'AVGHR', 'MAXHR', 'MINHR'])

            all_days = []
            avg_days = []
            min_days = []
            max_days = []
            
            if not day_df.empty: 
                if not day_df['AVGHR'][0] == None:
                    all_days.append(date_time)
                    avg_days.append(day_df['AVGHR'][0])
                    min_days.append(day_df['MINHR'][0])
                    max_days.append(day_df['MAXHR'][0])

            while start != end:
                if start > end:
                    break
                start = start + timedelta(days=1)
                date_time = start.strftime("%Y-%m-%d %H:%M:%S")
                date_time = date_time[0:10]
                day_start = date_time + ' 00:00:00'
                day_end = date_time + ' 23:59:59'
                cursor.execute(real_query, data)
                data = dict(uuid=userid, catone=activity1, cattwo=activity2, daystart=day_start, dayend=day_end)
                day_df = pd.DataFrame(cursor, columns=['STIME', 'AVGHR','MAXHR', 'MINHR'])
                print(day_df)
                if not day_df.empty:
                    if not day_df['AVGHR'][0] == None:
                        all_days.append(date_time)
                        avg_days.append(day_df['AVGHR'][0])
                        min_days.append(day_df['MINHR'][0])
                        max_days.append(day_df['MAXHR'][0])

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

            #Display graph and return
            plot_div = plot({'data': graphs, 'layout': layout}, output_type='div')
            return render(request,'trend2.html',context = {'plot_div': plot_div, 'form':form})
        else:
            print("Form is not valid")
    else:
        form = form2()
    return render(request, 'trend2.html', {'form': form})   

@login_required
def trend3(request):
    if request.method == 'POST':
        form = form3(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            print("================ TREND 3 =================")
            print("User:", request.user.get_username())
            print("Start:", start) 
            print("End:", end) 
            print("========================================")

            if not start > end:
                
                # set the username
                if request.user.get_username() == 'Charbo':
                    userid = '0.8302870117189518'
                else: # Cam
                    userid = '0.26777655249889387'
                # Graph 
                date_time = start.strftime("%Y-%m-%d %H:%M:%S")
                date_time = date_time[0:10]
                day_start_test = date_time + ' 00:00:00'
                date_time = end.strftime("%Y-%m-%d %H:%M:%S")
                date_time = date_time[0:10]
                day_end_test = date_time + ' 23:59:59'
                # print(day_start_test)
                # print(day_end_test)

                # Query
                query3 = """ SELECT TO_TIMESTAMP(TSTART, 'YYYY-MM-DD HH24:MI:SS') AS start_time, TO_TIMESTAMP(TEND, 'YYYY-MM-DD HH24:MI:SS') AS end_time, MAX(HRVALUE), TO_TIMESTAMP(MAX(TEND), 'YYYY-MM-DD HH24:MI:SS') - TO_TIMESTAMP(MIN(TSTART), 'YYYY-MM-DD HH24:MI:SS') AS Duration 
                        FROM crichardson5.beat_heartrate , crichardson5.beat_event
                        WHERE crichardson5.beat_event.USERID = crichardson5.beat_heartrate.USERID AND
                            crichardson5.beat_event.USERID = crichardson5.beat_event.USERID AND 
                            crichardson5.beat_event.USERID = %s AND
                            crichardson5.beat_event.CAT = 'fitness' AND
                            crichardson5.beat_event.TSTART BETWEEN %s AND %s AND
                            crichardson5.beat_heartrate.TIME_STAMP BETWEEN crichardson5.beat_event.TSTART AND crichardson5.beat_event.TEND
                        GROUP BY crichardson5.beat_event.tstart, crichardson5.beat_event.tend
                        ORDER BY crichardson5.beat_event.tstart ASC"""

                cursor.execute(query3, (userid,day_start_test, day_end_test, ))
                # cursor.execute(test_query_1,(test_userid, test_day_start, test_day_end,))
                day_df = pd.DataFrame(cursor, columns=['START_TIME','END_TIME', 'MAX_HR', 'DURATION'])
                # day_df = day_df.loc[day_df['CAT'] == activity]
                # if not day_df['AVG_HR'][0] == None:
                #     print(day_df)
                #     # print(day_df.loc[day_df['CAT'] == activity])
                #     # print(day_df['AVG_HR'][0])
                #     all_days.append(date_time)
                #     # test = day_df['AVG_HR']
                #     # print('testing: ', day_df['AVG_HR'][0])
                #     avg_days.append(day_df['AVG_HR'][0])
                #     min_days.append(day_df['MIN_HR'][0])
                #     max_days.append(day_df['MAX_HR'][0])
                
                # need to post-process for overlaps
                # for i, row in day_df.iterrows():
                #     if (len(day_df) == i):
                #         print("equal")
                #         break
                #     print("Length: ",len(day_df))
                #     print("Current Index: ",i)

                #     if day_df.iloc[i]['END_TIME'] > day_df.iloc[i+1]['START_TIME'] and day_df.iloc[i]['END_TIME'] < day_df.iloc[i+1]['END_TIME']:
                #         #combine the cells
                #         print("Merging")
                #         hr = max(day_df.iloc[i]['MAX_HR'], day_df.iloc[i+1]['MAX_HR'])
                #         dur = day_df.iloc[i+1]['END_TIME'] - day_df.iloc[i]['START_TIME']
                #         dict = {
                #             'START_TIME': day_df.iloc[i]['START_TIME'],
                #             'END_TIME': day_df.iloc[i+1]['END_TIME'],
                #             'MAX_HR': hr,
                #             'DURATION': dur,
                #         }
                #         df2 = pd.DataFrame(dict, index=[0])
                #         # print("new row: ", df2)
                #         # drop the old rows
                #         day_df.drop([0, 1], inplace=True)
                #         # add the new rows
                #         day_df = pd.concat([day_df, df2], ignore_index=True)
                #         # sort the df by the START_TIME
                #         day_df.sort_values(by=['START_TIME'], inplayce=True)
                day_df = day_df.groupby("DURATION").mean().reset_index()
                # print(day_df)

                total_durations = []
                for i, row in day_df.iterrows():
                    total_durations.append(str(row['DURATION'])[7:14])
                    # print(row['DURATION'])

                
                
                graphs = []
                # print(total_durations)
                total_HRs = day_df['MAX_HR']
        
                # Graph 
                graphs.append(
                    go.Scatter(
                        x = total_durations,
                        y = total_HRs,
                        # mode='markers',
                    )
                )
                layout = {
                    'title': 'Peak Heart Rate of Fitness Activities',
                    'xaxis_title': 'Duration (mins)',
                    'yaxis_title': 'Heart Rate',
                    'height': 600,
                    'width': 1000,
                }
                plot_div = plot({'data': graphs, 'layout': layout}, 
                                output_type='div')

                return render(request,'trend3.html',context = {'plot_div': plot_div, 'form':form})
    else:
        form = form3()
    return render(request, 'trend3.html', {'form': form})

@login_required
def trend4(request):
    if request.method == 'POST':
        form = form4(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
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
            
            if not start > end:
                # set the username
                if request.user.get_username() == 'Charbo':
                    userid = '0.8302870117189518'
                else: # Cam
                    userid = '0.26777655249889387'
                # Graph 
                date_time = start.strftime("%Y-%m-%d %H:%M:%S")
                date_time = date_time[0:10]
                print(date_time)
                all_days = []
                day_start_test = date_time + ' 00:00:00'
                date_time = end.strftime("%Y-%m-%d %H:%M:%S")
                date_time = date_time[0:10]
                day_end_test = date_time + ' 23:59:59'
                print(day_start_test)
                print(day_end_test)
                print(userid)
                # Query
                query4 = """SELECT TEND, ROUND(AVG(HRVALUE)) AS average, MIN(HRVALUE) AS min, MAX(HRVALUE) AS max, TO_TIMESTAMP(MAX(TEND), 'YYYY-MM-DD HH24:MI:SS') - TO_TIMESTAMP(MIN(TSTART), 'YYYY-MM-DD HH24:MI:SS') AS Duration
                            FROM (
                            SELECT *
                            FROM CRICHARDSON5.beat_event E, CRICHARDSON5.beat_heartrate H
                            WHERE E.TEND BETWEEN %s AND %s AND
                            E.CAT = 'rest' AND
                            E.USERID = H.USERID AND
                            E.USERID = %s AND
                            H.time_stamp BETWEEN E.TSTART AND E.TEND
                            )
                            GROUP BY TEND"""
                cursor.execute(query4, (day_start_test, day_end_test, userid,)) #, (userid, day_start_test, day_end_test)
                # cursor.execute(test_query_1,(test_userid, test_day_start, test_day_end,))
                day_df = pd.DataFrame(cursor, columns=['TEND','AVERAGE', 'MIN', 'MAX', 'DURATION'])
                print(day_df)
                day_df = day_df.sort_values(by=['TEND'])
                day_df = day_df.groupby("DURATION").mean().reset_index()
                for i, row in day_df.iterrows():
                    all_days.append(str(row['DURATION'])[7:14])
                print(all_days)
                avg_days = day_df['AVERAGE']
                min_days = day_df['MIN']
                max_days = day_df['MAX']
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
                    'title': 'HR During Sleep',
                    'xaxis_title': 'Sleep Duration (HH:MI:SS)',
                    'yaxis_title': 'Heart Rate',
                    'height': 600,
                    'width': 1000,
                }

                
                plot_div = plot({'data': graphs, 'layout': layout}, 
                                output_type='div')
            return render(request,'trend4.html',context = {'plot_div': plot_div, 'form':form})
    else:
        form = form4()
    return render(request, 'trend4.html', {'form': form})

@login_required
def trend5(request):
    if request.method == 'POST':
        form = form5(request.POST)
        if form.is_valid():
            start = (form.cleaned_data['start'])
            end = (form.cleaned_data['end'])
            print("================ TREND 5 =================")
            print("User:", request.user.get_username())
            print("Start:", start) 
            print("End:", end) 
            print("========================================")
            if not start > end:

                # set the username
                if request.user.get_username() == 'Charbo':
                    userid = '0.8302870117189518'
                else: # Cam
                    userid = '0.26777655249889387'

                # Graph 
                s_date_time = start.strftime("%Y-%m-%d %H:%M:%S")
                s_date_time = s_date_time[0:10]
                e_date_time = end.strftime("%Y-%m-%d %H:%M:%S")
                e_date_time = e_date_time[0:10]
                day_start = s_date_time + START_TIME
                day_end = e_date_time + END_TIME
                print(day_start,day_end)

                query ="""SELECT 
                            ROUND(100 - (((avghr_d-avghr_r)/avghr_r)*100)) as recovery_score,
                            DAY 
                            FROM
                                -- resting HR avg for all days in the given range
                                (SELECT 
                                        ROUND(AVG(hrvalue)) AS avghr_r, 
                                        crichardson5.beat_heartrate.userid AS id
                                    FROM crichardson5.beat_heartrate, crichardson5.beat_event
                                    WHERE
                                        crichardson5.beat_heartrate.userid = %s AND
                                        cat='rest' AND
                                        crichardson5.beat_heartrate.time_stamp BETWEEN %s AND %s
                                GROUP BY crichardson5.beat_heartrate.userid
                                ),
                                -- avg HR values per day in the given range
                                ( SELECT ROUND(AVG(hrvalue)) as avghr_d,USERID, DAY
                                    FROM( SELECT crichardson5.beat_heartrate.USERID USERID,crichardson5.beat_heartrate.HRVALUE HRVALUE,SUBSTR(TSTART, 1, 10) AS DAY
                                        FROM crichardson5.beat_heartrate, crichardson5.beat_event
                                        WHERE crichardson5.beat_event.tstart BETWEEN %s AND %s AND
                                                crichardson5.beat_heartrate.time_stamp BETWEEN crichardson5.beat_event.TSTART AND crichardson5.beat_event.TEND
                                                AND cat='rest' 
                                                AND crichardson5.beat_heartrate.userid = %s) new_dates
                                        GROUP BY USERID, DAY ORDER BY DAY ASC)
                        WHERE id = %s"""
                
                #cursor.execute(query, (userid, day_start, day_end, day_start, day_end, userid))
                cursor.execute(query, (userid, day_start, day_end, day_start, day_end, userid, userid,))
                print("sql done")
                df = pd.DataFrame(cursor, columns=['recovery_score', 'DAY'])
                # print(df)

                # Graph 
                graph =[]
                graph.append(
                    go.Scatter(
                        x=df['DAY'],
                        y=df['recovery_score'],
                        name='Recovery Score Progression'
                    )
                )
                layout = {
                    'title': 'Recovery Score Progression',
                    'xaxis_title': 'Time',
                    'yaxis_title': 'Recovery Score',
                    'height': 600,
                    'width': 1000,
                }
                plot_div = plot({'data': graph, 'layout': layout}, 
                                output_type='div')           
                return render(request,'trend5.html',{'plot_div': plot_div,'form':form})
    else:
        form = form5()
    return render(request, 'trend5.html', {'form': form})