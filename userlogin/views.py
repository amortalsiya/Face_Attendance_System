from django.shortcuts import render, redirect
from userlogin.forms import Myform, imageform
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
import cv2
import face_recognition
import numpy as np
import urllib
import datetime
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import pymongo
import datetime
from django.urls import reverse
from urllib.parse import urlencode



client=pymongo.MongoClient("mongodb://localhost:27017/")




def home(request):
    return render(request, 'userlogin/home.html')




def remove(name):
    yo = ""
    for i in range(len(name)):
        if (name[i] == '-' or name[i] == ' ' or name[i] == ':'):
            pass
        else:
            yo += str(name[i])
    return yo




def _grab_image(path=None, stream=None, url=None):
    if path is not None:
        image = cv2.imread(path)
    else:
        if url is not None:
            resp = urllib.urlopen(url)
            data = resp.read()
        elif stream is not None:
            data = stream.read()
        image = np.asarray(bytearray(data), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image




@login_required(login_url='login')
def profile(request):
    return render(request, 'userlogin/profile.html')




@login_required(login_url='login')
def upload_comp(request):
    if request.method == 'POST':
        form = imageform(request.POST, request.FILES)
        if form.is_valid():
            wait_for_now = form.save(commit=False)
            wait_for_now.user_map = request.user
            rawimage = _grab_image(stream=request.FILES["pic"])
            try:
                encodings = face_recognition.face_encodings(rawimage)[0]
                wait_for_now.facedata = encodings
                wait_for_now.save()
                messages.success(request, f'Your image was uploaded.')
            except:
                messages.warning(request, f'Image not detected. Try again')
    else:
        form = imageform()
    return render(request, 'userlogin/upload_comp.html', {'form': form})






@login_required(login_url='login')
def upload_webcam(request):
    if request.method == 'POST':
        aman = request.POST.get('data')
        cur = datetime.datetime.now()
        cur = remove(str(cur))
        response = urllib.request.urlopen(aman)
        name = "D:\\new\Attendance_System-main\media\images\\"+cur
        filename = "%s.jpg" % name
        with open(filename, 'wb') as f:
            f.write(response.file.read())
        webcam = image()
        yo = "images/" + cur+".jpg"
        webcam.pic = yo
        webcam.user_map = request.user
        rawimage = face_recognition.load_image_file(filename)
    try:
        encodings = face_recognition.face_encodings(rawimage)[0]
        webcam.facedata = encodings
        webcam.save()
        messages.success(request, f'Your image was uploaded.')
    except:
        messages.warning(request, f'Face not captured. Try again')
    return render(request, 'userlogin/upload_webcam.html')




@login_required(login_url='login')
def view(request):
    if request.method == 'GET':
        all = image.objects.filter(user_map=request.user)
    return render(request, 'userlogin/view.html', {'images': all})


def register(request):
    if request.method == "POST":
        form = Myform(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Your {username} account was created successfully.')
    else:
        form = Myform()
    return render(request, 'userlogin/register.html', {
        'form': form
    })





def change_passwd(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'userlogin/change_pass.html', {
        'form': form
    })





def feedback(request):
    if request.method=='POST':
        store_val=complaint()
        store_val.message=request.POST.get('message')
        store_val.email=request.user.email
        store_val.name=request.user.first_name
        store_val.Roll_No=request.user.username
        store_val.name=store_val.name.upper()
        store_val.save()
        messages.success(request, 'Your message/complaint was submitted.')
        return redirect('/')
    return render(request,'userlogin/feedback_complaint.html')

def markattendance(request):
    if request.method=='POST':
        course_name=request.POST.get('course')
        base_url = reverse('upload_webcam_mod') 
        query_string =  urlencode({'course': course_name})
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)
    
    return render(request,'userlogin/markme.html')


def admin_main(request):
  return render(request,'userlogin/admin_forward.html')