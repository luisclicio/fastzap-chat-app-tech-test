from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Message, Room
from core.permissions import IsAdminUserOrReadOnly, IsRoomMember
from core.serializers import MessageSerializer, RoomSerializer, UserSerializer

User = get_user_model()


class UserViewSet(viewsets.GenericViewSet):
    """
    API endpoint that allows users to be viewed.
    """

    serializer_class = UserSerializer

    @action(detail=False, methods=["get"])
    def profile(self, request):
        """
        Returns the authenticated user.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class RoomViewSet(viewsets.ModelViewSet):
    """
    API endpoints that allows rooms to be viewed or edited.

    Only admin users (is_staff) can create, update or delete rooms.
    Regular users can only view rooms they are members of or public rooms.
    """

    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = None

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset.all()

        return self.queryset.filter(
            Q(is_private=False)
            | Q(owner=self.request.user)
            | Q(members=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        serializer.instance.members.add(self.request.user)
        serializer.instance.save()


class MessageViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows messages to be listed.

    Only members of the room can list messages.
    """

    queryset = Message.objects.filter(status=Message.Status.APPROVED).prefetch_related(
        "author"
    )
    serializer_class = MessageSerializer
    permission_classes = [IsRoomMember]
    pagination_class = None
    lookup_field = "room__id"
    lookup_url_kwarg = "room_id"

    def get_queryset(self):
        room_id = self.kwargs.get(self.lookup_url_kwarg)
        return self.queryset.filter(room__id=room_id)
