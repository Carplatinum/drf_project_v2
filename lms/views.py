from rest_framework import viewsets, permissions
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsOwnerOrModeratorOrReadOnly, IsModerator
from rest_framework.permissions import IsAuthenticated

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        # Разделяем права в зависимости от action
        if self.action in ['create', 'destroy']:
            # Создавать и удалять могут только аутентифицированные, не модераторы
            # Создавать и удалять МОГУТ только владельцы, но т.к. пользователь создает,
            # то проверим, что он не модератор (т.к. модератор запрещен создавать/удалять)
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update']:
            # Обновлять могут владельцы или модераторы (кроме удаления/создания)
            return [IsAuthenticated(), IsOwnerOrModeratorOrReadOnly()]
        elif self.action == 'list':
            # Просмотр списка только для авторизованных
            return [IsAuthenticated()]
        elif self.action == 'retrieve':
            # Просмотр объекта - для всех авторизованных
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            # Создавать и удалять могут только аутентифицированные (не модераторы)
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update']:
            # Обновлять могут владельцы или модераторы
            return [IsAuthenticated(), IsOwnerOrModeratorOrReadOnly()]
        elif self.action == 'list':
            return [IsAuthenticated()]
        elif self.action == 'retrieve':
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
