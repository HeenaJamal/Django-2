from rest_framework import serializers
from .models import User, FileUpload

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ['id', 'table_name', 'file']

##############################################################

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'password']  # Include the password field
        extra_kwargs = {'password': {'write_only': True}}  # Make password write-only

