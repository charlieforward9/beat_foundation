from django import forms
from django.forms import ModelForm
from .widget import DatePickerInput
from django.forms.widgets import EmailInput, PasswordInput
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class dateForm(forms.Form):
    my_date_field = forms.DateField(widget=DatePickerInput)

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

# class User(models.Model):
#     username = models.CharField(max_length=100)
#     def _str__(self):
#         return self.username


# class RegistrationForn(ModelForm):
#     username = forms.CharField(max_length=100)
#     password = forms.CharField(widget=PasswordInput)
#     email = forms.CharField(widget=EmailInput)
#     HRdata = forms.FileField()
#     CalendarData = forms.FileField()
#     class Meta:
#         model = User
#         fields = ["username", "password", "email", "HRdata", "CalendarData"]




# class RegisterForm(UserCreationForm):
#     # HRdata = forms.FileField()
#     # CalendarData = forms.FileField()

#     class Meta:
#         model = User
#         fields = ["username", "email", "password", "fisrt_name", "last_name"]

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']
#         def clean_password2(self):
#             cd = self.cleaned_data
#             if cd['password'] != cd['password2']:
#                 raise forms.ValidationError('Passwords don\'t match.')
#             return cd['password2']

class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'username',
            'id':'username',
            'type':'text',
            'placeholder':'John Doe',
            'maxlength': '16',
            'minlength': '6',
            })
        self.fields['email'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'email',
            'id':'email',
            'type':'email',
            'placeholder':'JohnDoe@mail.com',
            })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'password1',
            'id':'password1',
            'type':'password',
            'placeholder':'password',
            'maxlength':'22',
            'minlength':'8'
            })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'password2',
            'id':'password2',
            'type':'password',
            'placeholder':'password',
            'maxlength':'22',
            'minlength':'8'
            })


    username = forms.CharField(max_length=20, label=False)
    email = forms.EmailField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
