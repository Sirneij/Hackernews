import dateutil.parser
import datetime
import requests
from celery import shared_task
from django.template.defaultfilters import slugify
from .models import LatestStory, Comment
import pytz

BASE_API_URL = "https://hacker-news.firebaseio.com/v0"


def get_item(id):
    item = requests.get(f"{BASE_API_URL}/item/{id}.json")
    return item.json()


@shared_task
def get_and_store_story_comments(unique_api_story_id, story_id):
    single_story = get_item(unique_api_story_id)
    for kid in single_story.get("kids", []):
        comment_response = get_item(kid)
        comment, _ = Comment.objects.get_or_create(unique_comment_api_id=kid, story=LatestStory.objects.get(id=story_id))
        comment.story_type = comment_response.get("type", "")
        comment.author = comment_response.get("by", "")
        comment.time = dateutil.parser.parse(
            datetime.datetime.fromtimestamp(comment_response.get("time", 0)).strftime("%Y-%m-%d %H:%M:%S")
        )
        comment.text = comment_response.get("text", "")
        comment.comment_url = comment_response.get("url", "")
        comment.score = comment_response.get("score", 0)
        comment.save()


@shared_task
def store_latest_stories(type):
    story_ids = requests.get(f"{BASE_API_URL}/{type}stories.json").json()
    for sid in story_ids:
        story_response = get_item(sid)
        story, _ = LatestStory.objects.get_or_create(
            unique_api_story_id=sid, title=story_response.get("title", "No title for this story from the API")
        )
        story.story_type = story_response.get("type", "No type")
        story.author = story_response.get("by", "No creator")
        story.time = dateutil.parser.parse(
            datetime.datetime.fromtimestamp(story_response.get("time", 0)).strftime("%Y-%m-%d %H:%M:%S")
        )
        story.slug = slugify(story_response.get("title", "No title for this story from the API"))
        story.story_url = story_response.get("url", "")
        story.score = story_response.get("score", 0)
        story.descendants = story_response.get("descendants", 0)
        story.save()
        get_and_store_story_comments.delay(story.unique_api_story_id, story.id)


@shared_task
def get_latest_stories():
    store_latest_stories.delay("new")
