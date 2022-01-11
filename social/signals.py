from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.core.exceptions import ValidationError
from .models import Post


@receiver(m2m_changed, sender=Post.images.through)
def images_changed(sender, **kwargs):
    print("the images signal changed ran")
