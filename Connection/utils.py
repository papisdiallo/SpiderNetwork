from django.core.files import File
from django.core.files.storage import FileSystemStorage, default_storage
import os
import base64
from enum import Enum
from django.conf import settings
from .models import ForgeLink


def is_ajax(request):  # need to move this function into function for DRY
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class connectionRequestStatus(Enum):
    NO_CON_REQUEST = 0
    YOU_SENT_CON_REQUEST = 1
    THEY_SENT_CON_REQUEST = 2


def get_forge_link_or_false(sender, receiver):
    try:
        return ForgeLink.objects.get(sender=sender, receiver=receiver, is_active=True)
    except ForgeLink.DoesNotExist:
        return False


def save_Base64_Temp_ImageString(imageString):
    print("the save base64 image string ran")
    INCORRECT_PADDING_EXCEPTION = "Incorrect padding"
    try:
        if not os.path.exists(settings.TEMP):
            os.mkdir(settings.TEMP)
        url = os.path.join(settings.TEMP, "temp_image_profile.png")
        storage = FileSystemStorage(location=url)
        image = base64.b64decode(imageString)
        with storage.open("", "wb+") as destination:
            destination.write(image)
            destination.close()

        return url
    except Exception as e:
        if str(e) == INCORRECT_PADDING_EXCEPTION:
            imageString += "=" * ((4 - len(imageString) % 4) % 4)
            return save_Base64_Temp_ImageString(imageString)
    return None


def convertDimensions(dimension):
    return int(float(str(dimension)))
