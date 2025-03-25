from django.contrib import admin
from .models import BlogPost,BlogMedia
'''
class BlogMediaInline(admin.TabularInline):  # Allows inline media uploads
    model = BlogMedia
    extra = 1  # Number of empty file fields shown
'''
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'author__username','content')
    list_filter = ('created_at',)
    #inlines = [BlogMediaInline]  # Allows media to be managed inline

@admin.register(BlogMedia)
class BlogMediaAdmin(admin.ModelAdmin):
    list_display = ('blog', 'file')

