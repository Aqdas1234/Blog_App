from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field

class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = CKEditor5Field("Content", config_name="default") 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class BlogMedia(models.Model):
    FILE_TYPE_CHOICES = [
        ("image", "Image"),
        ("video", "Video"),
    ]
    
    blog = models.ForeignKey(BlogPost, related_name="media", on_delete=models.CASCADE)
    file = models.FileField(upload_to="blog_media/")
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES,default='image')

    def __str__(self):
        return f"{self.blog.title} - {self.file_type}"
