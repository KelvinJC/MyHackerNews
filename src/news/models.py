from datetime import datetime, timezone

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class NewsArticle(models.Model):
    api_id        = models.IntegerField(unique=True)
    api_time      = models.IntegerField(blank=True, null=True)
    post_by       = models.CharField(max_length=100)
    type          = models.CharField(max_length=100)
    title         = models.CharField(max_length=200)
    url           = models.TextField(blank=True, null=True)
    time_added    = models.DateTimeField(auto_now_add=True)
    author        = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    # pub_date  = models.DateField()  convert Unix time to date in hacker request obejct?
