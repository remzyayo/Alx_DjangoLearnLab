from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, CommentCreateView, CommentUpdateView, CommentDeleteView

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),

    # Login & Logout
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),

    # Profile
    path("post/", PostListView.as_view(), name='posts-list'),
    path("post/new/", PostCreateView.as_view(), name='posts-create'),
    path("post/<int:pk>/", PostDetailView.as_view(), name='posts-detail'),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name='posts-update'),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name='posts-delete'),

    # comment urls
    path("post/<int:pk>/comment/new/", CommentCreateView.as_view(), name="comment-create"),
    path("comment/<int:pk>/update/", CommentUpdateView.as_view(), name="comment-update"),
    path("comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"),

]