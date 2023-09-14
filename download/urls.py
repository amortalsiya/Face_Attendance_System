from django.urls import path
from .import views
from django.contrib.auth import views as auth_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    
    path('download',views.down,name='face-down'),
    path('studdown',views.studdown,name='stud-down')
   
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
