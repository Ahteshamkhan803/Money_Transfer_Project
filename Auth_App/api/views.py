 
from urllib import response
from django.urls import reverse
from Auth_App.api.serializers import Register_serializer, otpVerificaion_Serializers
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Auth_App.models import TempUser
from .utils import generate_otp, send_otp
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from MoneyTransfer_App.models import UserProfile
from django.contrib.auth import logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

class Register_View(APIView):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        serializer = Register_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = generate_otp()

            temp_user = TempUser.objects.create(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
             
                email=email,
                otp=otp
            )

            send_otp(email, otp)
            return redirect('verify_otp', email=email)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class OtpVerification_view(APIView):
    def get(self, request, email=None):
        message = request.GET.get('message', '')
        return render(request, 'otp_verification.html', {'email': email, 'message': message})

    def post(self, request, email):
        serializer = otpVerificaion_Serializers(data=request.data)

        if serializer.is_valid():
            otp = serializer.validated_data['otp']
            try:
                temp_user = TempUser.objects.get(email=email, otp=otp)
                if timezone.now() > temp_user.otp_created_at + timezone.timedelta(minutes=1):
                    temp_user.delete()
                    message = 'OTP is expired. Please resend OTP.'
                    return redirect(f'{request.path}?message={message}')
                user = User.objects.create_user(
                    username=temp_user.username,
                    email=temp_user.email,
                    password=temp_user.password
                )
                temp_user.delete()
                return redirect('login')
            except TempUser.DoesNotExist:
                message = 'Invalid OTP. Please try again.'
                return redirect(f'{request.path}?message={message}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class Login_view(APIView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response = redirect('home')
            response.set_cookie('access_token', access_token, httponly=True)
            response.set_cookie('refresh_token', refresh_token, httponly=True)
            return response

        return render(request, 'login.html', {'errors': 'Invalid username or password'})


@login_required
def home_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            user_profile.profile_picture = profile_picture
            user_profile.save()
            messages.success(request, 'Profile picture uploaded successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please select a picture to upload.')

    return render(request, 'home.html', {'username': request.user})

@csrf_exempt  
def logout_view(request):
    response= redirect('login')
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
   
    return response
    



class ResendOtpView(APIView):
    def get(self, request, email):
        try:
            temp_user = TempUser.objects.get(email=email)
            otp = generate_otp()
            temp_user.otp = otp
            temp_user.otp_created_at = timezone.now()
            temp_user.save()
            send_otp(email, otp)
            message = 'A new OTP has been sent to your email.'
            return redirect(f'{request.path}?message={message}')
        except TempUser.DoesNotExist:
            return redirect('register')
