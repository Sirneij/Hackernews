from django.contrib import admin
from .models import LatestStory, Comment


@admin.register(LatestStory)
class LatestStoryAdmin(admin.ModelAdmin):
    list_display = ["unique_api_story_id", "story_type", "author", "title", "url"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["unique_comment_api_id", "author", "title", "url"]
