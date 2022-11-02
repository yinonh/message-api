"""message_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from Message import views as massageViwes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', massageViwes.MessagesList.as_view()),
    path('sendMassages/', massageViwes.SendMessageList.as_view()),
    path('reciveMassages/', massageViwes.ReciveMessageList.as_view()),
    path('unread/', massageViwes.UnreadMessageList.as_view()),
    path('<int:pk>', massageViwes.MessageDetail.as_view()),
    path('login/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls')),

]

urlpatterns = format_suffix_patterns(urlpatterns)