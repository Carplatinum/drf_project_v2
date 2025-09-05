from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsModerator(BasePermission):
    """
    Разрешает доступ только пользователям из группы 'moderators'.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and \
               request.user.groups.filter(name='moderators').exists()


class IsOwner(BasePermission):
    """
    Разрешает доступ только владельцу объекта.
    """
    def has_object_permission(self, request, view, obj):
        return hasattr(obj, 'owner') and obj.owner == request.user


class IsOwnerOrModeratorOrReadOnly(BasePermission):
    """
    Разрешает просмотр всем авторизованным.
    Модераторы могут изменять (кроме удаления/создания).
    Владельцы могут редактировать и удалять свои объекты.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        is_moder = request.user.groups.filter(name='moderators').exists()
        if request.method in SAFE_METHODS:
            return True
        if is_moder:
            # Модератор не может создавать (POST) и удалять (DELETE)
            if request.method in ['DELETE', 'POST']:
                return False
            return True
        # Владельцы могут редактировать и удалять свои объекты
        return hasattr(obj, 'owner') and obj.owner == request.user
