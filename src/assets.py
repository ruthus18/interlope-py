from dataclasses import dataclass

from .db import Database
from .db import db_get_models
from .db import db_get_textures
from .gfx import GfxInstance
from .mesh import Mesh
from .mesh import MeshID
from .mesh import mesh_load_from_record
from .texture import Texture
from .texture import TextureID
from .texture import texture_load_from_record


@dataclass
class AssetStorage:
    meshes: dict[MeshID, Mesh]
    textures: dict[TextureID, Texture]


def assets_load_from_db(db: Database, gfx: GfxInstance) -> AssetStorage:
    model_records = db_get_models(db)
    texture_records = db_get_textures(db)
    meshes = {}
    textures = {}

    for record in model_records:
        mesh = mesh_load_from_record(record, gfx)
        if mesh.id in meshes:
            raise ValueError(f'Duplicated mesh ID: {mesh.id}')

        meshes[mesh.id] = mesh

    for record in texture_records:
        texture = texture_load_from_record(record, gfx)
        if texture.id in textures:
            raise ValueError(f'Duplicated mesh ID: {mesh.id}')

        textures[texture.id] = texture

    return AssetStorage(meshes=meshes, textures=textures)
