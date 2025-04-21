from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminUserOrReadOnly(BasePermission):
    """
    Allows access only to admin users or read-only requests.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or request.user and request.user.is_staff
        )


class IsRoomMember(BasePermission):
    """
    Allows access only to members of the room.
    """

    def has_permission(self, request, view):
        room_id = int(view.kwargs.get(view.lookup_url_kwarg))

        if not room_id:
            return False

        # Check if the user is a member of the room
        return (
            request.user.is_authenticated
            and request.user.room_members.filter(id=room_id).exists()
        )
