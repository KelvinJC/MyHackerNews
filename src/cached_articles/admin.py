from django.contrib import admin

from .models import CachedJobArticle, CachedNewsArticle


# Register your models here.
admin.site.register(CachedNewsArticle)
admin.site.register(CachedJobArticle)