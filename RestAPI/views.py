# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.viewsets import ViewSet
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from django.http import Http404, HttpResponseBadRequest

from models import Message

from serializers import MessageSerializer


# Consts
MESSAGE_SENDER_KEY = 'sender'
REQUEST_QUERY_PARAMS_RECEIVER_PARAM = 'receiver'

# Error Messages Patterns Consts
FETCHING_MESSAGES_FOR_USER_ERROR_PATTERN = "User {0} may not exist or wrong param name passed, ERROR: {1}"
MESSAGE_WAS_NOT_FOUND_ERROR_PATTERN = "Massage with ID {0} not found, ERROR: {1}"


class MessagesViewSet(ViewSet):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        messages = Message.objects.all()
        messages_serializer = MessageSerializer(messages, many=True)
        return Response(messages_serializer.data)

    def create(self, request):
        message_data = request.data.dict()

        # Set logged user as a sender.
        message_data[MESSAGE_SENDER_KEY] = request.user.username

        message_serializer = MessageSerializer(data=message_data)

        if message_serializer.is_valid():
            message_serializer.save()
            return Response(message_serializer.data)
        return HttpResponseBadRequest("Problem accrued sending message."
                                      "Check passed request body arguments for validity.")

    def destroy(self, request, pk=None):
        try:
            message = Message.objects.get(pk=pk)
        except Exception as err:
            return Http404(MESSAGE_WAS_NOT_FOUND_ERROR_PATTERN.format(pk, err.message))

        logged_user = request.user.username

        if message.is_from_sender(logged_user) or message.is_related_to_receiver(logged_user):
            message.delete()
            return Response("Message with ID {0} was deleted successfully.".format(pk))
        return HttpResponseBadRequest("Message is not related to logged user.")

    @detail_route(methods=['post'])
    def read_message(self, request, pk=None):
        """
        Return message content by ID and mark it as read.
        """
        try:
            message = Message.objects.get(pk=pk)
        except Exception as err:
            return Http404(MESSAGE_WAS_NOT_FOUND_ERROR_PATTERN.format(pk, err.message))

        message.mark_as_read()
        serialized_message = MessageSerializer(message)
        return Response(serialized_message.data)

    @list_route(methods=['get'])
    def messages_for_user(self, request):
        """
        Get all messages received by user for username.
        """
        username = request.query_params.get(REQUEST_QUERY_PARAMS_RECEIVER_PARAM)
        try:
            messages = Message.fetch_received_messages_for_user(username=username)
        except Exception as err:
            return HttpResponseBadRequest(FETCHING_MESSAGES_FOR_USER_ERROR_PATTERN.format(
                username,
                err.message
            ))

        messages_serializer = MessageSerializer(messages, many=True)
        return Response(messages_serializer.data)

    @list_route(methods=['get'])
    def unread_messages_for_user(self, request):
        """
        Get all unread messages received by user for username.
        """
        username = request.query_params.get(REQUEST_QUERY_PARAMS_RECEIVER_PARAM)
        try:
            messages = Message.fetch_received_unread_messages_for_user(username=username)
        except Exception as err:
            return HttpResponseBadRequest(FETCHING_MESSAGES_FOR_USER_ERROR_PATTERN.format(
                username,
                err.message
            ))

        messages_serializer = MessageSerializer(messages, many=True)
        return Response(messages_serializer.data)