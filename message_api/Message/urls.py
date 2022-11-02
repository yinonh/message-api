from django.urls import path, include
from . import views as massageViwes


urlpatterns = [
    path('', massageViwes.MessagesList.as_view()),
    path('sendMassages/', massageViwes.SendMessageList.as_view()),
    path('reciveMassages/', massageViwes.ReciveMessageList.as_view()),
    path('unread/', massageViwes.UnreadMessageList.as_view()),
    path('<int:pk>', massageViwes.MessageDetail.as_view()),
    ]