

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
import blog_app
from blog_app.views import home
from blog_app import views as BlogsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', blog_app.views.home, name='home'),
    path('categoria/', include('blog_app.urls')),
    path('<slug:slug>', blog_app.views.blogs, name='blogs'),
    # URLs de autenticación (NUEVAS)
    path('login/', BlogsView.login_view, name='login'),
    path('logout/', BlogsView.logout_view, name='logout'),

    # Django-smart-select
    path('chaining/', include('smart_selects.urls')),
    # Search
    path('blog/buscar/', BlogsView.search, name='search'),

    #CKEditor
    path('ckeditor/', include('ckeditor_uploader.urls')),

    # URLS de employee
    path('employee/', include('employees.urls')),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
