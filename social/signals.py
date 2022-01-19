from django.dispatch import receiver
from django.db.models.signals import m2m_changed, pre_save, post_save
from django.core.exceptions import ValidationError
from .models import Post, UserProfile, Comment
from django.contrib.auth.models import User
import string
import random
from Connection.models import ConnectionsList


def uniqueSlugDigit(instance, size=12, new_slug=None):
    Klass = instance.__class__
    if new_slug is not None:
        slug = new_slug
    else:
        slug = "".join([random.choice(string.ascii_lowercase +
                       string.ascii_uppercase + string.digits) for n in range(size)])
    if Klass.objects.filter(post_slug=slug).exists():
        slug = "".join([random.choice(string.ascii_lowercase +
                       string.ascii_uppercase + string.digits) for n in range(size)])
        return uniqueSlugDigit(instance, size=12, new_slug=slug)
    return slug


@receiver(m2m_changed, sender=Post.images.through)
def images_changed(sender, *args, **kwargs):
    instance = kwargs.get("instance")
    if instance.images.all().count() > 5:
        raise ValidationError("You cannot upload more than 5 images")


@receiver(pre_save, sender=Post)
def post_unique_slug(sender, instance, *args, **kwargs):
    if not instance.post_slug:
        instance.post_slug = uniqueSlugDigit(instance)


@receiver(pre_save, sender=Comment)
def post_unique_slug(sender, instance, *args, **kwargs):
    if not instance.comment_slug:
        instance.comment_slug = "".join([random.choice(string.ascii_lowercase +
                                        string.ascii_uppercase + string.digits) for n in range(10)]) + str(instance.id)


@receiver(post_save, sender=User)
def post_unique_slug(sender, instance, created, *args, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance)
        profile.profile_slug = "".join([random.choice(string.ascii_lowercase +
                                                      string.ascii_uppercase + string.digits) for n in range(10)]) + str(instance.id)
        profile.save()
        # create a ConnectionsList for the new user
        userConnectionsList = ConnectionsList.objects.create(user=instance)
        userConnectionsList.save()  # do not think it is necessary though...
