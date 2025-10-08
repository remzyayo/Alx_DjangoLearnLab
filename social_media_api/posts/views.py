from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like
from .serializers import PostListSerializer, PostDetailSerializer, CommentSerializer, PostSerializer, LikeSerializer
from .permissions import IsOwnerOrReadOnly
from .pagination import StandardResultsSetPagination
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification

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
    queryset = Comment.objects.all()
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
    

class FeedListView(generics.ListAPIView):
    """
    Returns posts authored by users the current user follows.
    Ordered newest first.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None  # or your pagination

    def get_queryset(self):
        user = self.request.user
        # posts from users the current user follows
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by
    

class LikePostView(generics.GenericAPIView):
    """
    Authenticated user likes a post.
    """
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Like.objects.all()

    def post(self, request, pk):
        user = request.user
        post = generics.get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        

        # prevent liking own post is allowed; but prevent duplicate likes
        existing = Like.objects.filter(user=user, post=post).first()
        if existing:
            return Response({'detail': 'Post already liked.'}, status=status.HTTP_200_OK)

        like = Like.objects.create(user=user, post=post)

        # create notification for post author (if not liking own post)
        if post.author != user:
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb='liked your post',
                target_content_type=ContentType.objects.get_for_model(post),
                target_object_id=str(post.pk)
            )

        serializer = self.get_serializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UnlikePostView(generics.GenericAPIView):
    """
    Authenticated user unlikes a post.
    """
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Like.objects.all()

    def post(self, request, pk):
        user = request.user
        post = get_object_or_404(Post, pk=pk)

        like_qs = Like.objects.filter(user=user, post=post)
        if not like_qs.exists():
            return Response({'detail': 'You have not liked this post.'}, status=status.HTTP_200_OK)

        like_qs.delete()
        # Optionally mark related notifications as read or remove them
        # find notifications matching this action; this is a best-effort match
        try:
            ct = ContentType.objects.get_for_model(post)
            Notification.objects.filter(
                recipient=post.author,
                actor=user,
                verb='liked your post',
                target_content_type=ct,
                target_object_id=str(post.pk)
            ).delete()
        except Exception:
            pass

        return Response({'detail': 'Post unliked.'}, status=status.HTTP_200_OK)