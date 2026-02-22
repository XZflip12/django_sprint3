from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Post, Category


# Create your views here.
def index(request):
    template = 'blog/index.html'
    post_list = (Post.objects
    .select_related(
        'category'
    )
    .filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    )
    .order_by(
        'title'
    )
    .reverse()[:5])
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.select_related('category'),
        Q(id=id),
        Q(is_published=True),
        Q(pub_date__lte=timezone.now()),
        Q(category__is_published=True)
    )
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = (Post.objects
    .filter(
        category=category,
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    )
    .order_by(
        'title'
    ))
    context = {'category': category,
               'post_list': post_list}
    return render(request, template, context)
