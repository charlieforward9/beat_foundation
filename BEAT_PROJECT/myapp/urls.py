from django.urls import path
from . import views

urlpatterns= [
    path('', views.home, name='home'),
    path('signup/', views.registration, name="reg"),
    path('login/', views.userLogin, name="login"),
    path('logout/', views.userLogout, name="logout"),
    path('trends/', views.trends, name="trends"),
    path('customer_data', views.customer_data, name='customer_data'),
    path('calendar_data', views.calendar_data, name='calendar_data'),
    path('heartrate_data', views.heartrate_data, name='heartrate_data'),
    path('event_data', views.event_data, name='event_data'),
    path('charts_test', views.charts_test, name='charts_test'),
    path('about', views.about, name='about'),
    path('trend1/', views.trend1, name="trend1"),
    path('trend2/', views.trend2, name="trend2"),
    path('trend3/', views.trend3, name="trend3"),
    path('trend4/', views.trend4, name="trend4"),
    path('trend5/', views.trend5, name="trend5"),
]
