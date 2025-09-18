from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsOwnerOrModeratorOrReadOnly
from .paginators import CourseLessonPagination
from users.models import Payment
from .stripe_services import create_product, create_price, create_checkout_session


class StripePaymentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        product = create_product(course.title)
        price = create_price(product['id'], course.price)

        domain = 'http://localhost:8000'
        success_url = f"{domain}/success/"
        cancel_url = f"{domain}/cancel/"
        session = create_checkout_session(price['id'], success_url, cancel_url)

        Payment.objects.create(
            user=request.user,
            paid_course=course,
            amount=course.price,
            payment_method='stripe',
            stripe_product_id=product['id'],
            stripe_price_id=price['id'],
            stripe_session_id=session['id']
        )

        return Response({'checkout_url': session.url})


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для курсов с пагинацией и правами
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CourseLessonPagination

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsOwnerOrModeratorOrReadOnly()]
        elif self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonViewSet(viewsets.ModelViewSet):
    """
    ViewSet для уроков с пагинацией и правами
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CourseLessonPagination

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsOwnerOrModeratorOrReadOnly()]
        elif self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubscriptionView(APIView):
    """
    APIView для управления подписками пользователей на курсы.
    При POST запросе подписывает пользователя на курс или удаляет подписку.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        subscription_qs = Subscription.objects.filter(user=user, course=course)

        if subscription_qs.exists():
            subscription_qs.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'подписка добавлена'

        return Response({"message": message})
