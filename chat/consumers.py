from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import singleOneToOneRoom, messages
from channels.db import database_sync_to_async
from django.db.models import Q
from django.contrib.auth import get_user_model
import json

User = get_user_model()


class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        current_user_id = self.scope['user'].id
        other_user_id = self.scope['url_route']['kwargs']['id']
        user1 = await self.get_user(current_user_id)
        user2 = await self.get_user(other_user_id)
        room_name = await self.get_room_name(user1, user2)
        self.room_name = room_name
        self.room_group_name = f"Chat-{self.room_name}"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        current_user_id = self.scope['user'].id
        other_user_id = self.scope['url_route']['kwargs']['id']
        user1 = await self.get_user(current_user_id)
        user2 = await self.get_user(other_user_id)
        room = await self.get_room_instance(self.room_name)
        avatar_url = await self.create_msg_n_return_avatar_url(room, user1, user2, message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'avatar_url': avatar_url,
            }
        )

    async def chat_message(self, event):  # event will contain the msg and username
        message = event['message']
        username = event['username']
        avatar_url = event['avatar_url']
        await self.send(
            text_data=json.dumps(
                {"message": message, "username": username, "avatar_url": avatar_url, })
        )

    async def disconnect(self, code):
        print("the websocket is disconnected")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    @database_sync_to_async
    def get_room_name(self, user1, user2):
        lookup = Q(first_user=user1, second_user=user2) | Q(
            first_user=user2, second_user=user1)
        room = singleOneToOneRoom.objects.filter(lookup)
        if room.exists():
            return room.first().room_name

    @database_sync_to_async
    def get_user(self, _id):
        return User.objects.get(id=_id)

    @database_sync_to_async
    def get_room_instance(self, room_name):
        return singleOneToOneRoom.objects.get(room_name=room_name)

    @database_sync_to_async
    def create_msg_n_return_avatar_url(self, room, sender, receiver, message):
        msg = messages.objects.create(
            room=room, sender=sender, receiver=receiver, message_body=message)
        return msg.sender.profile.avatar.url
