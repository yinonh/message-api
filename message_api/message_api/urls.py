from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegisterView
from rest_framework.urlpatterns import format_suffix_patterns




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('login/', obtain_auth_token),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('', include('Message.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)