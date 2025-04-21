from unittest.mock import AsyncMock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from core.models import Message, Room
from core.tasks import moderate_message

User = get_user_model()


class ModerateMessageTaskTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        from django.conf import settings

        settings.CELERY_TASK_ALWAYS_EAGER = True
        settings.CELERY_TASK_EAGER_PROPAGATES = True

    def setUp(self):
        # Create admin user
        self.admin_user = User.objects.create_user(
            username="admin", password="adminpass", is_staff=True
        )

        # Create a room
        self.room = Room.objects.create(
            name="Test Room", is_private=False, owner=self.admin_user
        )

        # Create a message
        self.message = Message.objects.create(
            content="This is a test message",
            room=self.room,
            status=Message.Status.PENDING,
            author=self.admin_user,
        )

    @patch("core.tasks.is_safe_content", return_value=True)
    @patch("channels.layers.get_channel_layer")
    def test_moderate_message_approves_safe_content(
        self, mock_channel_layer, mock_is_safe_content
    ):
        # Configure the mock channel layer group_send to be async
        mock_channel_layer.return_value.group_send = AsyncMock()

        # Call the task
        moderate_message(self.message.id)

        # Assert that is_safe_content was called
        mock_is_safe_content.assert_called_once_with(self.message.content)

        # Refresh the message from the database
        self.message.refresh_from_db()

        # Assert the message was approved
        self.assertEqual(self.message.status, Message.Status.APPROVED)

        # Assert the message was sent to the channel layer
        mock_channel_layer.return_value.group_send.assert_called_once_with(
            f"room_{self.room.id}",
            {"type": "chat_message", "message_id": self.message.id},
        )

    @patch("core.tasks.is_safe_content", return_value=False)
    def test_moderate_message_rejects_unsafe_content(self, mock_is_safe_content):
        # Call the task
        moderate_message(self.message.id)

        # Assert that is_safe_content was called
        mock_is_safe_content.assert_called_once_with(self.message.content)

        # Refresh the message from the database
        self.message.refresh_from_db()

        # Assert the message was rejected
        self.assertEqual(self.message.status, Message.Status.REJECTED)
