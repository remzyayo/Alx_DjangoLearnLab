from django.urls import path
from .views import RegisterView, LoginView, ProfileView
from . import views
from .views import FollowUserView, UnfollowUserView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile-detail'),
    path("follow/<int:user_id>/", FollowUserView.as_view(), name='follow-user'),
    path("unfollow/<int:user_id>/", UnfollowUserView.as_view(), name='unfollow-user'),
]