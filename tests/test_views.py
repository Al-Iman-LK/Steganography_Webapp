from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.core.models import SteganoFile
from PIL import Image
import io

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_upload_view(self):
        """Test file upload view"""
        url = reverse('core:upload_file')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Test file upload
        test_file = SimpleUploadedFile(
            "test.png",
            b"file_content",
            content_type="image/png"
        )
        response = self.client.post(url, {
            'original_file': test_file,
            'file_type': 'image'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(SteganoFile.objects.exists())

    def test_process_view(self):
        """Test file processing view"""
        # Create a valid test image
        img = Image.new('RGB', (100, 100), color='red')
        img_io = io.BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)

        file = SteganoFile.objects.create(
            user=self.user,
            original_file=SimpleUploadedFile(
                'test.png',
                img_io.getvalue(),
                content_type='image/png'
            ),
            file_type='image'
        )
        
        url = reverse('core:process_file', args=[file.id])
        response = self.client.post(url, {'message': 'test message'})
        
        self.assertEqual(response.status_code, 302)  # Check redirection
        file.refresh_from_db()
        self.assertEqual(file.status, 'completed')
