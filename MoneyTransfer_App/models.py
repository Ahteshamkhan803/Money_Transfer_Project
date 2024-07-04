from django.db import models
from django.contrib.auth.models import User


#this model is for storing user priile data

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    



#this is for storing account information

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s account"




#this is for transaction details

class Transaction(models.Model):
    sender = models.ForeignKey(User, related_name='sent_transactions', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Transaction from {self.sender.username} to {self.receiver.username} for {self.amount}"
