from dataclasses import dataclass

from .assets import AssetStorage
from .db import Database
from .db import db_get_objects
from .loader import ObjectID
from .mesh import Mesh
from .texture import Texture


@dataclass
class WorldObject:
    id: ObjectID
    name: str
    mesh: Mesh
    texture: Texture


@dataclass
class World:
    objects: dict[ObjectID, WorldObject]


def world_load_from_db(db: Database, assets: AssetStorage) -> World:
    objects = {}

    for obj in db_get_objects(db):
        if obj.id in objects:
            raise ValueError(
                f'World init error: duplicated object ID = {obj.id}'
            ) 

        try:
            mesh = assets.meshes[obj.model]
        except KeyError:
            raise ValueError(
                f'World init error: unknown mesh ID = {obj.model}'
            )

        try:
            texture = assets.textures[obj.texture]
        except KeyError:
            raise ValueError(
                f'World init error: unknown texture ID = {obj.texture}'
            )

        objects[obj.id] = WorldObject(
            id=obj.id,
            name=obj.name,
            mesh=mesh,
            texture=texture,
        )

    return World(objects=objects)
