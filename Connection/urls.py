from django.urls import path
from .views import (
    getUserProfileForm, 
    crop_image, 
    Sending_Link_Forge, 
    cancelForgeLink,
    acceptForgeLink
)

urlpatterns = [
    path("update-profile/<slug:profile_slug>/",
         getUserProfileForm, name="edit-profile"),
    path("cropping-image/", crop_image, name="crop-image"),
    path("sending-link-forge/", Sending_Link_Forge, name="sending-link-forge"),
    path("cancel-forge-link/", cancelForgeLink, name="cancel-link-forge"),
    path("accept-forge-link/", acceptForgeLink, name="accept-link-forge"),
]
