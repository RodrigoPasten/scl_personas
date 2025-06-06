# Generated by Django 5.2.1 on 2025-05-11 02:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='update_up',
            new_name='update_at',
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.CharField(blank=True, max_length=100, unique=True)),
                ('featured_image', models.ImageField(upload_to='upload/%d%m%Y')),
                ('short_description', models.TextField(max_length=1500)),
                ('status', models.IntegerField(choices=[(0, 'Borrador'), (1, 'Publicado')], default=0)),
                ('is_featured', models.BooleanField(default=0, verbose_name='Publicación destacada')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('update_at', models.DateField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog_app.category')),
            ],
        ),
    ]
