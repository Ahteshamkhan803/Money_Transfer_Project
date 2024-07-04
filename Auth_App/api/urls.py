from django.urls import path
from Auth_App.api.views import Register_View, OtpVerification_view, home_view, Login_view, ResendOtpView, logout_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', Register_View.as_view(), name='register'),
    path('verify_otp/<str:email>/', OtpVerification_view.as_view(), name='verify_otp'),
    path('login/', Login_view.as_view(), name='login'),
    path('home/', home_view, name='home'),
    path('resend_otp/<str:email>/', ResendOtpView.as_view(), name='resend_otp'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', logout_view, name='logout'),
]

