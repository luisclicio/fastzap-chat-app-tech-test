import logging

import channels.layers
from asgiref.sync import async_to_sync

from config.celery import app
from core.utils import is_safe_content

logger = logging.getLogger(__name__)


@app.task
def moderate_message(message_id):
    """
    Moderates a message by checking its content and updating its status.
    """
    from core.models import Message

    logger.info(f"Moderating message {message_id}.")
    message = Message.objects.get(id=message_id)
    has_safe_content = is_safe_content(message.content)

    if has_safe_content:
        message.status = Message.Status.APPROVED

        # Sends approved message to the room's channel layer
        channel_layer = channels.layers.get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"room_{message.room.id}",
            {
                "type": "chat_message",
                "message_id": message.id,
            },
        )
        logger.info(
            f"Message {message.id} approved and sent to room {message.room.id}."
        )
    else:
        message.status = Message.Status.REJECTED
        logger.info(f"Message {message.id} rejected due to profanity.")

    message.save()
