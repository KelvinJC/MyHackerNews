from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
import django.db
from django.contrib.auth.decorators import login_required

from .models import CachedJobArticle, CachedNewsArticle
from jobs.models import JobArticle
from news.models import NewsArticle


# Create your views here.
def add_job_article_to_cache(request):
    if request.method == "POST":
        id = request.POST.get('cached_job')
        a = JobArticle.objects.get(pk=id)
        try:
            CachedJobArticle.objects.create(
            user   = request.user,
            article = a,
            )

            messages.success(request, ('The article has been added to your stash.'))
        except django.db.utils.IntegrityError:
                print( 'job story is already in the cache')
                messages.error(request, ('This article is in your stash already.'))
    return redirect('list-jobs')

@login_required
def list_cached_jobs(request):
    cached = CachedJobArticle.objects.filter(user=request.user).order_by('-time_cached')
    return render(request, 'cached_articles/cached_jobs.html', {'cached': cached})


def add_news_article_to_cache(request):
    if request.method == "POST":
        id = request.POST.get('cached_news')
        a = NewsArticle.objects.get(pk=id)
        
        try:
            CachedNewsArticle.objects.create(
            user    = request.user,
            article = a,
            )

            messages.success(request, ('The article has been added to your stash.'))
        except django.db.utils.IntegrityError:
                print( 'news story is already in the cache')
                messages.error(request, ('This article is in your stash already.'))
    return redirect('list-news')

def list_cached_news(request):
    cached = CachedNewsArticle.objects.filter(user=request.user).order_by('-time_cached')
    return render(request, 'cached_articles/cached_news.html', {'cached': cached})