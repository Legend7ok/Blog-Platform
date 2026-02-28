from django.contrib import admin
from .models import Post, Comment
from django.utils.html import format_html

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status', 'image_preview']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', '-publish']
    list_select_related = ['author']

    @admin.display(description='image')
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" />', obj.image.url)
        return "-"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
    list_select_related = ['post']
