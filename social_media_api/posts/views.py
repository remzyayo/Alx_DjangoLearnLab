from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from .serializers import PostListSerializer, PostDetailSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from .pagination import StandardResultsSetPagination

class PostViewSet(viewsets.ModelViewSet):
    """
    CRUD for Post.
    - List & retrieve: anyone (depending on default permission; typically allow any for read)
    - Create: authenticated
    - Update/Delete: owner only
    """
    queryset = Post.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']

    def get_permissions(self):
        # Allow read-only for any, write for authenticated users and owners for updates/deletes
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        elif self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsOwnerOrReadOnly()]

    def get_serializer_class(self):
        if self.action in ['list']:
            return PostListSerializer
        return PostDetailSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD for Comment.
    - Comments are created with an associated post (post provided in payload or via nested route)
    - Only the comment author can update/delete their comment.
    """
    queryset = Comment.objects.all
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content']
    ordering_fields = ['created_at', 'updated_at']

    def perform_create(self, serializer):
        # Expect 'post' id in the request data, or fail with 400
        post = None
        post_id = self.request.data.get('post')
        if not post_id:
            raise serializer.ValidationError({'post': 'This field is required.'})
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsOwnerOrReadOnly()]