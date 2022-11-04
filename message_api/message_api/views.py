from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserSerializer
from rest_framework import generics, permissions
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response





class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class UserDetail(APIView):
    def get_user(self, request, username):
        try:
            user = User.objects.get(username=username)
            if user.is_superuser:
                raise Http404
            return user
        except:
            raise Http404

    def get(self, request, username, format=None):
        user = self.get_user(request, username)
        serializer = UserSerializer(user)
        return Response(data=serializer.data)
