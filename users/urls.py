from django.urls import path
from .views import UserCreateView, UserDetailView

app_name = 'users'

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
