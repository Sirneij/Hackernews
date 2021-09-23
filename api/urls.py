from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = "api"
urlpatterns = [
    path("latest-stories/", views.StoryList.as_view(), name="latest_stories_list"),
    path("latest/<uuid:pk>/", views.StoryDetail.as_view(), name="story_detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
