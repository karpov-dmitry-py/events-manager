from datetime import datetime, timedelta
from django.core.mail import send_mass_mail
from django.http import HttpResponse
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


def alert(request):
    response = HttpResponse("<h1>No events to alert on!</h1>")
    comparison_date = datetime.now() + timedelta(hours=1)

    events = Event.objects.filter(start_date__gt=datetime.now())
    events = events.filter(start_date__lte=comparison_date)
    if not events:
        return response

    from_ = 'Your event management service'
    subject = 'Your planned event is coming soon!'
    emails = []

    for event in events:
        email = event.owner.email
        if not email:
            continue

        event_start_date = datetime.strftime(event.start_date, '%d.%m.%Y %H:%M')
        body = f'Hey, {event.owner.username}! Your planned event ({event.title}) is coming soon and ' \
               f'will start on {event_start_date}! Thanks!'

        message = (subject, body, from_, [email])
        emails.append(message)

    if emails:
        emails = tuple(emails)
        send_mass_mail(emails)

    response = HttpResponse(f'<h1>Alert(s) sent on {len(emails)} event(s)!</h1>')
    return response
