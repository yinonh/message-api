from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token



class MessagesTestCase(APITestCase):

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user('testerFinal', 'tester@testing.com', 'testpassword')

        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.token.save()

        self.client = APIClient()
        logged_in = self.client.login(username='testerFinal', password='testpassword')
        self.assertTrue(logged_in)



    def test_Login(self):
        token = Token.objects.get(user__username='testerFinal').key

        client = APIClient()

        url = reverse('login')
        response = client.post(url, {'username': 'testerFinal', 'password': 'testpassword'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], token)

    def test_user_detail(self):
        def test_request_without_client():
            unknownClient = APIClient()
            response = unknownClient.get(reverse('user_detail', kwargs={'username': self.user.username}))
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        def test_request_with_client():
            response = self.client.get(reverse('user_detail', kwargs={'username': self.user.username}))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_request_content():
            response = self.client.get(reverse('user_detail', kwargs={'username': self.user.username}))
            self.assertEqual(response.data['id'], self.user.id)
            self.assertTrue(len(response.data), 1)


        test_request_without_client()
        test_request_with_client()
        test_request_content()






