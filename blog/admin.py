from django.contrib import admin

# Register your models here.
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_date', 'post']

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
