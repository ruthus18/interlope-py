import logging
import logging.config

LOG_LEVEL = 'INFO'

log_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'class': 'colorlog.ColoredFormatter',
            'format': (
                '{green}[{asctime}.{msecs:03.0f}] '
                '{yellow}{levelname}\t'
                '{reset}{message}'
            ),
            'datefmt': '%H:%M:%S',
            'style': '{',
        },
    },
    "filters": {},
    "handlers": {
        "stdout": {
            "level": LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "null": {
            "level": "DEBUG",
            "class": "logging.NullHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": ["stdout"],
            "level": logging.DEBUG,
        },
        "asyncio": {
            "handlers": ["stdout"],
            "level": logging.ERROR,
        },
    },
}


def logging_init():
    logging.config.dictConfig(log_config)
