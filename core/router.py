from rest_framework.routers import SimpleRouter

from core.views import MessageViewSet, RoomViewSet, UserViewSet

router = SimpleRouter()

router.register(r"users", UserViewSet, basename="user")
router.register(r"rooms", RoomViewSet, basename="room")
router.register(
    r"rooms/(?P<room_id>[^/.]+)/messages", MessageViewSet, basename="message"
)
