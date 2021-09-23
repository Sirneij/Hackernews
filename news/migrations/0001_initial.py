# Generated by Django 3.2.7 on 2021-09-23 05:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LatestStory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('unique_api_story_id', models.CharField(max_length=10, null=True, verbose_name='Story ID')),
                ('story_type', models.CharField(max_length=15, null=True, verbose_name='Type of item')),
                ('author', models.CharField(max_length=50, null=True, verbose_name='Author')),
                ('slug', models.SlugField(max_length=2000, null=True)),
                ('time', models.DateTimeField(null=True, verbose_name='Date created')),
                ('text', models.TextField(null=True, verbose_name='The comment, story or poll text.')),
                ('dead', models.BooleanField(default=False)),
                ('url', models.URLField(max_length=1000, null=True, verbose_name='URL')),
                ('score', models.IntegerField(null=True, verbose_name='Score')),
                ('descendants', models.IntegerField(null=True, verbose_name='Descendants')),
                ('title', models.TextField(null=True, verbose_name='Title')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Latest story',
                'verbose_name_plural': 'Latest stories',
                'unique_together': {('unique_api_story_id', 'title')},
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('unique_comment_api_id', models.CharField(max_length=10, null=True, verbose_name='Story ID')),
                ('author', models.CharField(max_length=50, null=True, verbose_name='Author')),
                ('time', models.DateTimeField(null=True, verbose_name='Date created')),
                ('text', models.TextField(null=True, verbose_name='Text')),
                ('dead', models.BooleanField(default=False)),
                ('url', models.URLField(max_length=1000, null=True, verbose_name='URL')),
                ('score', models.IntegerField(null=True, verbose_name='Score')),
                ('title', models.TextField(null=True, verbose_name='Title')),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='news.lateststory')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'unique_together': {('unique_comment_api_id', 'story')},
            },
        ),
    ]
