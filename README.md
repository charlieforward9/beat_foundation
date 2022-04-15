# BEAT
**An attempt at optimizing the routine of life using the body's engine** 

## See Projects tab for upcoming developments

#### The Stack
* App foundation built using _Django_
* User Experience controlled with _Plotly_
* Database managed with _Oracle Developer_
* Application connected to Databases using _cx Oracle_ and _Oracle instant Client_
* Input files provided by _Google Calendar_(Calendar) and _Apple Health_(Heart Rate) parsed with Python Libraries: _dateutil_, _csvical_, _datetime_, _xml.etree_, _time_, _random_, _os_, _re_ and _sys_.
#### Collecting valid user input
* Calendar (.ics) parsed using [this tool](http://www.markwk.com/data-analysis-for-apple-health.html)
  * Only events preceded by a category keyword will be counted (case insensitive):
   * _Work_, _Rest_, _Fitness_, _Eating_, _Social_ or _Other_
* Heart Rate (.xml) 

Duplicate rows are automatically removed by the parser.

#### Repo Layout
* **BEAT_PROJECT** contains the applciation code, everything that makes the app run (still a local build)
* **BEATPARSER** is the current code required to parse the calendar and heart rate data. At this point it is all located in one file and mixed up with code coming from another tool meant to collect ALL Apple Health Data.
* **QUERIES.SQL** is the easiest way to see the queries that go into each trend. Integrated queries are in BEAT_PROJECT > myapp > views.py
* **server_connect** still figuring out what this is. I think its to connect to the SQL database, but that may be BEAT_PROJECT > manage.py . 


