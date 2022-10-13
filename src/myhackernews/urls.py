"""myhackernews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from news.views import add_news_view, news_api_request_view, news_list_view, home_view, search_news_view
from jobs.views import jobs_api_request_view, jobs_list_view, search_jobs_view, add_job_view


urlpatterns = [
    path('', home_view, name='home'),

    path('accounts/', include('accounts.urls')),
    
    path('jobs_list/', jobs_list_view, name='list-jobs'),
    path("jobs_api_request/", jobs_api_request_view, name='api-jobs'),
    path("search_jobs/", search_jobs_view, name='search-jobs'),
    path("add_job/", add_job_view, name='add-job'),

    path("news_list/", news_list_view, name='list-news'),
    path("news_api_request/", news_api_request_view, name='api-news'),
    path("search_news/", search_news_view, name='search-news'),
    path("add_news/", add_news_view, name='add-news'),
    path("admin/", admin.site.urls),
]
