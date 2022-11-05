from django.urls import path
from . import views as massageViwes


urlpatterns = [
    path('', massageViwes.MessagesList.as_view(), name='all_messages'),
    path('sendMessages/', massageViwes.SendMessageList.as_view(), name='sended_messages'),
    path('receiveMessages/', massageViwes.ReceiveMessageList.as_view(), name='received_messages'),
    path('unread/', massageViwes.UnreadMessageList.as_view(), name='unread_messages'),
    path('message/<int:pk>', massageViwes.MessageDetail.as_view(), name='message_detail'),
    ]