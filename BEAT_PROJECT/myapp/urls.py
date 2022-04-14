from django.urls import path
from . import views

urlpatterns= [
    path('', views.home, name='home'),
    path('signup/', views.registration, name="reg"),
    path('login/', views.userLogin, name="login"),
    path('logout/', views.userLogout, name="logout"),
    path('trend1/', views.trend1, name="trend1"),
    path('trend1/', views.trend1, name="trend1"),
    path('trend2/', views.trend2, name="trend2"),
    path('trend3/', views.trend3, name="trend3"),
    path('trend4/', views.trend4, name="trend4"),
    path('trend5/', views.trend5, name="trend5"),
]
