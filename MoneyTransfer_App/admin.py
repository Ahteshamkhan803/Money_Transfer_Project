from django.contrib import admin
from MoneyTransfer_App.models import UserProfile, Account, Transaction

# Register your models here.


class userProfile_Admin(admin.ModelAdmin):
    list_display=['user','phone_number','profile_picture']
admin.site.register(UserProfile,userProfile_Admin)    




class Account_Admin(admin.ModelAdmin):
    list_display=['user','balance']
admin.site.register(Account,Account_Admin)  




class Transaction_Admin(admin.ModelAdmin):
    list_display=['sender','receiver','amount','timestamp','description']
admin.site.register(Transaction,Transaction_Admin)  



