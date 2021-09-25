from news.models import LatestStory, Comment
from django import template

register = template.Library()

@register.filter
def story_title(id):
    comm = Comment.objects.select_related('story').get(id=id)
    if comm:
        return comm.story.title
