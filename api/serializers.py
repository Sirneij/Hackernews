from news.models import LatestStory, Comment
from django.contrib.auth import get_user_model
from rest_framework import serializers


class LatestStorySerializer(serializers.HyperlinkedModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")
    author = serializers.ReadOnlyField()
    score = serializers.ReadOnlyField()
    descendants = serializers.ReadOnlyField()
    time = serializers.ReadOnlyField()
    slug = serializers.ReadOnlyField()

    class Meta:
        model = LatestStory
        fields = [
            "url",
            "id",
            "title",
            "story_type",
            "author",
            "slug",
            "created_by",
            "time",
            "text",
            "dead",
            "story_url",
            "score",
            "descendants",
        ]


class UserSerializer(serializers.ModelSerializer):
    stories = serializers.HyperlinkedRelatedField(many=True, view_name="user-detail", read_only=True)

    class Meta:
        model = get_user_model()
        fields = ["url", "id", "username", "stories"]
