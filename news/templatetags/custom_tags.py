from news.models import Comment, LatestStory
from django import template

register = template.Library()


@register.filter
def story_title(parent_id):
    comm = LatestStory.objects.filter(unique_api_story_id=parent_id).first()
    if comm:
        if comm.story_type == "comment":
            comm2 = LatestStory.objects.filter(unique_api_story_id=comm.parent_id).first()
            if comm2:
                return comm2.title
        return comm.title
    else:
        return "Parent story has not been fetched yet"


@register.filter
def story_url(parent_id):
    comm = LatestStory.objects.filter(unique_api_story_id=parent_id).first()
    if comm:
        if comm.story_type == "comment":
            comm2 = LatestStory.objects.filter(unique_api_story_id=comm.parent_id).first()
            if comm2:
                return comm2.get_absolute_url()
        return comm.get_absolute_url()
    else:
        return "#"
