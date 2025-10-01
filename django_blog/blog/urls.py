from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),

    # Login & Logout
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),

    # Profile
    path("posts/", PostListView.as_view(), name='posts-list'),
    path("posts/new/", PostCreateView.as_view(), name='posts-create'),
    path("posts/<int:pk>/", PostDetailView.as_view(), name='posts-detail'),
    path("posts/<int:pk>/update/", PostUpdateView.as_view(), name='posts-update'),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view(), name='posts-delete'),
]