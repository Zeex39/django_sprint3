from django.shortcuts import render, get_object_or_404
from .models import Category, Post
from datetime import datetime
import pytz
# Create your views here.


def index(request):
    posts = Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=datetime.now().replace(tzinfo=pytz.UTC)
    ).order_by('pub_date')[:5]
    return render(request, 'blog/index.html', {'post_list': posts})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    if post.pub_date > datetime.now().replace(
        tzinfo=pytz.UTC
    ) or not post.is_published or not post.category.is_published:
        return render(request, '404.html', status=404)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    if not category.is_published:
        return render(request, '404.html', status=404)
    posts = Post.objects.filter(
        is_published=True,
        pub_date__lte=datetime.now().replace(tzinfo=pytz.UTC),
        category=category
    )
    return render(request, 'blog/category.html', {
        'category': category,
        'post_list': posts
    })
