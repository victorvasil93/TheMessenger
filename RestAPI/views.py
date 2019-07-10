# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.viewsets import ViewSet
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from django.http import Http404, HttpResponseBadRequest

from .models import Message

from .serializers import MessageSerializer


# Consts
MESSAGE_SENDER_KEY = 'sender'
REQUEST_QUERY_PARAMS_RECEIVER_PARAM = 'receiver'

# Error Messages Patterns Consts
FETCHING_MESSAGES_FOR_USER_ERROR_PATTERN = "User {0} may not exist, ERROR: {1}"
MESSAGE_WAS_NOT_FOUND_ERROR_PATTERN = "Error accrued fetching messages for {0}, ERROR: {1}"
MESSAGE_IS_NOT_RELATED_TO_USER_PATTERN = "Message is not related to logged user."


class MessagesViewSet(ViewSet):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        logged_user = request.user.username
        message_data = request.data.dict()

        # Set logged user as a sender.
        message_data[MESSAGE_SENDER_KEY] = logged_user

        message_serializer = MessageSerializer(data=message_data)

        if message_serializer.is_valid():
            message_serializer.save()
            return Response(message_serializer.data)
        return HttpResponseBadRequest("Problem accrued sending message."
                                      "Check passed request body arguments for validity.")

    def destroy(self, request, pk=None):
        logged_user = request.user.username

        try:
            message = Message.objects.get(pk=pk)
        except Exception as err:
            return Http404(MESSAGE_WAS_NOT_FOUND_ERROR_PATTERN.format(pk, err.message))

        if message.is_from_sender(logged_user) or message.is_related_to_receiver(logged_user):
            message.delete()
            return Response("Message with ID {0} was successfully deleted.".format(pk))
        return HttpResponseBadRequest(MESSAGE_IS_NOT_RELATED_TO_USER_PATTERN)

    @detail_route(methods=['post'])
    def read_message(self, request, pk=None):
        """
        Return message content by ID and mark it as read.
        """
        logged_user = request.user.username

        try:
            message = Message.objects.get(pk=pk)
        except Exception as err:
            return Http404(MESSAGE_WAS_NOT_FOUND_ERROR_PATTERN.format(pk, err.message))

        if message.is_related_to_receiver(logged_user):
            message.mark_as_read()
            serialized_message = MessageSerializer(message)
            return Response(serialized_message.data)
        return HttpResponseBadRequest(MESSAGE_IS_NOT_RELATED_TO_USER_PATTERN)

    @list_route(methods=['get'])
    def received_messages(self, request):
        """
        Get all messages received by logged user.
        """
        logged_user = request.user.username

        try:
            messages = Message.fetch_received_messages_for_user(username=logged_user)
        except Exception as err:
            return HttpResponseBadRequest(FETCHING_MESSAGES_FOR_USER_ERROR_PATTERN.format(
                logged_user,
                err.message
            ))

        messages_serializer = MessageSerializer(messages, many=True)
        return Response(messages_serializer.data)

    @list_route(methods=['get'])
    def unread_messages(self, request):
        """
        Get all unread messages received by logged user.
        """
        logged_user = request.user.username

        try:
            messages = Message.fetch_received_unread_messages_for_user(username=logged_user)
        except Exception as err:
            return HttpResponseBadRequest(FETCHING_MESSAGES_FOR_USER_ERROR_PATTERN.format(
                logged_user,
                err.message
            ))

        messages_serializer = MessageSerializer(messages, many=True)
        return Response(messages_serializer.data)
