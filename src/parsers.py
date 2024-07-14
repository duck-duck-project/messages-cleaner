from collections import defaultdict
from collections.abc import Iterable

from models import Message

__all__ = ('group_by_chat_id', 'parse_messages')


def group_by_chat_id(messages: Iterable[Message]) -> dict[int, list[Message]]:
    messages_by_chat_id: defaultdict[int, list[Message]] = defaultdict(list)
    for message in messages:
        messages_by_chat_id[message.chat_id].append(message)
    return dict(messages_by_chat_id)


def parse_messages(elements: Iterable[str]) -> list[Message]:
    messages: list[Message] = []

    for element in elements:
        chat_id, message_id = element.split(':')

        chat_id = int(chat_id)
        message_id = int(message_id)

        messages.append(Message(chat_id=chat_id, id=message_id))

    return messages
