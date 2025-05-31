from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from blog_app.models import Category, Blog
from django.db.models import Q

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
    try:
        category = Category.objects.get(pk=category_id)
    except:
        return redirect('404.html')
    context={
        'posts':posts,
        'category':category
    }
    return render(request, 'posts_by_category.html', context)

def blogs(request, slug):
    single_blog = get_object_or_404(Blog, slug = slug, status = 'Publicado')
    context = {
        'single_blog': single_blog,
    }
    return render(request, 'blogs.html', context)

def search(request):
    keyword = request.GET.get('keyword')
    blogs = Blog.objects.filter(Q(title__icontains = keyword)| Q(short_description__icontains = keyword) | Q(blog_body__icontains = keyword), status = 'Publicado')
    context = {
        'blogs':blogs,
        'keyword':keyword,
    }
    return render(request, 'search.html', context)
