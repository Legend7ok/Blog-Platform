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


def test_post_list_published_only(client, make_post):
    published = make_post(status=Post.Status.PUBLISHED, title="Published post")
    make_post(status=Post.Status.DRAFT, title="Draft post")

    response = client.get(reverse("blog:post_list"))

    posts_page = response.context["posts"]
    assert response.status_code == 200
    assert list(posts_page.object_list) == [published]


def test_post_list_pagination_valid_page(client, make_post):
    for i in range(5):
        make_post(title=f"Published {i}")

    response = client.get(reverse("blog:post_list"), {"page": 2})

    posts_page = response.context["posts"]
    assert response.status_code == 200
    assert posts_page.number == 2
    assert len(posts_page.object_list) == 2


def test_post_list_pagination_invalid_page_returns_first(client, make_post):
    for i in range(7):
        make_post(title=f"Published {i}")

    response = client.get(reverse("blog:post_list"), {"page": "bad"})

    posts_page = response.context["posts"]
    assert response.status_code == 200
    assert posts_page.number == 1


def test_post_list_pagination_out_of_range_returns_last(client, make_post):
    for i in range(7):
        make_post(title=f"Published {i}")

    response = client.get(reverse("blog:post_list"), {"page": 999})

    posts_page = response.context["posts"]
    assert response.status_code == 200
    assert posts_page.number == 3
    assert len(posts_page.object_list) == 1


def test_post_detail_draft_returns_404(client, make_post):
    draft_post = make_post(status=Post.Status.DRAFT, slug="draft-post")

    response = client.get(detail_url(draft_post))

    assert response.status_code == 404


def test_post_detail_comments_only_active(client, make_post):
    post = make_post()
    active_comment = Comment.objects.create(
        post=post, name="Active", email="a@example.com", body="visible", active=True
    )
    Comment.objects.create(
        post=post, name="Inactive", email="i@example.com", body="hidden", active=False
    )

    response = client.get(detail_url(post))

    comments = list(response.context["comments"])
    assert response.status_code == 200
    assert comments == [active_comment]


def test_post_comment_create(client, make_post):
    post = make_post()
    payload = {
        "name": "John",
        "email": "john@example.com",
        "body": "Nice article",
    }

    response = client.post(reverse("blog:post_comment", args=[post.id]), data=payload)

    comment = Comment.objects.get(post=post, email="john@example.com")
    assert response.status_code == 200
    assert comment.body == "Nice article"
    assert comment.active is True


def test_post_comment_draft_returns_404(client, make_post):
    draft_post = make_post(status=Post.Status.DRAFT)
    payload = {
        "name": "John",
        "email": "john@example.com",
        "body": "Comment",
    }

    response = client.post(
        reverse("blog:post_comment", args=[draft_post.id]),
        data=payload,
    )

    assert response.status_code == 404


def test_post_share_draft_returns_404(client, make_post):
    draft_post = make_post(status=Post.Status.DRAFT)

    response = client.get(reverse("blog:post_share", args=[draft_post.id]))

    assert response.status_code == 404


def test_post_share_email_valid(client, make_post):
    post = make_post(title="Share me")
    payload = {
        "name": "Alice",
        "email": "alice@example.com",
        "to": "bob@example.com",
        "comments": "Take a look",
    }

    response = client.post(reverse("blog:post_share", args=[post.id]), data=payload)

    assert response.status_code == 200
    assert response.context["sent"] is True
    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == ["bob@example.com"]
    assert "Share me" in mail.outbox[0].subject


def test_post_share_email_invalid(client, make_post):
    post = make_post()
    payload = {
        "name": "Alice",
        "email": "alice@example.com",
        "to": "not-an-email",
        "comments": "Bad email",
    }

    response = client.post(reverse("blog:post_share", args=[post.id]), data=payload)

    assert response.status_code == 200
    assert response.context["sent"] is False
    assert len(mail.outbox) == 0


def test_post_search_works_by_title(client, make_post):
    if connection.vendor != "postgresql":
        pytest.skip("Current post_search uses PostgreSQL TrigramSimilarity.")

    with connection.cursor() as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")

    title_match = make_post(title="Python patterns", body="Misc text")
    make_post(title="No keyword", body="Deep dive into Python testing")
    make_post(title="Completely unrelated", body="No matches here")

    response = client.get(reverse("blog:post_search"), {"query": "Python"})

    results = list(response.context["results"])
    assert response.status_code == 200
    assert title_match in results


def test_post_list_tag_filtering(client, make_post):
    tagged = make_post(title="Tagged post")
    tagged.tags.add("django")

    not_tagged = make_post(title="No tag post")
    not_tagged.tags.add("python")

    response = client.get(reverse("blog:post_list_by_tag", args=["django"]))

    posts_page = response.context["posts"]
    assert response.status_code == 200
    assert list(posts_page.object_list) == [tagged]