from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Message, Room

User = get_user_model()


class RoomViewSetTestCase(TestCase):
    def setUp(self):
        # Create admin user
        self.admin_user = User.objects.create_user(
            username="admin", password="adminpass", is_staff=True
        )

        # Create regular user
        self.regular_user = User.objects.create_user(
            username="user", password="userpass"
        )

        # Create private and public rooms owned by admin user
        self.public_room = Room.objects.create(
            name="Public Room", is_private=False, owner=self.admin_user
        )
        self.public_room.members.add(self.admin_user)

        self.private_room = Room.objects.create(
            name="Private Room", is_private=True, owner=self.admin_user
        )
        self.private_room.members.add(self.admin_user)
        self.private_room.members.add(self.regular_user)

        # Create messages
        self.message1 = Message.objects.create(
            content="Hello from admin",
            author=self.admin_user,
            room=self.private_room,
            status=Message.Status.APPROVED,
        )
        self.message2 = Message.objects.create(
            content="Hello from user",
            author=self.regular_user,
            room=self.private_room,
            status=Message.Status.APPROVED,
        )

        # Obtain JWT tokens
        admin_response = self.client.post(
            "/api/auth/token/",
            {"username": "admin", "password": "adminpass"},
            format="json",
        )
        self.admin_token = admin_response.data["access"]

        user_response = self.client.post(
            "/api/auth/token/",
            {"username": "user", "password": "userpass"},
            format="json",
        )
        self.user_token = user_response.data["access"]

        # API client
        self.client = APIClient()

    def test_admin_can_create_room(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.post(
            "/api/rooms/",
            {"name": "New Room", "is_private": True},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Room.objects.count(), 3)

    def test_regular_user_can_view_public_and_member_rooms(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.get("/api/rooms/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        room_names = [room["name"] for room in response.data]
        self.assertIn("Public Room", room_names)
        self.assertIn("Private Room", room_names)

    def test_regular_user_cannot_create_room(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.post(
            "/api/rooms/",
            {"name": "Unauthorized Room", "is_private": True},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Room.objects.count(), 2)

    def test_admin_can_view_all_rooms(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.get("/api/rooms/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        room_names = [room["name"] for room in response.data]
        self.assertIn("Public Room", room_names)
        self.assertIn("Private Room", room_names)

    def test_room_member_can_list_messages(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.get(f"/api/rooms/{self.private_room.id}/messages/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        message_contents = [message["content"] for message in response.data]
        self.assertIn("Hello from user", message_contents)
        self.assertIn("Hello from admin", message_contents)

    def test_non_member_cannot_list_messages(self):
        User.objects.create_user(username="nonmember", password="nonmemberpass")
        non_member_response = self.client.post(
            "/api/auth/token/",
            {"username": "nonmember", "password": "nonmemberpass"},
            format="json",
        )
        non_member_token = non_member_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {non_member_token}")
        response = self.client.get(f"/api/rooms/{self.private_room.id}/messages/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
