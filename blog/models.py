from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse



class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status = 'published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length = 250)
    body = models.TextField()
    slug = models.SlugField(max_length=250, unique_for_date = 'publish')

    publish = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length = 10, choices = STATUS_CHOICES, default = 'draft')
    objects = models.Manager()
    published = PublishedManager()
    class Meta:
        ordering = ('-publish',)
    def __str__(self):
        return f"{self.title} | Status: {self.status}"
        #Кононические URLы: blog/<year>/<month>/<day>/<slug>/
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])
