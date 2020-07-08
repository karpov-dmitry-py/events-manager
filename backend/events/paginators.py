from rest_framework.pagination import CursorPagination


class EventsSetPagination(CursorPagination):
    page_size = 5
    ordering = 'id'
