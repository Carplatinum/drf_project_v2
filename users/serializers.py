from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения данных пользователя без пароля"""
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar']

class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя с проверкой пароля"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)  # подтверждение пароля

    class Meta:
        model = User
        fields = ['email', 'phone', 'city', 'avatar', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data.get('phone', ''),
            city=validated_data.get('city', ''),
            avatar=validated_data.get('avatar', None),
        )
        return user
