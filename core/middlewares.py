from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


class JWTAuthMiddleware(BaseMiddleware):
    """
    Middleware to handle JWT authentication for WebSocket connections.
    """

    async def __call__(self, scope, receive, send):
        close_old_connections()

        if "user" not in scope or isinstance(scope["user"], AnonymousUser):
            # Extract the token from the query string
            query_string = scope["query_string"].decode()
            query_params = parse_qs(query_string)
            token = query_params.get("token", [None])[0]

            if token:
                try:
                    # Decode the token to get the user ID
                    decoded_token = AccessToken(token)
                    user_id = decoded_token["user_id"]

                    # Get the user object
                    scope["user"] = await self.get_user(user_id)
                except Exception:
                    scope["user"] = AnonymousUser()
            else:
                scope["user"] = AnonymousUser()

        return await self.inner(scope, receive, send)

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()
