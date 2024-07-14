from dataclasses import dataclass

__all__ = ('Message',)


@dataclass(frozen=True, slots=True)
class Message:
    id: int
    chat_id: int
