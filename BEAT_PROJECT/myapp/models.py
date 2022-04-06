from django.db import models

# Create your models here.
class Customer(models.Model):
        customer_username = models.CharField(max_length=100, primary_key=True, null=False)
        customer_fullname = models.CharField(max_length=100, null=True)
        customer_email = models.CharField(max_length=100, null=True)
        customer_pass = models.CharField(max_length=100, null=True)
