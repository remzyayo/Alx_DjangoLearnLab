from rest_framework import serializers
from django.conf import settings
from .models import Post, Comment, Like
from django.contrib.auth import get_user_model
from accounts.serializers import UserFollowSerializer

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    post_id = serializers.IntegerField(source='post.id', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post_id', 'author', 'content', 'created_at', 'updated_at']

class PostListSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'content', 'comments_count', 'created_at', 'updated_at']

    def get_comments_count(self, obj):
        return obj.comments.count()

class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'content', 'comments', 'created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    author = UserFollowSerializer(read_only=True)  # compact author info
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'created_at']  # adapt to your fields
        read_only_fields = ['id', 'author', 'created_at', 'likes_count']

        
class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class LikeSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ('id', 'user', 'post', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')