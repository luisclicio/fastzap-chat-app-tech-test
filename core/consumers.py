import json
import logging

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from core.models import Message, Room, RoomMember
from core.tasks import moderate_message

logger = logging.getLogger(__name__)

User = get_user_model()


class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            logger.debug("User is anonymous, closing connection.")
            await self.close()
            return

        await self.accept()

        self.room_id = int(self.scope["url_route"]["kwargs"]["room_id"])
        self.is_room_member = await self.user_is_room_member()

        if not self.is_room_member:
            logger.debug(
                f"User {self.scope['user'].id} is not a member of the room {self.room_id}, closing connection."
            )
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "user_not_member",
                    }
                )
            )
            await self.close()
            return

        # Adds the user to the group
        self.room_group_name = f"room_{self.room_id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.update_online_status(True)
        await self.broadcast_members_online()

        logger.debug(f"User {self.scope['user'].id} connected to room {self.room_id}.")

    async def disconnect(self, close_code):
        """
        Handles the user connection close.
        """
        if self.scope["user"].is_anonymous or not self.is_room_member:
            return

        # Removes the user from the group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        await self.update_online_status(False)
        await self.broadcast_members_online()

        logger.debug(
            f"User {self.scope['user'].id} disconnected from room {self.room_id}."
        )

    async def receive(self, text_data):
        logger.debug(f"Received message from user {self.scope['user'].id}: {text_data}")
        data = json.loads(text_data)
        message_content = data["message"]
        message = await self.save_message(message_content)
        moderate_message.delay(message.id)

    async def chat_message(self, event):
        """
        Handles the chat message event sent from the group. The event comes from
        Celery moderation task.
        """
        message = await self.get_message(event["message_id"])

        await self.send(
            text_data=json.dumps(
                {
                    "type": "chat_message",
                    "id": message.id,
                    "content": message.content,
                    "created_at": message.created_at.isoformat(),
                    "author": {
                        "id": message.author.id,
                        "username": message.author.username,
                    },
                }
            )
        )

    async def update_members(self, event):
        """
        Handles the update members event sent from the group. The event comes from
        the broadcast_members_online method.
        """
        await self.send(
            text_data=json.dumps(
                {"type": "update_members", "members": event["members"]}
            )
        )

    async def broadcast_members_online(self):
        """
        Broadcasts the updated list of online members to all users in the room. Called
        when a user connects or disconnects from the room.
        """
        members = await self.get_online_members()
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "update_members", "members": members},
        )

    @database_sync_to_async
    def user_is_room_member(self):
        """
        Checks if the user is a member of the room.
        Returns True if the user is a member, False otherwise.
        """
        try:
            user = self.scope["user"]
            room = Room.objects.get(id=self.room_id)
            return room.memberships.filter(user=user).exists()
        except Room.DoesNotExist:
            return False
        except RoomMember.DoesNotExist:
            return False

    @database_sync_to_async
    def update_online_status(self, is_online):
        """
        Updates the online status of the user in the room.
        """
        user = self.scope["user"]
        member = RoomMember.objects.get(user=user.id, room=self.room_id)
        member.is_online = is_online
        member.save()

    @database_sync_to_async
    def get_online_members(self):
        """
        Retrieves the list of online members in the room.
        Returns a list of usernames of online members.
        """
        room = Room.objects.get(id=self.room_id)
        members = room.memberships.filter(is_online=True).values_list(
            "user__username", flat=True
        )
        return list(members)

    @database_sync_to_async
    def save_message(self, content):
        room = Room.objects.get(id=self.room_id)
        message = Message.objects.create(
            room=room, author=self.scope["user"], content=content
        )
        return message

    @database_sync_to_async
    def get_message(self, message_id):
        return Message.objects.filter(id=message_id).prefetch_related("author").first()
