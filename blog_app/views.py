from django.shortcuts import render
from django.http import HttpResponse

from blog_app.models import Category, Blog


def home(request):
    categories = Category.objects.all()
    featured_post = Blog.objects.filter(is_featured = True)
    post = Blog.objects.filter(is_featured = False, status = 'Publicado')
    context = {
        'categories':categories,
        'featured_post':featured_post,
        'post':post
    }
    return render(request, 'home.html', context=context)

def post_by_category(request, category_id):
    posts = Blog.objects.filter(status='Publicado', category = category_id)
    context={
        'posts':posts
    }
    return render(request, 'posts_by_category.html', context)
