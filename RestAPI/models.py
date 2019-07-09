# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
import datetime


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender')
    receiver = models.ForeignKey(User, related_name='receiver')
    subject = models.CharField(max_length=1000)
    creation_date = models.DateTimeField(default=datetime.datetime.now())
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ('creation_date',)

    def __str__(self):
        return self.subject

    @classmethod
    def fetch_received_messages_for_user(cls, username):
        """
        Fetch all messages with status "unread" by specific username.
        :param username: {string} Target username.
        :return: {queryset} List of relevant messages.
        """
        user = User.objects.get(username=username)
        return cls.objects.filter(receiver=user.pk)

    @classmethod
    def fetch_received_unread_messages_for_user(cls, username):
        """
        Fetch all messages with status "unread" by specific username.
        :param username: {string} Target username.
        :return: {queryset} List of relevant messages.
        """
        user = User.objects.get(username=username)
        return cls.objects.filter(receiver=user.pk, is_read=False)

    def mark_as_read(self):
        """
        Mark message as read.
        :return: {void}
        """
        self.is_read = True
        self.save()

    def is_related_to_receiver(self, username):
        """
        Check if message related to receiver by username.
        :param username: {string} Receiver's username.
        :return: {bool} True if related to receiver.
        """
        if self.receiver.username == username:
            return True
        return False

    def is_from_sender(self, username):
        """
        Check if message sent by user for username.
        :param username: {string} Sender's username.
        :return: {bool} True if sent by sender.
        """
        if self.sender.username == username:
            return True
        return False
