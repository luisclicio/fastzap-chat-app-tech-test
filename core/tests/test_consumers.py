from unittest.mock import patch

from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from django.test import TransactionTestCase

from config.asgi import application
from core.models import Message, Room, RoomMember

User = get_user_model()


class RoomConsumerTestCase(TransactionTestCase):
    def setUp(self):
        # Creates a test user and room
        self.admin_user = User.objects.create_user(
            username="testuser", password="password", is_staff=True
        )
        self.room = Room.objects.create(
            name="Test Room", is_private=False, owner=self.admin_user
        )
        RoomMember.objects.create(user=self.admin_user, room=self.room, is_online=False)

    async def test_connect_and_disconnect(self):
        # Simulates the connection WebSocket
        communicator = WebsocketCommunicator(application, f"/ws/rooms/{self.room.id}/")
        communicator.scope["user"] = self.admin_user  # Simulates an authenticated user

        # Connects to the WebSocket
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Simulates disconnection
        await communicator.disconnect()

    @patch("core.consumers.moderate_message.delay")
    async def test_receive_message_with_moderation(self, mock_moderate_message):
        # Simulates the connection WebSocket
        communicator = WebsocketCommunicator(application, f"/ws/rooms/{self.room.id}/")
        communicator.scope["user"] = self.admin_user  # Simulates an authenticated user

        # Connects to the WebSocket
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Sends a message to the WebSocket
        message_content = {"message": "Hello, World!"}
        await communicator.send_json_to(message_content)

        # Awaits the message to be received
        await communicator.receive_nothing()

        # Checks if the message was saved in the database
        saved_message = await database_sync_to_async(
            lambda: Message.objects.filter(content=message_content["message"]).exists()
        )()
        self.assertTrue(saved_message)

        # Checks if the moderation task was called
        mock_moderate_message.assert_called_once()

        # Simulates disconnection
        await communicator.disconnect()
