from django.urls import path
from . import views as massageViwes


urlpatterns = [
    path('', massageViwes.MessagesList.as_view()),
    path('sendMessages/', massageViwes.SendMessageList.as_view()),
    path('receiveMessages/', massageViwes.ReceiveMessageList.as_view()),
    path('unread/', massageViwes.UnreadMessageList.as_view()),
    path('message/<int:pk>', massageViwes.MessageDetail.as_view()),
    ]