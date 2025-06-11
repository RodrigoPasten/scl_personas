from django.contrib import admin
from blog_app.models import Category, Blog, Comment


class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}
    list_display = ('title', 'category', 'author', 'status', 'is_featured', 'created_at')
    search_fields = ('title','created_at')
    list_editable = ('status','is_featured')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author_name', 'content_preview', 'created_date', 'active']
    list_filter = ['active', 'created_date', 'post']
    search_fields = ['content', 'author__first_name', 'author__last_name']
    list_editable = ['active']  

    def author_name(self, obj):
        return obj.author_name

    author_name.short_description = 'Autor'

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    content_preview.short_description = 'Comentario'

admin.site.register(Category)
admin.site.register(Blog, BlogAdmin)
