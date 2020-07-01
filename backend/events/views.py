from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .models import Event
from .serializers import EventSerializer
from .permissions import IsOwner


class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return self.request.user.events.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
