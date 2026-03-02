from datetime import timedelta

import pytest
from django.contrib.auth.models import User
from django.core import mail
from django.db import connection
from django.urls import reverse
from django.utils import timezone

from .models import Comment, Post


pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def email_settings(settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    settings.DEFAULT_FROM_EMAIL = "noreply@example.com"


@pytest.fixture
def author():
    return User.objects.create_user(
        username="author",
        email="author@example.com",
        password="secret123",
    )


@pytest.fixture
def make_post(author):
    counter = {"value": 0}

    def _make_post(**kwargs):
        counter["value"] += 1
        idx = counter["value"]
        publish = kwargs.pop("publish", timezone.now() + timedelta(minutes=idx))

        defaults = {
            "title": f"Post {idx}",
            "slug": f"post-{idx}",
            "author": author,
            "body": f"Body for post {idx}",
            "publish": publish,
            "status": Post.Status.PUBLISHED,
        }
        defaults.update(kwargs)
        return Post.objects.create(**defaults)

    return _make_post


def detail_url(post):
    return reverse(
        "blog:post_detail",
        args=[post.publish.year, post.publish.month, post.publish.day, post.slug],
    )
