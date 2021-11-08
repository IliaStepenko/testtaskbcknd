from datetime import datetime

import django
from django.contrib.auth import get_user_model
from django.db import models


class Chat(models.Model):

    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"

    name = models.CharField(max_length=75, null=False)
    short_link = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name


class Message(models.Model):

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        null=False
    )

    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        null=False
    )

    send_date = models.DateTimeField(auto_now_add=True)

    text = models.TextField(null=False, default='', blank=False)

    is_anonymous = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.author.first_name}   -   {self.send_date.strftime('%m/%d/%Y, %H:%M:%S')}"
