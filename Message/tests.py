from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Message



class MessagesTestCase(APITestCase):

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user('testerFinal', 'tester@testing.com', 'testpassword')
        self.user2 = User.objects.create_user('tester2', 'tester2@testing.com', 'testpassword')
        self.user.save()
        self.user2.save()
        self.client = APIClient()
        self.message1 = Message.objects.create(sender=self.user, receiver=self.user2, subject='test',
                                               message='test test')
        self.message1.save()
        self.message2 = Message.objects.create(sender=self.user2, receiver=self.user, subject='test',
                                               message='test test')
        self.message2.save()
        self.message3 = Message.objects.create(sender=self.user2, receiver=self.user2, subject='test',
                                               message='test test')
        self.message3.save()
        # assure login
        logged_in = self.client.login(username='testerFinal', password='testpassword')
        self.assertTrue(logged_in)

    def test_MessagesList(self):

        def test_request_without_client():
            unknownClient = APIClient()
            response = unknownClient.get(reverse('all_messages'))
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        def test_request_with_client():
            response = self.client.get(reverse('all_messages'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_request_content():
            response = self.client.get(reverse('all_messages'))
            self.assertEqual(response.data[0]['id'], self.message1.id)
            self.assertEqual(response.data[1]['id'], self.message2.id)
            self.assertTrue(len(response.data), 2)

        def test_message_post():
            user_sended_messages = len(Message.objects.filter(sender=self.user.id))
            url = reverse('all_messages')
            response = self.client.post(url, {'sender': '35', 'receiver': str(self.user2.id), 'subject': 'test',
                                            'message': 'test test'}, format='json')

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(len(Message.objects.filter(sender=35)), 0)
            self.assertEqual(len(Message.objects.filter(sender=self.user.id)), user_sended_messages + 1)

        test_request_without_client()
        test_request_with_client()
        test_request_content()
        test_message_post()

    def test_SendMessageList(self):

        def test_request_without_client():
            unknownClient = APIClient()
            response = unknownClient.get(reverse('sended_messages'))
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        def test_request_with_client():
            response = self.client.get(reverse('sended_messages'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_request_content():
            response = self.client.get(reverse('sended_messages'))
            self.assertEqual(response.data[0]['id'], self.message1.id)
            self.assertTrue(len(response.data), 1)

        def test_message_post():
            user_sended_messages = len(Message.objects.filter(sender=self.user.id))
            url = reverse('sended_messages')
            response = self.client.post(url, {'sender': '35', 'receiver': str(self.user2.id), 'subject': 'test',
                                              'message': 'test test'}, format='json')

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(len(Message.objects.filter(sender=35)), 0)
            self.assertEqual(len(Message.objects.filter(sender=self.user.id)), user_sended_messages + 1)

        test_request_without_client()
        test_request_with_client()
        test_request_content()
        test_message_post()

    def test_ReceiveMessageList(self):
        def test_request_without_client():
            unknownClient = APIClient()
            response = unknownClient.get(reverse('received_messages'))
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        def test_request_with_client():
            response = self.client.get(reverse('received_messages'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_request_content():
            response = self.client.get(reverse('received_messages'))
            self.assertEqual(response.data[0]['id'], self.message2.id)
            self.assertTrue(len(response.data), 1)

        def test_message_post():
            user_sended_messages = len(Message.objects.filter(sender=self.user.id))
            url = reverse('received_messages')
            response = self.client.post(url, {'sender': '35', 'receiver': str(self.user2.id), 'subject': 'test',
                                              'message': 'test test'}, format='json')

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(len(Message.objects.filter(sender=35)), 0)
            self.assertEqual(len(Message.objects.filter(sender=self.user.id)), user_sended_messages + 1)

        test_request_without_client()
        test_request_with_client()
        test_request_content()
        test_message_post()

    def test_MessageDetail(self):

        def test_request_without_client():
            unknownClient = APIClient()
            response = unknownClient.get(reverse('message_detail', kwargs={'pk': self.message1.id}))
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        def test_request_with_client():
            response = self.client.get(reverse('message_detail', kwargs={'pk': self.message1.id}))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_request_content():
            response = self.client.get(reverse('message_detail', kwargs={'pk': self.message1.id}))
            self.assertEqual(response.data['id'], self.message1.id)
            self.assertTrue(len(response.data), 1)

        def test_delete():
            self.assertEqual(len(Message.objects.filter(pk=self.message1.id)), 1)
            url = reverse('message_detail', kwargs={'pk': self.message1.id})
            response = self.client.delete(url)

            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(len(Message.objects.filter(pk=self.message1.id)), 0)

        test_request_without_client()
        test_request_with_client()
        test_request_content()
        test_delete()

    def test_UnreadMessage(self):
        def test_request_without_client():
            unknownClient = APIClient()
            response = unknownClient.get(reverse('unread_messages'))
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        def test_request_with_client():
            response = self.client.get(reverse('unread_messages'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_request_content_unread():
            response = self.client.get(reverse('unread_messages'))
            self.assertEqual(response.data[0]['id'], self.message2.id)
            self.assertEqual(len(response.data), 1)

        def test_request_content_read():
            client2 = APIClient()
            logged_in = client2.login(username='tester2', password='testpassword')
            self.assertTrue(logged_in)

            response = client2.get(reverse('unread_messages'))
            self.assertEqual(len(response.data), 2)

            response = self.client.get(reverse('message_detail', kwargs={'pk': self.message1.id}))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            response = client2.get(reverse('unread_messages'))
            self.assertEqual(len(response.data), 1)


        test_request_without_client()
        test_request_with_client()
        test_request_content_unread()
        test_request_content_read()
