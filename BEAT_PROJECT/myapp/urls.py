from django.urls import path
from . import views

urlpatterns= [
    path('', views.home, name='home'),
    path('signup/', views.registration, name="reg"),
    path('login/', views.userLogin, name="login"),
    path('logout/', views.userLogout, name="logout"),
    path('trend1/', views.trend1, name="trend1"),
    
]
