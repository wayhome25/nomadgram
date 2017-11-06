from django.contrib import admin

from nomadgram.notifications.models import Notification


@admin.register(Notification)
class NotificaionAdmin(admin.ModelAdmin):
    list_display = ['creator', 'to', 'notificaiton_type']
