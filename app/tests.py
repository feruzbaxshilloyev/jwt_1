from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User


class AuthTestCase(APITestCase):
    def test_registration(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'password123',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_login(self):
        user = User.objects.create_user(username='testuser', password='password123')
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'password123',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)


class UserCRUDTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin123')
        self.client.login(username='admin', password='admin123')
        self.user_data = {'username': 'user', 'password': 'testpass123', 'email': 'baxshilloyevferuz23.com'}

    def test_create_user(self):
        url = reverse('user-list-create')
        response = self.client.post(url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_list_users(self):
        url = reverse('user-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        response = self.client.put(url,
                                   {'username': 'user1', 'password': 'userpass123', 'email': 'baxshilloyevferuz23.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
