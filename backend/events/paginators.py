from rest_framework.pagination import PageNumberPagination


class EventsSetPagination(PageNumberPagination):
    page_size = 5
