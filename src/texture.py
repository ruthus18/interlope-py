import logging
from dataclasses import dataclass

from .db import TextureRecord
from .gfx import GfxInstance
from .gfx import TextureGfxData
from .gfx import gfx_load_texture
from .iofs import iofs_read_texture_file

logger = logging.getLogger(__name__)


type TextureID = str


@dataclass
class Texture:
    id: TextureID
    path: str
    gfx_data: TextureGfxData


def texture_load_from_record(
    record: TextureRecord,
    gfx: GfxInstance,
) -> Texture:
    image = iofs_read_texture_file(record.path)
    gfx_data = gfx_load_texture(gfx, image)
    image.close()

    logger.info(f'Texture loaded: {record.id}')
    return Texture(
        id=record.id,
        path=record.path,
        gfx_data=gfx_data,
    )
