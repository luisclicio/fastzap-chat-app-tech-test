from django.urls import re_path

from core import consumers

websocket_urlpatterns = [
    re_path(r"ws/rooms/(?P<room_id>\w+)/$", consumers.RoomConsumer.as_asgi()),
]
