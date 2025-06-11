from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=30, unique=True)
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = "categorias"

    def __str__(self):
        return self.category_name

STATUS_CHOICE = (
    ('Borrador', "Borrador"),
    ('Publicado', "Publicado")
)
class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Título')
    slug = models.CharField(max_length=100, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoria')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor')
    featured_image = models.ImageField(upload_to='upload/%d%m%Y', verbose_name='Imagen')
    short_description = models.TextField(max_length=1500, verbose_name='Descripción')
    blog_body = RichTextUploadingField(config_name='blog')
    status = models.CharField(choices=STATUS_CHOICE, default='Borrador', verbose_name='Estado')
    is_featured= models.BooleanField(default=0, verbose_name='Publicación destacada')
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title



class Comment(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='Comentario')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, verbose_name='Activo')

    class Meta:
        ordering = ['-created_date']  # Más recientes primero
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

    def __str__(self):
        return f'Comentario de {self.author.first_name} en {self.post.title}'

    @property
    def author_name(self):
        """Devuelve el nombre del autor del comentario"""
        if hasattr(self.author, 'employee'):
            return f"{self.author.employee.name} {self.author.employee.last_name}"
        return self.author.get_full_name() or self.author.username

    # Comentarios principales
    @classmethod
    def get_main_comments(cls, post):
        return cls.objects.filter(post=post, active=True, parent=None)