from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Document
from .serializers import DocumentSerializer
import json

class DocumentAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.login_url = reverse('login', kwargs={'id': self.user.id})

        # Login and store token
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass123'
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Create a test document
        self.document = Document.objects.create(
            title='Test Doc',
            content='Test Content',
            created_by=self.user
        )

    def test_list_documents(self):
        url = reverse('document-list')  # from router
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) >= 1)

    def test_create_document(self):
        url = reverse('document-list')
        data = {
            'title': 'New Doc',
            'content': 'Content here',
            'created_by': self.user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_document(self):
        url = reverse('document-detail', args=[self.document.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], self.document.title)

    def test_update_document(self):
        url = reverse('document-detail', args=[self.document.id])
        response = self.client.put(url, {
            'title': 'Updated Title',
            'content': 'Updated Content',
            'created_by': self.user.id
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Updated Title')

    def test_delete_document(self):
        url = reverse('document-detail', args=[self.document.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
