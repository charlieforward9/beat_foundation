from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('myapp.urls')), # look up the patterns from the myapp/urls
    path('admin/', admin.site.urls),
]
