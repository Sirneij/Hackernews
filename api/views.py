from news.models import LatestStory, Comment
from .serializers import LatestStorySerializer
from rest_framework import generics


class StoryList(generics.ListCreateAPIView):
    queryset = LatestStory.objects.all()
    serializer_class = LatestStorySerializer


class StoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LatestStory.objects.all()
    serializer_class = LatestStorySerializer
