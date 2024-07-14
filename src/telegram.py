import contextlib
from collections.abc import Iterable

import httpx

from logger import get_logger

__all__ = ('get_telegram_bot_http_client', 'TelegramBot')

logger = get_logger('telegram')


@contextlib.contextmanager
def get_telegram_bot_http_client(token: str) -> httpx.Client:
    base_url = f'https://api.telegram.org/bot{token}'
    with httpx.Client(base_url=base_url) as http_client:
        yield http_client


class TelegramBot:

    def __init__(self, http_client: httpx.Client):
        self.__http_client = http_client

    def delete_messages(
            self,
            chat_id: int,
            message_ids: Iterable[int],
    ) -> httpx.Response:
        url = '/deleteMessages'
        data = {
            'chat_id': chat_id,
            'message_ids': tuple(message_ids),
        }

        logger.debug(
            'Sending delete messages request',
            extra={'data': data},
        )

        response = self.__http_client.post(url, json=data)
        print(response)

        logger.debug(
            'Received delete messages response',
            extra={
                'status_code': response.status_code,
                'response_body': response.text,
            },
        )

        return response
