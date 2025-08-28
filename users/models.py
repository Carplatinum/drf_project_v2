from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Электронная почта'), unique=True)
    phone = models.CharField(_('Телефон'), max_length=20, blank=True)
    city = models.CharField(_('Город'), max_length=100, blank=True)
    avatar = models.ImageField(_('Аватарка'), upload_to='avatars/', blank=True, null=True)

    is_staff = models.BooleanField(_('Статус персонала'), default=False)
    is_active = models.BooleanField(_('Активен'), default=True)

    date_joined = models.DateTimeField(_('Дата регистрации'), auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        return self.email
