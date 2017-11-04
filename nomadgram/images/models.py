from django.db import models

from nomadgram.users.models import User


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Image(TimeStampedModel):
    """Image Model"""
    file = models.ImageField("photo")
    location = models.TextField("location", blank=True)
    caption = models.TextField("caption", blank=True)
    creator = models.ForeignKey(User)

    @property
    def like_count(self):
        return self.likes.count()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return '{} - {}'.format(self.location, self.caption)


class Comment(TimeStampedModel):
    """Comment Model"""
    message = models.TextField()
    creator = models.ForeignKey(User)
    image = models.ForeignKey(Image, related_name='comments')

    def __str__(self):
        return self.message


class Like(TimeStampedModel):
    """Like Model"""
    creator = models.ForeignKey(User)
    image = models.ForeignKey(Image, related_name='likes')

    def __str__(self):
        return 'User: {} - Image Caption: {}'.format(self.creator.username, self.image.caption)
