from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Document

class DocumentAPITests(APITestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_create_document(self):
        # Test document creation
        url = '/api/documents/'
        data = {'title': 'Test Document', 'content': 'Content for the test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_documents(self):
        # Test fetching all documents
        Document.objects.create(title="Doc 1", content="Content 1", user=self.user)
        Document.objects.create(title="Doc 2", content="Content 2", user=self.user)
        response = self.client.get('/api/documents/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_document(self):
        document = Document.objects.create(title="Doc 1", content="Content 1", user=self.user)
        response = self.client.get(f'/api/documents/{document.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_document(self):
        document = Document.objects.create(title="Doc 1", content="Content 1", user=self.user)
        data = {'title': 'Updated Title'}
        response = self.client.patch(f'/api/documents/{document.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')

    def test_delete_document(self):
        document = Document.objects.create(title="Doc 1", content="Content 1", user=self.user)
        response = self.client.delete(f'/api/documents/{document.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
