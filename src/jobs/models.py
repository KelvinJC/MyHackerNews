from datetime import datetime, timezone

from django.db import models
from django.utils import timezone

# Create your models here.
class JobArticle(models.Model):
    api_id        = models.IntegerField(unique=True)
    api_time      = models.IntegerField()
    author        = models.CharField(max_length=100)
    type          = models.CharField(max_length=100, blank=True, null=True)
    title         = models.CharField(max_length=200)
    url           = models.URLField(blank=True, null=True)
    time_added     = models.DateTimeField(default=timezone.now)


