from django.conf import settings
from django.core.mail import send_mail
from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportMixin
from django.contrib.auth.hashers import make_password
from import_export.fields import Field
admin.site.register(image)
admin.site.register(custom)
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget


class UserResource(resources.ModelResource):
    password = Field(attribute='password', column_name='password')

    class Meta:
        model = User
        fields = ('username', 'password',
                  'first_name', 'last_name', 'email',)
        exclude = ('password')
        export_order = ('username', 'password',
                        'first_name', 'last_name', 'email')
        import_id_fields = ['username']
    def before_import_row(self, row, **kwargs):
        row['username'] = row['username'].upper()
        row['first_name'] = row['first_name'].upper()
        row['last_name'] = row['last_name'].upper()
        row['password'] = make_password(row['username'])
        mail_id = row['email']
        stud_name=str(row['first_name'])
        sbjt='Account creation for IIT Patna Face based authentication system.'
        msg="""Dear %(yo)s
        Your account has been created successfully for IIT PATNA's FACE ATTENDANCE SYSTEM.
        Your initial password is your Username(Roll Number) in Caps Lock.
        For example your Roll Number is 2001cs04 then your password is 2001CS04...Remember to change it at the earliest."""%{'yo':stud_name}        
        send_mail(
            sbjt,
            msg,
            settings.EMAIL_HOST_USER,
            [str(mail_id),],
        )


class UserAdmin(ImportExportModelAdmin):
    list_display=('username','first_name','last_name')
    resource_class = UserResource
    pass

class customResource(resources.ModelResource):
    user = fields.Field(
        column_name='user',
        attribute='user',
        widget=ForeignKeyWidget(User, 'username'))

    class Meta:
        model=custom
        fields = ('user','year','branch','department','course','Elective')
        export_order = ('user','year','branch','department','course','Elective')
        import_id_fields = ['user']
    def before_import_row(self, row, **kwargs):
        if(row['course']=='PHD'):
            row['course']=1;
        elif(row['course']=='B-Tech'):
            row['course']=2
        elif(row['course']=='M-Tech'):
            row['course']=3
        else:
            row['course']=4

        if(row['Elective']=='Vacuum'):
            row['Elective']=1;
        else:
            row['Elective']=2;

class customAdmin(ImportExportModelAdmin):
    resource_class = customResource
    list_display=('user','branch')
    pass
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(custom)
admin.site.register(custom, customAdmin)