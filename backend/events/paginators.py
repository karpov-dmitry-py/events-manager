from rest_framework.pagination import CursorPagination


class EventsSetPagination(CursorPagination):
    page_size = 7
    ordering = 'id'
