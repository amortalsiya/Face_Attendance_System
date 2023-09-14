from django.shortcuts import render
import datetime
import pymongo
import datetime
import pandas as pd

client=pymongo.MongoClient("mongodb://localhost:27017/")


def down(request):
    if request.method=="POST":
        cc=request.POST.get('course')
        date=request.POST.get('date')
        
        db=client.attendance
        
        collection=db[date]
        now = datetime.datetime.now()
        filename=now.strftime("%d%m%Y%H%M%S")
        filename=cc+filename
        all_records=collection.find({'Course':cc})
        print(all_records)
        
        list_cursor=list(all_records)
        df=pd.DataFrame(list_cursor)
        df = df.iloc[: , :-1]
        df.to_excel(r'' +filename+'.xlsx')
        
        
       
    return render(request,'userlogin/download.html')

def studdown(request):
    if request.method=="POST":
        date=request.POST.get('date')
        cc=request.user.username    
        db=client.attendance
        
        collection=db[date]
        now = datetime.datetime.now()
        filename=now.strftime("%d%m%Y%H%M%S")
        filename=cc+filename
        all_records=collection.find({'Roll':cc})
        print(all_records)
            
        list_cursor=list(all_records)
        df=pd.DataFrame(list_cursor)
        df = df.iloc[: , :-1]
        df.to_excel(r'' +filename+'.xlsx')
       
    return render(request,'userlogin/studdown.html')
    

