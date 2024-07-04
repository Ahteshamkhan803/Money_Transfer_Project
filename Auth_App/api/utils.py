
import random
from django.core.mail import send_mail

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp(email, otp,):
    
    subject = 'Your OTP Code'
    message = f'Your OTP code is {otp}. It is valid for 10 minutes.'
    from_email = 'noreply@example.com'
    send_mail(subject, message, from_email, [email])
