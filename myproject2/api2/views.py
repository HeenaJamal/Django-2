from rest_framework.generics import RetrieveAPIView, ListAPIView, UpdateAPIView                   # type: ignore
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView                                                          # type: ignore
from rest_framework.response import Response                                                       # type: ignore
from rest_framework import status                                                                      # type: ignore
from .models import User, FileUpload
from .serializers import UserSerializer, FileUploadSerializer
import csv
import os
from django.db import connection                                      # type: ignore

import jwt
import datetime
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from .serializers import UserSerializer
from .models import User

# Secret Key for signing JWT (you can use Django's SECRET_KEY)
SECRET_KEY = settings.SECRET_KEY

# Generate JWT Token function
def generate_jwt_token(user):
    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),  # Token expires in 24 hours
        'iat': datetime.datetime.utcnow(),  # Issued at
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


# Signup API
class SignupView(APIView):
    def post(self, request):
        data = request.data
        data['password'] = make_password(data['password'])  # Hash the password
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login API with JWT Token
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Find user by email
        user = User.objects.filter(email=email).first()

        # Verify the password
        if user and check_password(password, user.password):
            # Generate JWT Token
            token = generate_jwt_token(user)
            return Response({
                "message": "Login successful",
                "token": token
            }, status=status.HTTP_200_OK)

        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


"""
class SignupView(APIView):
    def post(self, request):
        data = request.data
        data['password'] = make_password(data['password'])  # Hash the password
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update LoginView to check both email and password
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()

        if user and check_password(password, user.password):  # Verify the password
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
"""

# View user by ID
class UserDetailView(APIView):
    def post(self, request):
        user_id = request.data.get('id')
        if not user_id:
            return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

# List all users
class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Update user
class UserUpdateView(APIView):
    def put(self, request):
        user_id = request.data.get('id')
        if not user_id:
            return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class FileUploadView(APIView):
    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            file_path = serializer.instance.file.path
            table_name = serializer.instance.table_name
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                header = next(reader)
                with connection.cursor() as cursor:
                    # Create the table with `table_<10-digit random number>`
                    create_table_query = f"CREATE TABLE `{table_name}` ({', '.join([f'`{col}` TEXT' for col in header])})"
                    cursor.execute(create_table_query)
                    # Insert rows from CSV into the table
                    for row in reader:
                        cursor.execute(f"INSERT INTO `{table_name}` VALUES ({', '.join(['%s' for _ in row])})", row)
            return Response({"table_name": table_name}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
