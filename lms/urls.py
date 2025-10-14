from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet, SubscriptionView, StripePaymentCreateView

app_name = 'lms'

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')

urlpatterns = [
    path('', include((router.urls, app_name), namespace=app_name)),
    path('subscription/', SubscriptionView.as_view(), name='subscription'),
    path('stripe/pay/', StripePaymentCreateView.as_view(), name='stripe-pay'),
]
