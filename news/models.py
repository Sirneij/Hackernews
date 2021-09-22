from django.db import models
from django.urls import reverse


class Story(models.Model):
    unique_api_story_id = models.CharField("Story ID from the API", max_length=10, null=True)
    story_type = models.CharField(
        "Type of item One of 'job, 'story', 'comment', 'poll', or 'pollopt'", max_length=15, null=True
    )
    author = models.CharField("Name of the author", max_length=50, null=True)
    time = models.DateTimeField("Creation date of the item", null=True)
    text = models.TextField("The comment, story or poll text.", null=True)
    dead = models.BooleanField(default=False)
    url = models.CharField("The URL of the story.", max_length=550, null=True)
    score = models.CharField("The story's score, or the votes for a pollopt.", max_length=10, null=True)
    title = models.CharField("The title of the story, poll or job. HTML.", max_length=500, null=True)

    class Meta:
        verbose_name = "Story"
        verbose_name_plural = "Stories"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news-detail", kwargs={"id": self.id})


class Comment(models.Model):
    unique_comment_api_id = models.CharField("Story ID from the API", max_length=10, null=True)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="comments")
    author = models.CharField("Name of the author", max_length=50, null=True)
    time = models.DateTimeField("Creation date of the item", null=True)
    text = models.TextField("The comment, story or poll text.", null=True)
    dead = models.BooleanField(default=False)
    url = models.CharField("The URL of the story.", max_length=550, null=True)
    score = models.CharField("The story's score, or the votes for a pollopt.", max_length=10, null=True)
    title = models.CharField("The title of the story, poll or job. HTML.", max_length=500, null=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.title
