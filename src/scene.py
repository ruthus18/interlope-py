from dataclasses import dataclass

from glm import vec3

from .camera import camera_calc_model_matrix
from .camera import camera_calc_perspective_matrix
from .camera import camera_calc_view_matrix
from .gfx import GfxInstance
from .gfx import gfx_draw_scene
from .loader import loader_load_scene
from .world import World
from .world import WorldObject


@dataclass
class SceneObject:
    id: int
    ptr: WorldObject
    position: vec3
    rotation: vec3
    scale: vec3

    is_active: bool

@dataclass
class Scene:
    objects: list[SceneObject]

    _obj_id_iter: int


def scene_load_from_config(world: World) -> Scene:
    scene_params = loader_load_scene()
    objects = []
    _obj_id_iter = 0

    for obj_params in scene_params.objects:

        obj_ptr = world.objects[obj_params.ptr]
        objects.append(
            SceneObject(
                id=_obj_id_iter,
                ptr=obj_ptr,
                position=obj_params.position,
                rotation=obj_params.rotation,
                scale=obj_params.scale,
                is_active=True
            ),
        )
        _obj_id_iter += 1
        

    return Scene(_obj_id_iter=_obj_id_iter, objects=objects)


def scene_add_object(
    self: Scene,
    ptr: WorldObject,
    p: vec3 | None = None,
    r: vec3 | None = None,
    s: vec3 | None = None, 
) -> None:
    self.objects.append(
        SceneObject(
            id=self._obj_id_iter,
            ptr=ptr,
            position=p,
            rotation=r,
            scale=s,
            is_active=True,
        )
    )
    self._obj_id_iter += 1


def scene_draw(self: Scene, gfx: GfxInstance):
    gfx_draw_scene(
        gfx,
        persp_mat=camera_calc_perspective_matrix(),  # TODO
        view_mat=camera_calc_view_matrix(),  # TODO
        objects_queue=(
            (
                obj.ptr.mesh.gfx_data,
                obj.ptr.texture.gfx_data,
                camera_calc_model_matrix(obj.position, obj.rotation, obj.scale),
            )
            for obj in self.objects
            if obj.is_active
        )
    )
