import cx_Oracle
import matplotlib.pyplot as plt
from io import BytesIO
import urllib, base64
import seaborn as sb
import pandas as pd
from plotly.offline import plot
import plotly.graph_objects as go
from datetime import datetime, timedelta

#create connection

username = "cameronkeene"
pwd = "ThlJHhz544u1EOJbVodlpPDM"
dsn = "oracle.cise.ufl.edu:1521/orcl"
conn = cx_Oracle.connect(user=username, password=pwd, dsn=dsn)
print(conn.version)

cursor = conn.cursor()

activity = 'rest'
start = '2021-06-01 00:00:00'
end = '2021-06-03 23:59:59'
avg = True
high = True
low = True
# print("================ TREND 1 =================")
# print("User:", request.user.get_username())
# print("Activity:", activity)
# print("Start:", start) 
# print("End:", end) 
# print("Avg:", avg) 
# print("High:", high) 
# print("Low:", low) 
# print("========================================")
# set the username
userid = '0.8302870117189518'
# Query
activity = activity.lower()
# Graph 
# date_time = start.strftime("%Y-%m-%d %H:%M:%S")
date_time = start
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
                WHERE crichardson5.beat_event.USERID = '0.8302870117189518' AND
                    crichardson5.beat_event.TSTART BETWEEN '2021-06-01 00:00:00' AND '2021-06-01 23:59:59' AND
                        crichardson5.beat_event.CAT = 'rest' """

cursor.execute(real_query)
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


# while start != end:
#     if start > end:
#         break
#     start = start + timedelta(days=1)
#     date_time = start.strftime("%Y-%m-%d %H:%M:%S")
#     date_time = date_time[0:10]
#     day_start = date_time + ' 00:00:00'
#     day_end = date_time + ' 23:59:59'
#     # print(day_start)
#     # print(day_end)
#     cursor.execute(real_query, (userid, day_start, day_end, activity,))
#     day_df = pd.DataFrame(cursor, columns=['AVG_HR','MIN_HR', 'MAX_HR'])

#     if not day_df['AVG_HR'][0] == None:
#         # print(day_df)
#         # day_df = day_df.loc[day_df['CAT'] == activity]
#         all_days.append(date_time)
#         avg_days.append(day_df['AVG_HR'][0])
#         min_days.append(day_df['MIN_HR'][0])
#         max_days.append(day_df['MAX_HR'][0])


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

plot_div.show()