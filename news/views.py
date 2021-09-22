from django.shortcuts import render
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from .models import LatestStory, Comment


def index(request):
    stories = LatestStory.objects.all()[:6]
    context = {"page_title": "Welcome to a Beautiful Hackernews clone", "stories": stories}
    return render(request, "news/index.html", context)


def lazy_load_stories(request):
    page = request.POST.get("page")
    stories = LatestStory.objects.all()
    # use Django's pagination
    # https://docs.djangoproject.com/en/dev/topics/pagination/
    results_per_page = 6
    paginator = Paginator(stories, results_per_page)
    try:
        stories = paginator.page(page)
    except PageNotAnInteger:
        stories = paginator.page(2)
    except EmptyPage:
        stories = paginator.page(paginator.num_pages)
    # build a html stories list with the paginated stories
    stories_html = loader.render_to_string("news/stories.html", {"stories": stories})
    # package output data and return it as a JSON object
    output_data = {"stories_html": stories_html, "has_next": stories.has_next(), "stories_count": len(stories)}
    return JsonResponse(output_data)
