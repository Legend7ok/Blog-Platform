from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown


register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.simple_tag
def pagination_range(page, max_pages=5):
    try:
        max_pages = int(max_pages)
    except (TypeError, ValueError):
        max_pages = 5

    if max_pages < 1:
        max_pages = 1

    total_pages = page.paginator.num_pages
    current_page = page.number

    if total_pages <= max_pages:
        start = 1
        end = total_pages
    else:
        half = max_pages // 2
        start = current_page - half
        end = start + max_pages - 1

        if start < 1:
            start = 1
            end = max_pages
        elif end > total_pages:
            end = total_pages
            start = total_pages - max_pages + 1

    return range(start, end + 1)
