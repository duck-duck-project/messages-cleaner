import time

import redis

from config import load_config
from logger import get_logger, setup_logger
from parsers import group_by_chat_id, parse_messages
from telegram import TelegramBot, get_telegram_bot_http_client

logger = get_logger('app')


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
