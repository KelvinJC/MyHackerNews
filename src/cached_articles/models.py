from django.db import models


from django.contrib.auth.models import User
from jobs.models import JobArticle
from news.models import NewsArticle


# Create your models here.
class CachedJobArticle(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(JobArticle, on_delete=models.CASCADE)
    time_cached = models.DateTimeField(auto_now_add=True)
    is_removed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ["user","article"]


class CachedNewsArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE)
    time_cached = models.DateTimeField(auto_now_add=True)
    is_removed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ["user","article"]
