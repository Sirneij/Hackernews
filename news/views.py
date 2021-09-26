from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from .models import Comment, LatestStory
from . import utils


def index(request):
    stories = LatestStory.objects.all().order_by("-time")[:4]
    types = LatestStory.objects.order_by("-story_type").values_list("story_type")
    story_types = []
    for t in types:
        if t[0] in story_types:
            continue
        story_types.append(t[0])
    context = {"page_title": "Welcome to a Beautiful Hackernews clone", "stories": stories, "story_types": story_types}
    return render(request, "news/index.html", context)


def story_detail(request, id, slug):
    story = get_object_or_404(LatestStory, id=id, slug=slug)
    comments_by_parent_id = LatestStory.objects.filter(unique_api_story_id=story.parent_id)
    comments_normally = Comment.objects.select_related("story").filter(story=story)
    from itertools import chain

    story_comments = list(chain(comments_by_parent_id, comments_normally))
    context = {
        "page_title": f"{story.title}",
        "story": story,
        "story_comments": story_comments,
    }
    return render(request, "news/detail.html", context)


def lazy_load_stories(request):
    stories = LatestStory.objects.all().order_by("-time")
    """
    Exposes data for easy lazy-loading at the frontend to increase system performance.

    Pagination is highly influenced by https://docs.djangoproject.com/en/dev/topics/pagination/
    """
    page = request.POST.get("page")
    results_per_page = 4
    paginator = Paginator(stories, results_per_page)
    try:
        stories = paginator.page(page)
    except PageNotAnInteger:
        stories = paginator.page(2)
    except EmptyPage:
        stories = paginator.page(paginator.num_pages)
    stories_html = loader.render_to_string("news/stories.html", {"stories": stories})
    output_data = {
        "stories_html": stories_html,
        "has_next": stories.has_next(),
        "stories_count": len(stories),
    }
    return JsonResponse(output_data)


def search_by_text(request):
    if request.method == "POST":
        search_text = request.POST.get("search_text")
        stories = utils.stories(search_text).get("stories", [])
        if len(stories) > 4:
            page = request.POST.get("page")
            results_per_page = 4
            paginator = Paginator(stories, results_per_page)
            try:
                stories = paginator.page(page)
            except PageNotAnInteger:
                stories = paginator.page(2)
            except EmptyPage:
                stories = paginator.page(paginator.num_pages)
            stories_html = loader.render_to_string("news/stories.html", {"stories": stories})
            stories_list = []
            for i in stories:
                stories_list.append({"title": i.title, "author": i.author, "story_type": i.story_type, "text": i.text})
            output_data = {
                "stories_html": stories_html,
                "has_next": stories.has_next(),
                "stories_count": len(stories),
                # "real_stories": stories_list,
            }
            return JsonResponse(output_data)
        elif len(stories) < 4 and len(stories) > 0:
            stories_html = loader.render_to_string("news/stories.html", {"stories": stories})
            stories_list = []
            for i in stories:
                stories_list.append({"title": i.title, "author": i.author, "story_type": i.story_type, "text": i.text})
            output_data = {
                "stories_html": stories_html,
                "has_next": False,
                "stories_count": len(stories),
                # "real_stories": stories_list,
            }
            return JsonResponse(output_data)
        else:
            return JsonResponse({"no_story": True})
    if request.method == "GET":
        search_text = request.GET.get("search_text")
        stories = utils.stories(search_text).get("stories", [])
        if len(stories) > 4:
            page = request.GET.get("page")
            results_per_page = 4
            paginator = Paginator(stories, results_per_page)
            try:
                stories = paginator.page(page)
            except PageNotAnInteger:
                stories = paginator.page(1)
            except EmptyPage:
                stories = paginator.page(paginator.num_pages)
            stories_html = loader.render_to_string("news/stories.html", {"stories": stories})
            stories_list = []
            for i in stories:
                stories_list.append({"title": i.title, "author": i.author, "story_type": i.story_type, "text": i.text})
            output_data = {
                "stories_html": stories_html,
                "has_next": stories.has_next(),
                "stories_count": len(stories),
                # "real_stories": stories_list,
            }
            return JsonResponse(output_data)
        elif len(stories) < 4 and len(stories) > 0:
            stories_html = loader.render_to_string("news/stories.html", {"stories": stories})
            stories_list = []
            for i in stories:
                stories_list.append({"title": i.title, "author": i.author, "story_type": i.story_type, "text": i.text})
            output_data = {
                "stories_html": stories_html,
                "has_next": False,
                "stories_count": len(stories),
                # "real_stories": stories_list,
            }
            return JsonResponse(output_data)
        else:
            return JsonResponse({"no_story": True})


def filter_by_story_type(request):
    if request.method == "POST":
        story_type = request.POST["story_type"]
        stories = LatestStory.objects.filter(story_type=story_type).order_by("-time")
        if len(stories) > 4:
            page = request.POST.get("page")
            results_per_page = 4
            paginator = Paginator(stories, results_per_page)
            try:
                stories = paginator.page(page)
            except PageNotAnInteger:
                stories = paginator.page(2)
            except EmptyPage:
                stories = paginator.page(paginator.num_pages)
            stories_html = loader.render_to_string("news/stories.html", {"stories": stories})
            output_data = {
                "stories_html": stories_html,
                "has_next": stories.has_next(),
                "stories_count": len(stories),
            }
            return JsonResponse(output_data)
        elif len(stories) < 4 and len(stories) > 0:
            stories_html = loader.render_to_string("news/stories.html", {"stories": stories})
            output_data = {
                "stories_html": stories_html,
                "has_next": False,
                "stories_count": len(stories),
            }
            return JsonResponse(output_data)
        else:
            return JsonResponse({"no_story": True})
    elif request.method == "GET":
        story_type = request.GET["story_type"]
        stories = LatestStory.objects.filter(story_type=story_type).order_by("-time")
        if len(stories) > 4:
            paginator = Paginator(stories, 4)
            page = request.GET.get("page")
            try:
                stories = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer deliver the first page
                stories = paginator.page(1)
            except EmptyPage:
                stories = paginator.page(paginator.num_pages)
            newstories_html = loader.render_to_string("news/stories.html", {"stories": stories})
            output_data = {
                "newstories_html": newstories_html,
                "newhas_next": stories.has_next(),
                "newstories_count": len(stories),
            }
            return JsonResponse(output_data)
        elif len(stories) < 4 and len(stories) > 0:
            newstories_html = loader.render_to_string("news/stories.html", {"stories": stories})
            output_data = {
                "newstories_html": newstories_html,
                "newhas_next": False,
                "newstories_count": len(stories),
            }
            return JsonResponse(output_data)
        else:
            return JsonResponse({"no_story": True})
