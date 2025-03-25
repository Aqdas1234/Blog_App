from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegisterView, UserLogoutView,BlogPostDetailView,BlogPostCreateView,BlogPostListView

urlpatterns = [
    path('signup/', UserRegisterView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),  # JWT Login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('blogs/create', BlogPostCreateView.as_view(), name='blog-create'),
    path('blogs/', BlogPostListView.as_view(), name='blog-list'),
    
    path('blogs/<int:pk>/', BlogPostDetailView.as_view(), name='blog-detail'),
]
