from news.models import LatestStory, Comment
from rest_framework import serializers


class LatestStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LatestStory
        fields = "__all__"
