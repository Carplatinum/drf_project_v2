from rest_framework import generics
from .models import User
from .serializers import UserSerializer, UserCreateSerializer

# Для просмотра профиля пользователя (GET)
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Для регистрации нового пользователя (POST)
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
