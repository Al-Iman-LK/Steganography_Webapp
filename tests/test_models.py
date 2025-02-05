from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.core.models import SteganoFile
from django.core.files.uploadedfile import SimpleUploadedFile

class ModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_stegano_file_creation(self):
        """Test SteganoFile model creation"""
        file = SteganoFile.objects.create(
            user=self.user,
            original_file='test.png',
            file_type='image',
            status='pending'
        )
        self.assertTrue(isinstance(file, SteganoFile))
        self.assertEqual(file.__str__(), f"image - testuser - pending")

    def test_auto_delete_flag(self):
        """Test auto_delete functionality"""
        file = SteganoFile.objects.create(
            user=self.user,
            original_file='test.png',
            file_type='image',
            auto_delete=True
        )
        self.assertTrue(file.auto_delete)

    def test_file_status_transitions(self):
        """Test file status transitions"""
        file = SteganoFile.objects.create(
            user=self.user,
            original_file='test.png',
            file_type='image'
        )
        
        self.assertEqual(file.status, 'pending')
        file.status = 'processing'
        file.save()
        self.assertEqual(file.status, 'processing')
        file.status = 'completed'
        file.save()
        self.assertEqual(file.status, 'completed')
