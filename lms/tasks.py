from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta
from django.conf import settings
from users.models import User
from .models import Subscription, Course


@shared_task
def send_course_update_email(course_id):
    course = Course.objects.get(id=course_id)
    subscriptions = Subscription.objects.filter(course=course)
    emails = [sub.user.email for sub in subscriptions if sub.user.is_active]

    subject = f'Обновление курса: {course.title}'
    message = f'Привет! Курс "{course.title}" был обновлен. Посетите сайт, чтобы узнать подробности.'
    from_email = settings.DEFAULT_FROM_EMAIL

    for email in emails:
        send_mail(subject, message, from_email, [email])


@shared_task
def block_inactive_users():
    month_ago = now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=month_ago, is_active=True)

    count = inactive_users.update(is_active=False)
    return f"{count} пользователей были заблокированы."
