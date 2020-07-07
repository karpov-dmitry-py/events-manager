from datetime import datetime, timedelta
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from .models import Event
from .serializers import EventSerializer
from .permissions import IsOwner
from .paginators import EventsSetPagination


class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    pagination_class = EventsSetPagination

    def get_queryset(self):
        queryset = self.request.user.events.all()
        return queryset

    def filter_queryset(self, queryset):
        params = dict(self.request.query_params.items())
        filter_by_date = params.get('start_date', None)
        filter_by_title = params.get('title', None)

        if not (filter_by_date or filter_by_title):
            return queryset

        if filter_by_date:
            now = datetime.now()
            days_count = int(filter_by_date)
            comparison_date = datetime(year=now.year, month=now.month, day=now.day) - timedelta(days=days_count)
            queryset = queryset.filter(start_date__gte=comparison_date)

        if filter_by_title:
            queryset = queryset.filter(title__icontains=filter_by_title)

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
