import pathlib
import tomllib
from dataclasses import dataclass

__all__ = ('Config', 'CONFIG_FILE_PATH', 'load_config')

CONFIG_FILE_PATH = pathlib.Path(__file__).parent.parent / 'config.toml'


@dataclass(frozen=True, slots=True)
class Config:
    redis_url: str
    telegram_bot_token: str


def load_config(file_path: pathlib.Path = CONFIG_FILE_PATH) -> Config:
    config_text = file_path.read_text(encoding='utf-8')
    config = tomllib.loads(config_text)

    return Config(
        redis_url=config['redis']['url'],
        telegram_bot_token=config['telegram_bot']['token'],
    )
