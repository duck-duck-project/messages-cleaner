import json
import logging.config

import pathlib
from typing import Final

__all__ = ('get_logger', 'setup_logger', 'LOGGING_CONFIG_FILE_PATH')

LOGGING_CONFIG_FILE_PATH: Final[pathlib.Path] = (
        pathlib.Path(__file__).parent.parent / 'logging_config.json'
)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def setup_logger(
        config_file_path: pathlib.Path = LOGGING_CONFIG_FILE_PATH,
) -> None:
    logging_config_text = config_file_path.read_text(encoding='utf-8')
    logging.config.dictConfig(json.loads(logging_config_text))
