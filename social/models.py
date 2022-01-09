from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.template.defaultfilters import slugify


class Tags(models.Model):
    name = models.CharField(max_length=200)
    tag_slug = models.SlugField()
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    images = models.ManyToManyField(Files, null=True, blank=True)
    content = models.TextField()
    post_slug = models.SlugField(blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.author}'s post"

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    date_commented = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.author}'s comment"


class Files(models.Model):
    image = models.ImageField(upload_to="post/images")
