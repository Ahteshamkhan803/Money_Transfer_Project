from rest_framework import serializers
from django.contrib.auth.models import User
from Auth_App.models import TempUser





class Register_serializer(serializers.ModelSerializer):
    confirm_password= serializers.CharField(write_only=True)


    class Meta:
        model= TempUser
        fields= ['username', 'email', 'password', 'confirm_password']



    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError('both password must be same ')
        
        return  attrs
    



class otpVerificaion_Serializers(serializers.Serializer):
    email= serializers.CharField()
    otp= serializers.CharField(max_length=6)    