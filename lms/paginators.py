from rest_framework.pagination import PageNumberPagination


class CourseLessonPagination(PageNumberPagination):
    """
    Пагинация с параметрами:
    page_size - стартовый размер страницы
    page_size_query_param - имя параметра в запросе для размера страницы
    max_page_size - максимальный размер страницы
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
