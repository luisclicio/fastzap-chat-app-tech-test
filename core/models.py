from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    is_private = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        "auth.User", related_name="rooms", on_delete=models.CASCADE
    )
    members = models.ManyToManyField(
        "auth.User",
        blank=True,
        through="RoomMember",
        related_name="room_members",
    )

    def __str__(self):
        return self.name


class RoomMember(models.Model):
    is_online = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    room = models.ForeignKey(Room, related_name="memberships", on_delete=models.CASCADE)
    user = models.ForeignKey(
        "auth.User", related_name="room_memberships", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user.username} in {self.room.name}"


class Message(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        REJECTED = "rejected", "Rejected"
        APPROVED = "approved", "Approved"

    content = models.TextField()
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE)
    author = models.ForeignKey(
        "auth.User", related_name="messages", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.author.username} ({self.status}): {self.content[:20]}"
