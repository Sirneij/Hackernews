from django.contrib import admin
from .models import LatestStory, Comment


@admin.register(LatestStory)
class LatestStoryAdmin(admin.ModelAdmin):
    list_display = ["unique_api_story_id", "story_type", "author", "title", "story_url"]
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ["title", "story_type", "author", "created_by"]
    list_per_page = 20


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["unique_comment_api_id", "author", "title", "comment_url"]
    list_per_page = 20
