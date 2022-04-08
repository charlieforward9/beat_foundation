import cx_Oracle
import matplotlib.pyplot as plt
from io import BytesIO
import urllib, base64
import seaborn as sb
import pandas as pd

#create connection
conn = cx_Oracle.connect('CISEServer/cameronkeene@//oracle.cise.ufl.edu:1521/orcl')
print(conn.version)


cursor = conn.cursor()

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
print(final_df)

plot = sb.barplot(data = final_df)
plt.show()
# # fig = plot.get_figure()
# # fig.savefig(plot_file, format = 'png')
# plot_file = BytesIO()
# plot.figure.savefig(plot_file, format='png')
# encoded_file = base64.b64encode(plot_file.getValue())