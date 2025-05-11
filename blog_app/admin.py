from django.contrib import admin
from blog_app.models import Category, Blog

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}
    list_display = ('title', 'category', 'author', 'status', 'is_featured', 'created_at')
    search_fields = ('title','created_at')
    list_editable = ('status','is_featured')



admin.site.register(Category)
admin.site.register(Blog, BlogAdmin)
