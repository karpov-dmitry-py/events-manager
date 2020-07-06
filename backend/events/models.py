from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    EVENT_TYPE_CHOICES = (
        ('meeting', 'Встреча'),
        ('call', 'Телефонный звонок'),
        ('webcast', 'Онлайн-вебинар'),
    )

    class Meta:
        ordering = ['id']

    title = models.CharField(max_length=500)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES, default='meeting')
    start_date = models.DateTimeField()
    body = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')

    def __str__(self):
        return f'<id:{self.id}> {self.title} ({self.owner}, начало: {self.start_date})'

