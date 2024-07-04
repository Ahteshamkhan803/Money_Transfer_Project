from django.contrib import admin

# Register your models here.
from Auth_App.models import TempUser



class Tempuser_Admin(admin.ModelAdmin):
    list_display=['username', 'password','email', 'otp', 'otp_created_at']

admin.site.register(TempUser, Tempuser_Admin)    