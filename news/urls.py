from django.urls import path
from . import views

app_name = "news"
urlpatterns = [
    path("", views.index, name="index"),
    path("lazy_load_stories/", views.lazy_load_stories, name="lazy_load_stories"),
]
