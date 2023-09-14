from django.db import models
from django.contrib.auth.models import User
from picklefield.fields import PickledObjectField

class image(models.Model):
    user_map=models.ForeignKey(User,default=None,on_delete=models.CASCADE)
    pic=models.ImageField(upload_to='images/', blank=True, null=True)
    facedata=PickledObjectField(default=None)

class custom(models.Model):
    user = models.ForeignKey(User,to_field='username',on_delete=models.CASCADE)
    year=models.CharField(max_length=8)
    branch=models.CharField(max_length=100, default=None)
    opt1=(
        ('1','PHD'),
        ('2','B-Tech'),
        ('3','MSc'),
        ('4','M-Tech')
    )
    opt2=(
        ('1','Vacuum'),
        ('2','Optics'),
    )
    department=models.CharField(max_length=100,default=None)
    course=models.CharField(max_length=100,default=None,choices=opt1)
    Elective=models.CharField(max_length=100,default=None,choices=opt2)

class complaint(models.Model):
    message=models.TextField(default=None, blank=True)
    email=models.EmailField(default=None, blank=True)
    name=models.CharField(max_length=100,default=None, blank=True)
    Roll_No=models.CharField(max_length=100,default=None, blank=True)