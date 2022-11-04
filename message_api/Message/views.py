from django.http import Http404
from django.db.models import Q
from .serializers import MessageSerializer, MessageSerializerHeder
from .models import Message
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework import permissions


class MessagesList(APIView):

    @swagger_auto_schema(
        query_serializer=MessageSerializerHeder,
        responses={
            '200': openapi.Response('Json of all the messages', MessageSerializerHeder),
            '400': 'Bad Request'
        },
        permission_classes=[permissions.IsAuthenticated],
    operation_id='Masseges list',
        operation_description='All the sended and received messages for the current authenticated user',
    )
    def get(self, request, format=None):
        massages = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).order_by('-creation_date')
        serializer = MessageSerializerHeder(massages, many=True)
        return Response(data=serializer.data)

    @swagger_auto_schema(methods=['post'],
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['receiver', 'subject', 'message'],
                             properties={
                                 'receiver': openapi.Schema(type=openapi.TYPE_NUMBER),
                                 'subject': openapi.Schema(type=openapi.TYPE_STRING),
                                 'message': openapi.Schema(type=openapi.TYPE_STRING)
                             },
                         ),
                         permission_classes=[permissions.IsAuthenticated],
                         responses={
                             '201': openapi.Response('CREATED', status=status.HTTP_201_CREATED),
                             '400': 'Bad Request'
                         },
                         operation_id='Send new message',)
    @action(detail=True, methods=['POST'])
    def post(self, request, format=None):
        request.data['sender'] = request.user.id
        request.data['creation_date'] = datetime.date.today()
        request.data['read'] = False
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendMessageList(MessagesList):

    @swagger_auto_schema(
        query_serializer=MessageSerializerHeder,
        responses={
            '200': openapi.Response('Json of all the sended messages', MessageSerializerHeder),
            '400': 'Bad Request'
        },
        permission_classes=[permissions.IsAuthenticated],
        operation_id='Sended messages list',
        operation_description='List of all the messages sended by the user',
    )
    def get(self, request, format=None):
        massages = Message.objects.filter(sender=request.user).order_by('-creation_date')
        serializer = MessageSerializerHeder(massages, many=True)
        return Response(data=serializer.data)


class ReceiveMessageList(MessagesList):

    @swagger_auto_schema(
        query_serializer=MessageSerializerHeder,
        responses={
            '200': openapi.Response('Json of all the received messages', MessageSerializerHeder),
            '400': 'Bad Request'
        },
        permission_classes=[permissions.IsAuthenticated],
        operation_id='Received messages list',
        operation_description='List of all the messages the user received',
    )
    def get(self, request, format=None):
        massages = Message.objects.filter(receiver=request.user).order_by('-creation_date')
        serializer = MessageSerializerHeder(massages, many=True)
        return Response(data=serializer.data)


class MessageDetail(APIView):

    def get_massage(self, request, pk):
        try:
            msg = Message.objects.get(pk=pk)
            if msg.receiver == request.user or msg.sender == request.user:
                return msg
            raise Http404
        except:
            raise Http404

    @swagger_auto_schema(
        query_serializer=MessageSerializer,
        responses={
            '200': openapi.Response('Json of all the message detail', MessageSerializer),
            '404': '404'
        },
        permission_classes=[permissions.IsAuthenticated],
        operation_id='Message detail',
        operation_description='all the detail about the requested message. the message tagged as "read"',
    )
    def get(self, request, pk, format=None):
        massage = self.get_massage(request, pk)
        serializer = MessageSerializer(massage)
        massage.read = True
        massage.save()
        return Response(data=serializer.data)

    @swagger_auto_schema(
        responses={
            '204': openapi.Response('NO CONTENT', status=status.HTTP_204_NO_CONTENT),
            '404': '404'
        },
        permission_classes=[permissions.IsAuthenticated],
        operation_id='Delete message',
        operation_description='Delete specific message',
    )
    def delete(self, request, pk, format=None):
        massage = self.get_massage(request, pk)
        massage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UnreadMessageList(APIView):
    @swagger_auto_schema(
        responses={
            '200': openapi.Response('Json of all the unread messages', MessageSerializerHeder),
            '400': 'Bad Request'
        },
        permission_classes=[permissions.IsAuthenticated],
        operation_id='Unread message',
        operation_description='List of all the unread messages the user received',
    )
    def get(self, request, format=None):
        massages = Message.objects.filter(receiver=request.user, read=False).order_by('-creation_date')
        serializer = MessageSerializerHeder(massages, many=True)
        return Response(data=serializer.data)
