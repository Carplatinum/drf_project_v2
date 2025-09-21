import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('drf_project')

# Загружаем настройки из Django settings с префиксом CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находим tasks.py в приложениях
app.autodiscover_tasks()

# Настройка timezone и beat scheduler
app.conf.timezone = settings.TIME_ZONE
app.conf.enable_utc = False
