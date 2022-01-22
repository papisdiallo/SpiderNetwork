from django.urls import path
from .views import getUserProfileForm, crop_image

urlpatterns = [
    path("update-profile/<slug:profile_slug>/",
         getUserProfileForm, name="edit-profile"),
    path("cropping-image/", crop_image, name="crop-image"),
]
