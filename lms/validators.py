from django.core.exceptions import ValidationError


def validate_video_url(value):
    """
    Валидатор для проверки, что ссылка ведёт только на youtube.com.
    Поддерживаются только ссылки с домена youtube.com.
    """
    if "youtube.com" not in value:
        raise ValidationError(
            'Ссылка должна быть с домена youtube.com',
            code='invalid_url'
        )
