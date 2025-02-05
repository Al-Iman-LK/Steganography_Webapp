import shutil
from django.test import TestCase
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from apps.core.models import SteganoFile
from apps.core.services.steganography.processor import SteganographyProcessor
from PIL import Image
import os
import io

class TestSteganography(TestCase):
    def setUp(self):
        # Create test media directory
        self.test_media = os.path.join(settings.MEDIA_ROOT, 'test')
        os.makedirs(self.test_media, exist_ok=True)

        # Create test user
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test image
        img = Image.new('RGB', (100, 100), color='red')
        img_io = io.BytesIO()
        img.save(img_io, format='PNG')

        # Create test file
        self.stegano_file = SteganoFile.objects.create(
            user=self.user,
            original_file=SimpleUploadedFile(
                name='test.png',
                content=img_io.getvalue(),
                content_type='image/png'
            ),
            file_type='image'
        )

    def tearDown(self):
        if hasattr(self, 'test_media') and os.path.exists(self.test_media):
            shutil.rmtree(self.test_media)

    def test_image_steganography(self):
        """Test basic image steganography functionality"""
        test_message = "Hello, World!"
        processor = SteganographyProcessor(self.stegano_file)
        processor.embed_message(test_message)
        
        self.assertEqual(self.stegano_file.status, 'completed')
        self.assertTrue(os.path.exists(self.stegano_file.processed_file.path))

    def test_large_message(self):
        """Test handling of messages that are too large"""
        large_message = "A" * 1000000  # Very large message
        processor = SteganographyProcessor(self.stegano_file)
        with self.assertRaises(ValueError):
            processor.embed_message(large_message)

    def test_invalid_file_type(self):
        """Test handling of unsupported file types"""
        test_file = SimpleUploadedFile(
            "test.txt",
            b"dummy text content",
            content_type="text/plain"
        )
        
        stegano_file = SteganoFile.objects.create(
            user=self.user,
            original_file=test_file,
            file_type='document'
        )
        
        processor = SteganographyProcessor(stegano_file)
        with self.assertRaises(ValueError) as context:
            processor.embed_message("test message")
        
        self.assertTrue("Unsupported file type" in str(context.exception))
        
        # Verify file status is set to failed
        stegano_file.refresh_from_db()
        self.assertEqual(stegano_file.status, 'failed')
