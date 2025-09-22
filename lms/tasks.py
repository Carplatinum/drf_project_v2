from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from users.models import User
from django.core.mail import send_mail
from .models import Course, Subscription


@shared_task
def block_inactive_users():
    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)
    count = inactive_users.update(is_active=False)
    return f"{count} пользователей были заблокированы."


@shared_task
def send_course_update_email(course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return "Курс не найден."
    subscriptions = Subscription.objects.filter(course=course)
    emails = [sub.user.email for sub in subscriptions]
    subject = f"Обновление курса: {course.title}"
    message = f"В курсе '{course.title}' произошли изменения. Перейдите, чтобы узнать детали."
    send_mail(subject, message, None, emails)
    return f"Отправлено {len(emails)} уведомлений."
