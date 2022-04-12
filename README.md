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
  * Only events preceded by a category keyword will be counted (not case sensitive): _Work_, _Rest_, _Fitness_, _Eating_, _Social_ or _Other_
* Heart Rate (.xml) 

Duplicates are automatically removed by the parser.
