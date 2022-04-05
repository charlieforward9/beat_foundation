from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.registration),
    path('login/', views.trends),
    path('trends/', views.trends),


    #path('home/', views.home, name="home"),
]