from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class TempUser(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    otp = models.CharField(max_length=6)
    otp_created_at = models.DateTimeField(auto_now_add=True)
    


    def save(self, *args, **kwargs):
        self.otp_created_at = timezone.now() 
        super().save(*args, **kwargs)