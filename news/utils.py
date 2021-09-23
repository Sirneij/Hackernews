from django.db.models import Q

from .models import LatestStory

STRIP_WORDS = ["a", "an", "and", "by", "for", "from", "in", "no", "not", "of", "on", "or", "that", "the", "to", "with"]


def stories(search_text):
    words = _prepare_words(search_text)
    stories = LatestStory.objects.all()
    results = {}
    results["stories"] = []
    # iterate through keywords
    for word in words:
        stories = stories.filter(
            Q(title__icontains=word) | Q(story_type__iexact=word) | Q(author__iexact=word) | Q(text__icontains=word)
        ).order_by("-time")
        results["stories"] = stories
    return results


def _prepare_words(search_text):
    """strip out common words, limit to 5 words"""
    words = search_text.split()
    for common in STRIP_WORDS:
        if common in words:
            words.remove(common)
    return words[0:100]
