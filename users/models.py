from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from lms.models import Course, Lesson
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


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateTimeField(auto_now_add=True)
    paid_course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)

    def __str__(self):
        return f"Payment by {self.user.email} on {self.payment_date.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
