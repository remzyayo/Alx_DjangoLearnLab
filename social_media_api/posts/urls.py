from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PostViewSet, CommentViewSet, FeedListView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

app_name = 'posts'
urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedListView.as_view(), name='feed'),
]