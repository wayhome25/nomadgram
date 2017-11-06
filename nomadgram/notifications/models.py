from django.db import models

from nomadgram.images.models import Image
from nomadgram.images.models import TimeStampedModel
from nomadgram.users.models import User


class Notification(TimeStampedModel):

    TYPE_CHOICES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
    )

    creator = models.ForeignKey(User, related_name='creator')
    to = models.ForeignKey(User, related_name='to')
    notificaiton_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    image = models.ForeignKey(Image, null=True, blank=True)
