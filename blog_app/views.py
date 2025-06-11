from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Blog, Comment
from .forms import CommentForm


from blog_app.models import Category, Blog
from django.db.models import Q

# Login y Logout
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Django verifica las credenciales
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Crea la sesión
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)  # Destruye la sesión
    return redirect('login')


# Crea las categorias del nav
@login_required
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

@login_required
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


@login_required
def blogs(request, slug):
    single_blog = get_object_or_404(Blog, slug=slug, status='Publicado')

    # Obtener comentarios activos del post
    comments = Comment.objects.filter(post=single_blog, active=True)  # CORREGIDO: single_blog

    # Manejar envío de nuevo comentario
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = single_blog  # CORREGIDO: single_blog
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comentario agregado exitosamente')
            return redirect('blogs', slug=slug)
    else:
        form = CommentForm()

    # CONTEXTO ÚNICO Y CORREGIDO
    context = {
        'single_blog': single_blog,  # Mantén tu nombre original
        'comments': comments,
        'comment_form': form,
        'comments_count': comments.count()
    }

    return render(request, 'blogs.html', context)

@login_required
def search(request):
    keyword = request.GET.get('keyword')
    blogs = Blog.objects.filter(Q(title__icontains = keyword)| Q(short_description__icontains = keyword) | Q(blog_body__icontains = keyword), status = 'Publicado')
    context = {
        'blogs':blogs,
        'keyword':keyword,
    }
    return render(request, 'search.html', context)
