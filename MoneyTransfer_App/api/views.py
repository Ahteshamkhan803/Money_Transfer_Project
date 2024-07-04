
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from MoneyTransfer_App.models import Account, Transaction, UserProfile
from django.contrib.auth.models import User
from MoneyTransfer_App.api.filters import UserFilter, UserProfileFilter
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view , permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import TransactionSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from rest_framework_simplejwt.views import TokenRefreshView
# def register_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             Account.objects.create(user=user)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()
#     return render(request, 'register.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'login.html', {'form': form})

@login_required
def home_view(request):
    return render(request, 'home.html')







@login_required
def send_money(request):
    username = request.GET.get('username', '')
    
   

    # user_filter = UserFilter(request.GET, queryset=User.objects.all())

    if request.method == 'POST':
        username = request.POST.get('username')
        amount = request.POST.get('amount')
        receiver = get_object_or_404(User, username=username)

        if receiver == request.user:
            messages.error(request, 'You cannot send money to yourself.')
            return redirect('send_money')
        
        sender_account = get_object_or_404(Account, user=request.user)
        receiver_account = get_object_or_404(Account, user=receiver)

        amount = Decimal(amount)
        if sender_account.balance >= amount:
            sender_account.balance -= amount
            receiver_account.balance += amount
            sender_account.save()
            receiver_account.save()

            Transaction.objects.create(
                sender=request.user,
                receiver=receiver,
                amount=amount,
                description="Money transfer"
            )

            messages.success(request, 'Money sent successfully!')
            return redirect('send_money')
        else:
            messages.error(request, 'Insufficient balance!')

    return render(request, 'send_money.html', { 'username':username})



class TransactionView(LoginRequiredMixin, TemplateView):
    
  
    template_name = 'transactions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        
        sent_transactions = Transaction.objects.filter(sender=self.request.user).select_related('receiver__userprofile').order_by('-timestamp')
        received_transactions = Transaction.objects.filter(receiver=self.request.user).select_related('sender__userprofile').order_by('-timestamp')
        

        sent_paginator = Paginator(sent_transactions, 5)  
        sent_page_number = self.request.GET.get('sent_page')
        context['sent_transactions_page'] = sent_paginator.get_page(sent_page_number)

        # Paginate received transactions
        received_paginator = Paginator(received_transactions, 5)  
        received_page_number = self.request.GET.get('received_page')
        context['received_transactions_page'] = received_paginator.get_page(received_page_number)
        return context
    



@login_required
def search_users(request):
    user_filter = UserProfileFilter(request.GET, queryset=UserProfile.objects.all())
    return render(request, 'search_user.html', {'filter': user_filter})



class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        
        if 'access' not in response.data:
            
            return redirect(reverse_lazy('login'))
        
        return response

