from rest_framework import serializers
from apps.core.models import SteganoFile
from apps.users.models import UserProfile

class SteganoFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SteganoFile
        fields = ['id', 'original_file', 'processed_file', 'file_type', 
                 'status', 'created_at', 'auto_delete']
        read_only_fields = ['processed_file', 'status', 'created_at']

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'avatar', 'total_files_processed', 
                 'storage_used', 'created_at']
        read_only_fields = ['total_files_processed', 'storage_used', 'created_at']
