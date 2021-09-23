from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = "api"
urlpatterns = [
    path("latest-stories/", views.latest_stories_list, name="latest_stories_list"),
    path("latest/<pk>", views.story_detail, name="story_detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
