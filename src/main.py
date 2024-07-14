import time
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass

import redis

from config import load_config
from logger import get_logger, setup_logger
from telegram import TelegramBot, get_telegram_bot_http_client

logger = get_logger('app')


@dataclass(frozen=True, slots=True)
class Message:
    id: int
    chat_id: int


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


def main() -> None:
    config = load_config()
    setup_logger()

    logger.debug('Starting')

    redis_client = redis.from_url(config.redis_url, decode_responses=True)

    with get_telegram_bot_http_client(
            token=config.telegram_bot_token,
    ) as http_client:
        telegram_bot = TelegramBot(http_client)

        for _ in range(100):
            raw_messages = redis_client.lpop('duck-duck:clean-up', 100)

            if raw_messages is None:
                logger.info('No more messages to clean up')
                break

            messages = parse_messages(raw_messages)

            chat_id_to_messages = group_by_chat_id(messages)

            for chat_id, messages in chat_id_to_messages.items():
                message_ids = [message.id for message in messages]

                telegram_bot.delete_messages(
                    chat_id=chat_id,
                    message_ids=message_ids,
                )
                time.sleep(0.1)

    logger.debug('Finished')


if __name__ == '__main__':
    main()
