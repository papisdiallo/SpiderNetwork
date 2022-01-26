from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.template.defaultfilters import slugify


class Files(models.Model):
    image = models.ImageField(upload_to="post/images")


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    images = models.ManyToManyField(Files)
    content = models.TextField()
    post_slug = models.SlugField(blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User,  related_name="likes", blank=True,)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.author}'s post"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True, blank=True, related_name="comments")
    image = models.ForeignKey(
        Files, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField()
    comment_slug = models.SlugField(blank=True, null=True)
    likes = models.ManyToManyField(
        User,  related_name="comment_likes", blank=True,)
    date_commented = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.author}'s comment"


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(
        default="default/default.png", upload_to="users/avatar/")
    full_name = models.CharField(max_length=200, blank=True, null=True)
    work_at = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    profile_slug = models.SlugField()
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
