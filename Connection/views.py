from django.shortcuts import render
from django.http import JsonResponse
from social.models import UserProfile
from .models import ConnectionsList, ForgeLink
from social.forms import UserProfileForm
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.files import File
import cv2
from .utils import (
    is_ajax, convertDimensions,
    save_Base64_Temp_ImageString,
    get_forge_link_or_false
)
from django.contrib.auth import get_user_model

User = get_user_model()


def getUserProfileForm(request, profile_slug):
    payload = {}
    try:
        profile = UserProfile.objects.get(profile_slug=profile_slug)
    except UserProfile.DoesNotExists():
        payload["error"] = "Something went wrong with getting your profile. Try later...."
    form = UserProfileForm(request.POST or None, instance=profile)
    if is_ajax(request=request):
        if request.method == "GET":
            context = {"form": form, }
            template = render_to_string(
                "connection/profile_update.html", context, request=request)
            return JsonResponse({"template": template, "profileUrl": profile.avatar.url})
        else:
            if form.is_valid():
                # getting the changed field name
                field_name = form.changed_data[0]
                field_obj = UserProfile._meta.get_field(field_name)
                # get the new value of the field
                field_value = field_obj.value_from_object(profile)
                form.save()
                payload["success"] = True
                payload["new_value"] = field_value
                payload["field_name"] = field_name
                payload["max_size"] = settings.MAX_SIZE_FOR_UPLOAD
            else:
                payload["success"] = False
            return JsonResponse(payload)


@login_required
def crop_image(request):
    payload = {}
    user = request.user
    if request.method == "POST" and is_ajax(request=request):
        try:
            # getting the image from the ajax
            image = request.POST.get("imageString")
            url = save_Base64_Temp_ImageString(
                image)  # save the image temporarly
            cropX = convertDimensions(request.POST.get("cropX"))
            cropY = convertDimensions(request.POST.get("cropY"))
            cropWidth = convertDimensions(request.POST.get("cropWidth"))
            cropHeight = convertDimensions(request.POST.get("cropHeight"))

            img = cv2.imread(url)
            if cropX < 0:
                cropX = 0
            if cropY < 0:
                cropY = 0

            cropped_image = img[cropY:cropY+cropHeight, cropX:cropX+cropWidth]
            cv2.imwrite(url, cropped_image)
            user.profile.avatar.save(
                f"{user.id}_profile_image.png", File(open(url, "rb")))
            payload["success"] = True
            # payload["profile_url"] = user.profile.avatar.url
        except Exception as e:
            payload["success"] = False
            payload["error"] = e
    return JsonResponse(payload)


@login_required
def Sending_Link_Forge(request):
    payload = {}
    user = request.user
    if is_ajax(request=request) and request.method == "POST":
        receiver_profile_slug = request.POST.get("profile_slug")
        receiver = UserProfile.objects.get(
            profile_slug=receiver_profile_slug).user
        try:  # Getting a cancelled request if exists and setting it active again
            old_Link = ForgeLink.objects.get(sender=user, receiver=receiver)
            if old_Link:
                if not old_Link.is_active:
                    old_Link.is_active = True  # Setting it back to True
                    old_Link.save()
                    payload["success"] = True
                    payload["profile_owner"] = receiver.username
                else:
                    payload["error"] = "You have already sent a link request to this user"
            else:  # means there is not old request at all
                new_con = ForgeLink.objects.create(
                    sender=user, receiver=receiver)
                new_con.save()
                payload["success"] = True
                payload["profile_owner"] = receiver.username
        except ForgeLink.DoesNotExist:
            new_con = ForgeLink.objects.create(
                sender=user, receiver=receiver)
            new_con.save()
            payload["success"] = True
            payload["profile_owner"] = receiver.username
    return JsonResponse(payload)


@login_required
def cancelForgeLink(request):
    payload = {}
    if is_ajax(request=request) and request.method == "POST":
        profile_slug = request.POST.get('profile_slug')
        receiver = UserProfile.objects.get(profile_slug=profile_slug).user
        try:
            link = ForgeLink.objects.get(
                sender=request.user, receiver=receiver, is_active=True)
            if link:
                link.is_active = False
                link.save()
                payload["success"] = True
        except ForgeLink.DoesNotExist:
            payload["error"] = "Sorry! Impossible to cancel this request now. Try later!!!"
    return JsonResponse(payload)


@login_required
def deleteForgeLink(request):
    payload = {}
    if is_ajax(request=request) and request.method == "POST":
        request_id = request.POST.get('request_id')
        try:
            link = ForgeLink.objects.get(id=request_id)
            if link:
                link.decline()
                link.save()
                payload["success"] = True
        except ForgeLink.DoesNotExist:
            payload["error"] = "Sorry! Impossible to delete this request now. Try later!!!"
    return JsonResponse(payload)


@login_required
def acceptForgeLink(request):
    payload = {}
    if is_ajax(request=request) and request.method == "POST":
        request_id = request.POST.get("request_id")
        try:
            link = ForgeLink.objects.get(pk=request_id)
            link.accept()
            link.save()
            payload["success"] = True
            payload["sender"] = link.sender.username
        except ForgeLink.DoesNotExist:
            payload["error"] = "Cannot accept this request now. Please Try later !!"
        return JsonResponse(payload)


@login_required
def Unlink(request):
    payload = {}
    user = request.user
    if is_ajax(request=request) and request.method == 'POST':
        removee_id = request.POST.get("removee_id")
        # need to check if the removee is inside of the list of connections
        # first before making the remove action. User the areLinked method
        removee = User.objects.get(pk=removee_id)
        try:
            link = ConnectionsList.objects.get(user=user)
            if link.areLinked(removee):  # just a simple check
                link.unLink(removee)
                payload["success"] = True
            else:
                payload["error"] = f"You can only remove a user within your connections"
        except ConnectionsList.DoesNotExist:
            payload["error"] = f"Cannot unlink {removee.username} now. Please try later!"
    return JsonResponse(payload)
