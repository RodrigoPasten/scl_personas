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
    blog_body = models.TextField(verbose_name='Contenido')
    status = models.CharField(choices=STATUS_CHOICE, default='Borrador', verbose_name='Estado')
    is_featured= models.BooleanField(default=0, verbose_name='Publicación destacada')
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

