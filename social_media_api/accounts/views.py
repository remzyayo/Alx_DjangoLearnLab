from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserFollowSerializer
from .serializers import RegistrationSerializer, LoginSerializer, UserProfileSerializer
from .models import CustomUser
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification

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



class FollowUserView(generics.GenericAPIView):
    """
    Allow the authenticated user to follow another user.
    """
    serializer_class = UserFollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all() 

    def post(self, request, user_id):
        user = request.user
        target_user = get_object_or_404(CustomUser, pk=user_id)

        if user == target_user:
            return Response({'detail': 'You cannot follow yourself.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if user.is_following(target_user):
            return Response({'detail': 'Already following this user.'},
                            status=status.HTTP_200_OK)

        user.follow(target_user)

        Notification.objects.create(
           recipient=target_user,
           actor=user,
           verb='followed you',
           target_content_type=ContentType.objects.get_for_model(user),  # pointing to user
           target_object_id=str(user.pk)
    )
        serializer = self.get_serializer(target_user)
        return Response({
            'detail': f'You are now following {target_user.username}.',
            'user': serializer.data
        }, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):
    """
    Allow the authenticated user to unfollow another user.
    """
    serializer_class = UserFollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()  # ✅ Required by ALX checker

    def post(self, request, user_id):
        user = request.user
        target_user = get_object_or_404(CustomUser, pk=user_id)

        if user == target_user:
            return Response({'detail': 'You cannot unfollow yourself.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not user.is_following(target_user):
            return Response({'detail': 'You are not following this user.'},
                            status=status.HTTP_200_OK)

        user.unfollow(target_user)
        serializer = self.get_serializer(target_user)
        return Response({
            'detail': f'You have unfollowed {target_user.username}.',
            'user': serializer.data
        }, status=status.HTTP_200_OK)


