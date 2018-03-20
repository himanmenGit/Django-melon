from rest_framework.pagination import PageNumberPagination

__all__ = (
    'SmallSetPagination',
    'StandardResultsSetPagination',
)


class SmallSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 5


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10
