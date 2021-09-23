from django.urls import path
from . import views

app_name = "news"
urlpatterns = [
    path("", views.index, name="index"),
    path("lazy_load_stories/", views.lazy_load_stories, name="lazy_load_stories"),
    path("filter_by_story_type/", views.filter_by_story_type, name="filter_by_story_type"),
    path("search_by_text/", views.search_by_text, name="search_by_text"),
    path("story-detail/<uuid:id>/<slug:slug>/", views.story_detail, name="story_detail"),
]
