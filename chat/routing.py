from django.urls import re_path
from .consumers import PersonalChatConsumer


websocket_urlpatterns = [
    re_path(r'ws/personalChat/(?P<id>\d+)/$',
            PersonalChatConsumer.as_asgi()),
]
