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
