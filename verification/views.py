from django.shortcuts import render
from django.contrib import messages
from userlogin.models import *
import face_recognition
import urllib
import datetime
import pymongo
import datetime

def take():
    file1 = open(r"D:\Text\setting.txt", "r") 
    a=file1.read()
    num=int(a)
    file1.close()
    return num

def up():
    file1 = open(r"D:\Text\setting.txt", "r") 
    a=file1.read()
    num=int(a)
    file1.close()
    
    file2 = open(r"D:\Text\setting.txt", "w+")
    if(num!=26):
        num=num+1
    else:
        num=24
    print(num)
    file2.write(str(num))
    file1.close()


def remove(name):
    yo = ""
    for i in range(len(name)):
        if (name[i] == '-' or name[i] == ' ' or name[i] == ':'):
            pass
        else:
            yo += str(name[i])
    return yo

client=pymongo.MongoClient("mongodb://localhost:27017/")

def upload_webcam_mod(request):
    print(request)
    course_name=request.GET.get('course')
    if request.method == 'POST':
        print("jdslkfjlsdf")
        hello = request.POST.get('data')
        cur = datetime.datetime.now()
        cur = remove(str(cur))
        response = urllib.request.urlopen(hello)
        name = "D:\\new\Attendance_System-main\media\images\\"+cur
        filename = "%s.jpg" % name
        with open(filename, 'wb') as f:
            f.write(response.file.read())
        rawimage = face_recognition.load_image_file(filename)
        print(course_name)

    try:
        encodings = face_recognition.face_encodings(rawimage)[0]
        now = datetime.datetime.now()
        year=now.strftime("%Y")
        month=now.strftime("%m")
        day=now.strftime("%d")
        date=year+'-'+month+'-'+day


        db=client.Face_Try
        collection=db.auth_user
        
        db2=client.attendance
        collection2=db2[date]

   
        total=image.objects.all()
        known_face_encodings=[]
        known_usermapid=[]
      
        for x in total:
            if x.facedata is None:
                continue
            known_face_encodings.append(x.facedata)
            known_usermapid.append(x.user_map_id)
            

        all_face_locations = face_recognition.face_locations(rawimage, number_of_times_to_upsample=2,model='cnn')
        all_face_encodings=face_recognition.face_encodings(rawimage,all_face_locations)
        for current_face_location, current_face_encoding in zip(all_face_locations,all_face_encodings):
                if current_face_encoding is None:
                    continue
                
                all_matches=face_recognition.compare_faces(known_face_encodings,current_face_encoding,tolerance=0.6)
                if True in all_matches:
                    first_match_index=all_matches.index(True)
                    userid=take()
                    up()
                    
                    records=collection.find_one({'id':userid})



                    my_dict = {"user_map_id": userid,
                                "First Name": records["first_name"],
                                "Last Name" : records["last_name"],
                                "Email" : records["email"],
                                "Course" : course_name,
                                "Roll" :records["username"],
                                "Date_Time": now,
                                }

                    collection2.insert_one(my_dict)
                    
        messages.success(request, f'Your attendance was marked.')

    except:
        messages.warning(request, f'Face not captured. Try again')
    return render(request, 'userlogin/upload_webcam_modified.html')