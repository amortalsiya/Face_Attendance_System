from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError  
from .models import image

class Myform(UserCreationForm):
    username=forms.CharField(label='roll', max_length=8, required=True)
    first_name=forms.CharField(required=True)
    last_name=forms.CharField(required=True)
    email = forms.EmailField(label='college_email',required=True)
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password1','password2']


        def username_clean(self):  
            username = self.cleaned_data['username']
            new = User.objects.filter(username = username)  
            if new.count():  
                raise ValidationError("User Already Exist")  
            return username  
  
        def email_clean(self):  
            email = self.cleaned_data['email'].lower()  
            new = User.objects.filter(email=email)  
            if new.count():  
                raise ValidationError(" Email Already Exist")  
            return email  
  
        def clean_password2(self):  
            password1 = self.cleaned_data['password1']  
            password2 = self.cleaned_data['password2']  
    
            if password1 and password2 and password1 != password2:  
                raise ValidationError("Passwords didn't match")  
            return password2  

class yoform(UserCreationForm):
    year=forms.IntegerField(required=True)
    Roll_Number=forms.CharField(label='roll', max_length=8, required=True)
    first_name=forms.CharField(required=True)
    last_name=forms.CharField(required=True)
    college_email = forms.EmailField(label='college_email',required=True)
    class Meta:
        model=User
        fields=['Roll_Number','first_name','last_name','year','college_email','password1','password2']
class imageform(forms.ModelForm):
    
        class Meta:
            model = image
            fields = ['pic']
