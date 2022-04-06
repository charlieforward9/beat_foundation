from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.registration, name="reg"),
    path('login/', views.userLogin, name="login"),
    path('logout/', views.userLogout, name="logout"),
    path('trends/', views.trends, name="trends"),


    #path('home/', views.home, name="home"),
]