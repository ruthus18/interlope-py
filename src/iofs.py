from PIL import Image

from .config import config


def iofs_read_shader_file(filename: str) -> str:
    path = config.SHADERS_DIR + filename

    with open(path, 'r') as shader_file:
        return shader_file.read()


def iofs_read_mesh_file(filename: str) -> str:
    path = config.ASSETS_DIR + 'models/' + filename

    with open(path, 'r') as asset_file:
        return asset_file.read()


def iofs_read_texture_file(filename: str) -> Image:
    path = config.ASSETS_DIR + 'textures/' + filename
    return Image.open(path).transpose(Image.FLIP_TOP_BOTTOM)
