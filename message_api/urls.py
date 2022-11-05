from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegisterView, UserDetail
from rest_framework.urlpatterns import format_suffix_patterns

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Message API",
        default_version='1.0.0',
        description="API documentation"
    ),
    #public=True
)

urlpatterns = [
    path('admin/', admin.site.urls, name='admin_panel'),
    path('api-auth/', include('rest_framework.urls')),
    path('login/', obtain_auth_token, name='login'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='documentation'),
    path('', include('Message.urls')),
    path('<str:username>', UserDetail.as_view(), name='user_detail'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
