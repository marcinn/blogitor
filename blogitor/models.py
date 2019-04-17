from enum import IntEnum

import commonmark
import djsqltemplate

from django.contrib.postgres.fields.array import ArrayField
from django.contrib.postgres.search import SearchVectorField
from django.db import models

from . import settings


sql_tag_stats = djsqltemplate.get('posts_tag_stats.sql')


class Importance(IntEnum):
    LOW = -1
    NORMAL = 0
    HIGH = 1
    CRITICAL = 10


IMPORTANCE_CHOICES = tuple(map(
    lambda x: (int(x), str(x).replace('Importance.', '').title()), Importance))


class Language(models.Model):
    code = models.CharField(max_length=10, unique=True, primary_key=True)
    fts_regconfig = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.code


class PostManager(models.Manager):
    def tag_stats(self, queryset=None):
        if queryset is not None:
            pks = tuple(queryset.values_list('pk', flat=True))
        else:
            pks = None
        return list(sql_tag_stats.values(post_pks=pks))


class Post(models.Model):
    slug = models.SlugField(unique=True)
    author = models.CharField(max_length=120)
    title = models.CharField(max_length=255)
    excerpt = models.TextField(null=True, blank=True)
    body = models.TextField(blank=True, default='')
    body_html = models.TextField(blank=True, default='')  # rendered
    date = models.DateField()
    language = models.ForeignKey(
            Language, default=settings.POST_DEFAULT_LANGUAGE_CODE,
            on_delete=models.PROTECT)

    # extra

    tags = ArrayField(models.TextField(), blank=True)
    terms = SearchVectorField(blank=True)

    # options

    allow_comments = models.BooleanField(
            default=settings.POST_ALLOW_COMMENTS_DEFAULT)
    importance = models.IntegerField(
            choices=IMPORTANCE_CHOICES, default=Importance.NORMAL)

    # publication

    publish_after = models.DateTimeField(null=True, blank=True)
    published = models.BooleanField(default=False)
    expires_at = models.DateTimeField(null=True, blank=True)

    # meta

    created_by = models.ForeignKey(
            settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
            null=True, blank=True, related_name='created_posts')
    created_by_username = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(
            settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
            null=True, blank=True, related_name='modified_posts')
    modified_by_username = models.CharField(max_length=120)
    modified_at = models.DateTimeField(auto_now=True)
    published_by = models.ForeignKey(
            settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
            null=True, blank=True, related_name='published_posts')
    published_by_username = models.CharField(
            max_length=120, null=True, blank=True)
    published_at = models.DateTimeField(auto_now=True)
    objects = PostManager()

    def __str__(self):
        return self.title

    def render_body(self):
        parser = commonmark.Parser()
        renderer = commonmark.HtmlRenderer()

        ast = parser.parse(self.body)
        return renderer.render(ast)
