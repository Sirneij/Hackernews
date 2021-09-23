from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from news.models import LatestStory, Comment
from .serializers import LatestStorySerializer


@api_view(["GET", "POST"])
def latest_stories_list(request, format=None):
    """
    List all code latest news, or create a new story.
    """
    if request.method == "GET":
        stories = LatestStory.objects.all()
        serializer = LatestStorySerializer(stories, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = LatestStorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def story_detail(request, pk, format=None):
    """
    Retrieve, update or delete a story.
    """
    try:
        story = LatestStory.objects.get(pk=pk)
    except LatestStory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = LatestStorySerializer(story)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = LatestStorySerializer(story, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        story.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
