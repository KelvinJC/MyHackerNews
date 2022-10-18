from django.urls import path

from . import views

urlpatterns = [
   path('cache_job_article/', views.add_job_article_to_cache, name='cache-job'),
   path('list_cached_jobs/', views.list_cached_jobs, name='list-cached-jobs'),


   path('list_cached_news/', views.list_cached_news, name='list-cached-news'),
   path('cache_news_article/', views.add_news_article_to_cache, name='cache-news'),

]
