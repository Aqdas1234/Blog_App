from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BlogPost,BlogMedia
from rest_framework.validators import UniqueValidator


# User Registration Serializer
class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="Email already exists.")]
    )
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')  
        password = validated_data.pop('password')  
        user = User(**validated_data)  
        user.set_password(password)  
        user.save()
        return user


# Blog Media Serializer
class BlogMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogMedia
        fields = ['id', 'file', 'file_type']


# Blog Post Serializer (for Viewing)
class BlogPostSerializer(serializers.ModelSerializer):
    
    author = serializers.ReadOnlyField(source='author.username')
    media = BlogMediaSerializer(many=True, read_only=True)  # Show media files

    class Meta:
        model = BlogPost
        fields = ['id', 'author', 'title', 'media','content', 'created_at']
    
    def validate_title(self, value):
        """Ensure title is unique only when creating a new blog post."""
        if BlogPost.objects.exclude(pk=self.instance.pk if self.instance else None).filter(title=value).exists():
            raise serializers.ValidationError("A blog post with this title already exists.")
        return value

    def create(self, validated_data):
        request = self.context.get('request')  # Get request object
        blog_post = BlogPost.objects.create(**validated_data)

        files = request.FILES.getlist('files') if request and hasattr(request, 'FILES') else []
        for file in files:
            file_type = "image" if file.content_type.startswith("image") else "video"
            BlogMedia.objects.create(blog=blog_post, file=file, file_type=file_type)

        return blog_post


"""
# Blog Post Create Serializer (for Creating a Post)
class BlogPostCreateSerializer(serializers.ModelSerializer):
    '''
    media = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,  # Media is required only when creating a post
        required=False
    )
    '''
    author = serializers.ReadOnlyField(source='author.username')  # Prevent author override

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'author']

    def create(self, validated_data):
        #media_files = validated_data.pop('media', [])
        blog = BlogPost.objects.create(**validated_data)
        '''
        # Save all media files
        for file in media_files:
            BlogMedia.objects.create(blog=blog, file=file)
        '''
        return blog
"""