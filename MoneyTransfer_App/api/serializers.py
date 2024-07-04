# from rest_framework import serializers
# from MoneyTransfer_App.models import Transaction, Account

# class TransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transaction
#         fields = ['sender', 'receiver', 'amount', 'description']

#     def validate(self, data):
#         sender = data['sender']
#         amount = data['amount']
#         sender_account = Account.objects.get(user=sender)

#         if sender_account.balance < amount:
#             raise serializers.ValidationError("Insufficient balance.")
        
#         return data


from rest_framework import serializers
from django.contrib.auth.models import User
from MoneyTransfer_App.models import UserProfile, Transaction

class UserProfileSerializer(serializers.ModelSerializer):
    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'profile_picture_url']

    def get_profile_picture_url(self, obj):
        if obj.profile_picture:
            return obj.profile_picture.url
        return None

class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'userprofile']

class TransactionSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    receiver = UserSerializer()

    class Meta:
        model = Transaction
        fields = ['sender', 'receiver', 'amount', 'timestamp', 'description']
