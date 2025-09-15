import re
from urllib.parse import urlparse
from rest_framework import serializers


class VideoUrlValidator:
    """Проверка содержания материалов на наличие сторонних ссылок
    Разрешены только ссылки на YouTube (youtube.com, www.youtube.com, youtu.be)
    """

    def __init__(self, fields):
        self.fields = fields  # список полей для проверки

    def __call__(self, value):
        # value — словарь с полями сериализатора
        url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\.-]*\??[/\w\.-=&%]*'

        for field in self.fields:
            temp_value = value.get(field)
            if temp_value:
                urls = re.findall(url_pattern, temp_value)
                for url in urls:
                    parsed_url = urlparse(url)
                    domain = parsed_url.netloc.lower()
                    allowed_domains = ['youtube.com', 'www.youtube.com', 'youtu.be']
                    if not any(allowed_domain in domain for allowed_domain in allowed_domains):
                        raise serializers.ValidationError(
                            f"В поле '{field}' разрешены только ссылки на YouTube"
                        )
