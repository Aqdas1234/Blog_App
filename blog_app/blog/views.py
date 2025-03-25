from django.contrib.auth import logout
from rest_framework import generics, permissions, status,filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
#from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .serializers import UserRegisterSerializer, BlogPostSerializer
from .models import BlogPost,BlogMedia
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.exceptions import PermissionDenied


# User Signup View
class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]  


# User Logout View

class UserLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"error": "Refresh token required."}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)

        except TokenError:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"Logout Error: {str(e)}")  # Debugging ke liye
            return Response({"error": "Something went wrong."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Pagination for Blog Posts
class BlogPagination(PageNumberPagination):
    page_size = 5  
    page_size_query_param = 'page_size'  
    max_page_size = 20  


# Blog Post List & Create View
class BlogPostCreateView(generics.CreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def validate_files(self, files):
        for file in files:
            if file.size > 10 * 1024 * 1024:  # 10MB limit
                raise ValidationError(f"File {file.name} exceeds the 10MB size limit.")
            if not file.content_type.startswith(("image", "video")):
                raise ValidationError(f"File {file.name} is not an image or video.")

    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('files')
        if files:  # Only validate if files exist
            try:
                self.validate_files(files)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        content = request.data.get("content")
        title = request.data.get("title")
        author = request.user

        blog_post = BlogPost.objects.create(title=title, content=content, author=author)

        for file in files:
            file_type = "image" if file.content_type.startswith("image") else "video"
            BlogMedia.objects.create(blog=blog_post, file=file, file_type=file_type)

        return Response({"message": "Blog Created Successfully!"}, status=status.HTTP_201_CREATED)


class BlogPostListView(generics.ListAPIView):
    queryset = BlogPost.objects.all().order_by('-created_at')
    serializer_class = BlogPostSerializer
    pagination_class = BlogPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']

# Retrieve, Update, Delete a Single Blog Post
class BlogPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]  # Anyone can view

    def perform_update(self, serializer):
        if self.request.user != self.get_object().author:
            raise PermissionDenied("You are not allowed to edit this post.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
           raise PermissionDenied("You are not allowed to delete this post.")
        instance.delete()
