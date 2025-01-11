import tomllib
from dataclasses import dataclass

from . import color

CONF_PATH = 'engineconf.toml'


@dataclass
class Config:
    WINDOW_WIDTH: int
    WINDOW_HEIGHT: int
    WINDOW_TITLE: str
    WINDOW_COLOR: color.GLColor
    WINDOW_FULLSC: bool
    WINDOW_BORDER: bool
    WINDOW_POS: tuple[int, int]

    ASSETS_DIR: str
    SHADERS_DIR: str

    ROOT_SCENE: str


def config_init() -> None:
    with open(CONF_PATH) as f:
        conf = tomllib.loads(f.read())

    win_conf = conf['window']
    win_color = getattr(color, win_conf['color'], color.DARK2)
    paths_conf = conf['paths']

    return Config(
        WINDOW_WIDTH=win_conf['width'],
        WINDOW_HEIGHT=win_conf['height'],
        WINDOW_BORDER=win_conf['border'],
        WINDOW_FULLSC=win_conf['fullsc'],
        WINDOW_TITLE=win_conf['title'],
        WINDOW_POS=win_conf['pos'],
        WINDOW_COLOR=win_color,
        #
        SHADERS_DIR=paths_conf['shaders_dir'],
        ASSETS_DIR=paths_conf['assets_dir'],
        #
        ROOT_SCENE=conf['world']['root_scene'],
    )


config = config_init()
