import django_filters
from django.contrib.auth.models import User

class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='startswith')
    email = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['username', 'email']





import django_filters
from MoneyTransfer_App.models import UserProfile

class UserProfileFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    email = django_filters.CharFilter(field_name='user__email', lookup_expr='icontains')
    phone_number = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = UserProfile
        fields = ['user', 'email', 'phone_number']