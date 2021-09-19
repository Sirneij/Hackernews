from django.http import response
from django.shortcuts import render
import requests

BASE_API_URL = "https://hacker-news.firebaseio.com/v0"


def get_story(id):
    try:
        story = requests.get(f"{BASE_API_URL}/item/{id}.json")
        return story.json()
    except:
        print("Error while getting a story.")


def get_stories(type):
    try:
        story_ids = requests.get(f"{BASE_API_URL}/{type}stories.json").json()
        stories = []
        for sid in story_ids:
            story_response = get_story(sid)
            stories.append(story_response)
        return stories
    except:
        print("Error while getting list of stories.")


import json


def index(request):
    # # response = get_story("8861")
    # # response = requests.get(f"{BASE_API_URL}/newstories.json").json()
    # response = get_stories("new")
    # with open("data.json", "w") as outfile:
    #     json.dump(response, outfile)
    # # print(response)
    context = {"page_title": "Welcome to a Beautiful Hackernews clone"}
    return render(request, "news/index.html", context)
