from djchoices.choices import ChoiceItem
from djchoices.choices import DjangoChoices

from django.db import models

from nomadgram.images.models import Comment
from nomadgram.images.models import Image
from nomadgram.images.models import TimeStampedModel
from nomadgram.users.models import User


class Notification(TimeStampedModel):
    """유저 알림 내용을 타입별로 저장한다"""

    class NotificationType(DjangoChoices):
        LIKE = ChoiceItem('Like')
        COMMENT = ChoiceItem('Comment')
        FOLLOW = ChoiceItem('Follow')

    creator = models.ForeignKey(User, related_name='creator')
    to = models.ForeignKey(User, related_name='to')
    notificaiton_type = models.CharField(max_length=20, choices=NotificationType.choices)
    image = models.ForeignKey(Image, null=True, blank=True)
    comment = models.ForeignKey(Comment, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return "From : {} - To: {}".format(self.creator, self.to)
