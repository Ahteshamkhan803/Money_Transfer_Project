from django.urls import path
from .views import send_money,TransactionView, search_users


urlpatterns = [
   
    path('send_money/', send_money, name='send_money'),
    path('transactions/', TransactionView.as_view(), name='transactions'),
    path('search_users/', search_users, name='search_users'),
    
]