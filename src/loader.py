import tomllib
from dataclasses import dataclass

from glm import vec3

from .color import GLColor
from .config import config

type ObjectID = str

@dataclass
class SceneObjectParams:
    ptr: ObjectID
    position: vec3
    rotation: vec3
    scale: vec3


@dataclass
class LightParams:
    # only point lights supported at now
    position: vec3
    color: GLColor


@dataclass
class CameraDesc:
    position: vec3


@dataclass
class SceneParams:
    objects: list[SceneObjectParams]
    lights: list[LightParams]
    camera: CameraDesc


def loader_load_scene() -> SceneParams:
    scene_path = 'scenes/' + config.ROOT_SCENE + '.toml'

    with open(scene_path) as config_f:
        data = tomllib.loads(config_f.read())

    objects = [SceneObjectParams(
        ptr=o['ptr'],
        position=vec3(o['position']),
        rotation=vec3(o['rotation']),
        scale=vec3(o['scale']),
    ) for o in data['object']]

    return SceneParams(objects=objects, lights=[], camera=[])
