from rest_framework import viewsets, status, permissions, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
import logging
from ..core.models import SteganoFile
from ..core.services.steganography.processor import SteganographyProcessor
from ..core.services.steganography.extractor import SteganographyExtractor  # Add this import
from .serializers import SteganoFileSerializer, UserProfileSerializer

logger = logging.getLogger(__name__)

class SteganoFileViewSet(viewsets.ModelViewSet):
    serializer_class = SteganoFileSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return SteganoFile.objects.none()
        return SteganoFile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Handle file creation with upload purpose"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        instance = serializer.save(user=self.request.user)
        
        # Check if this is an upload for extraction
        is_for_extraction = request.data.get('for_extraction', False)
        
        if is_for_extraction:
            # Set the processed file same as original for extraction
            instance.status = 'completed'
            instance.processed_file = instance.original_file
            instance.save()
            
            # Return success with file ID
            data = serializer.data
            data['id'] = instance.id  # Make sure ID is included for extraction
            headers = self.get_success_headers(serializer.data)
            return Response(data, status=status.HTTP_201_CREATED, headers=headers)
        
        # Normal upload for embedding
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        data['next'] = f'/process/{instance.id}/'
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        stegano_file = self.get_object()
        message = request.data.get('message')
        
        if not message:
            return Response(
                {'error': 'Message is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            processor = SteganographyProcessor(stegano_file)
            processor.embed_message(message)
            serializer = self.get_serializer(stegano_file)
            return Response(serializer.data)
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValueError as e:
            logger.error(f"Processing error: {str(e)}")
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response(
                {'error': 'Internal server error'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def extract(self, request, pk=None):
        stegano_file = self.get_object()
        
        try:
            extractor = SteganographyExtractor(stegano_file)
            message = extractor.extract_message()
            return Response({
                'status': 'success',
                'message': message
            })
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    def permission_denied(self, request, message=None, code=None):
        if request.authenticators and not request.successful_authenticator:
            raise exceptions.NotAuthenticated()
        raise exceptions.PermissionDenied(message)

    def handle_exception(self, exc):
        if isinstance(exc, (exceptions.NotAuthenticated, exceptions.AuthenticationFailed)):
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return super().handle_exception(exc)

class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        return [self.request.user.profile]
