from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404

from .serializers import RegistrationSerializer, LoginSerializer, UserProfileSerializer
from .models import CustomUser

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # serializer.create attached token as attribute on user
            token = Token.objects.get(user=user)
            data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "token": token.key
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username=None):
        """
        If username provided -> fetch that user's profile
        If not provided -> return request.user's profile
        """
        if username:
            user = get_object_or_404(CustomUser, username=username)
        else:
            user = request.user
        serializer = UserProfileSerializer(user, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        """
        Update request.user profile (partial fields allowed).
        """
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)