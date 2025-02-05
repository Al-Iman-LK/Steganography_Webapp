from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.core.models import SteganoFile
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

class APITests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_file_upload_api(self):
        """Test file upload through API"""
        url = reverse('api:steganofile-list')
        test_file = SimpleUploadedFile(
            "test.png",
            b"file_content",
            content_type="image/png"
        )
        
        response = self.client.post(url, {
            'original_file': test_file,
            'file_type': 'image'
        }, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SteganoFile.objects.count(), 1)

    def test_process_api(self):
        """Test file processing through API"""
        # Create test image
        img = Image.new('RGB', (100, 100), color='red')
        img_io = io.BytesIO()
        img.save(img_io, format='PNG')
        
        # Create file
        file = SteganoFile.objects.create(
            user=self.user,
            original_file=SimpleUploadedFile(
                'test.png',
                img_io.getvalue(),
                content_type='image/png'
            ),
            file_type='image'
        )
        
        url = reverse('api:steganofile-process', args=[file.id])
        
        response = self.client.post(url, {'message': 'test message'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        file.refresh_from_db()
        self.assertEqual(file.status, 'completed')

    def test_unauthorized_access(self):
        """Test unauthorized access to API"""
        # Clear any existing authentication
        self.client.force_authenticate(user=None)
        self.client.credentials()
        
        url = reverse('api:steganofile-list')
        response = self.client.get(url)
        
        # Should return 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Also test with invalid credentials
        self.client.credentials(HTTP_AUTHORIZATION='Basic invalid:credentials')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
