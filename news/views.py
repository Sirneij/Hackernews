from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from .models import LatestStory, Comment


def index(request):
    stories = LatestStory.objects.all().order_by("-time")[:4]
    story_types = ["job", "story", "comment", "poll", "pollopt"]
    context = {"page_title": "Welcome to a Beautiful Hackernews clone", "stories": stories, "story_types": story_types}
    return render(request, "news/index.html", context)


def story_detail(request, id, slug):
    story = get_object_or_404(LatestStory, id=id, slug=slug)
    context = {"page_title": f"{story.title}", "story": story}
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


def filter_by_story_type(request):
    if request.method == "POST":
        story_type = request.POST.get("story_type")
        print(story_type)
        stories = LatestStory.objects.filter(story_type=story_type).order_by("-time")
        if stories.exists():
            page = request.POST.get("page")
            results_per_page = 4
            paginator = Paginator(stories, results_per_page)
            try:
                stories = paginator.page(page)
            except PageNotAnInteger:
                stories = paginator.page(1)
            except EmptyPage:
                stories = paginator.page(paginator.num_pages)
            stories_html = loader.render_to_string("news/stories.html", {"stories": stories})

            output_data = {
                "stories_html": stories_html,
                "has_next": stories.has_next(),
                "stories_count": len(stories),
            }
            return JsonResponse(output_data)
        else:
            return JsonResponse({"no_story": True})
    elif request.method == "GET":
        story_type = request.GET.get("story_type")
        stories = LatestStory.objects.filter(story_type=story_type).order_by("-time")
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

            output_data = {
                "stories_html": stories_html,
                "has_next": stories.has_next(),
                "stories_count": len(stories),
            }
            return JsonResponse(output_data)


def search_by_text(request):
    search_text = request.POST.get("search_text")
    stories = LatestStory.objects.filter(title__icontains=search_text)
    if len(stories) > 0:
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
    else:
        return JsonResponse({"no_story": True})
