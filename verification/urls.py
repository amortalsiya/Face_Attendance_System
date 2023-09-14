from django.urls import path
from .import views
from django.contrib.auth import views as auth_view
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    
 
    path('upload_webcam_mod',views.upload_webcam_mod,name="upload_webcam_mod"),
   
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
