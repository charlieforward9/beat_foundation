# BEAT
**An attempt at optimizing the routine of life using the body's engine** 



## See Projects tab for upcoming developments

#### The Stack
* App foundation built using _Django_
* User Experience controlled with _React?_ and _Charts.JS_
* Database managed with _Oracle Developer_
* Application connected to Databases using _..._
* Input files provided by _Google Calendar_(Calendar) and _Apple Health_(Heart Rate) parsed with _Python Libraries (listed below)_
#### Collecting valid user input
* Calendar (.ics) parsed using [this tool](http://www.markwk.com/data-analysis-for-apple-health.html)
  * Only events preceded by a category keyword will be counted (not case sensitive): _Work_, _Rest_, _Fitness_, _Eating_, _Social_ or _Other_
* Heart Rate (.xml) parsed using [this library](https://icalendar.readthedocs.io/en/latest/)

### Instructions:
Virtual Environment Setup:
	$ pip install virtualenv
cd to project directory:
	$ cd proejct path
Create virtual env:
	$ virtualenv env
Activate venv:
	$ \path\to\env\Scripts\activate
	or
	$ .\\env\Scripts\activate
Check:
	$ pip -V (notice capital V)
If you are running the virtual env. it'll show the path to the env.'s location.

Django:
	$ pip install django
Bootstraps:
	$ pip install bootstrap-py
How to stop the server:
	Ctrl + c

url(port)/admin
Admin priviliges:
	$ python manage.py
	$ django-admin (to see the privileges)
	$ python manage.py createsuperuser
		usr: beats
		pswd: beats
		* not sure if this is local, we need to test it