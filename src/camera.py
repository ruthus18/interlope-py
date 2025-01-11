import enum
import typing as t
from dataclasses import dataclass
from math import cos
from math import pi
from math import sin

import glm
from glm import mat4
from glm import radians
from glm import vec2
from glm import vec3

from .config import config


# TODO: Refactor data model

CAMERA_FOV = 60.0
CAMERA_SPEED = 5
MOUSE_SENS = 150.0


@dataclass
class Camera:
    position: vec3
    # rotation: vec3
    # scale: vec3


class CameraMode(enum.StrEnum):
    fly = enum.auto()
    person = enum.auto()


class MovementController(t.NamedTuple):
    w: bool
    s: bool
    a: bool
    d: bool


mode = CameraMode.person

v_cam_pos = vec3(0.0, 1.7, 2.0)
v_cam_front = vec3(0.0, 0.0, -1.0)
v_cam_up = vec3(0.0, 1.0, 0.0)

yaw = -90.0
pitch = 0.0

# --
# TODO:
#   Camera should be configurable (no use global in `calc_view_matrix`)
#   -> need `Camera` struct


def camera_calc_perspective_matrix() -> mat4:
    WINDOW_ASPECT = config.WINDOW_WIDTH / config.WINDOW_HEIGHT
    return glm.perspective(radians(CAMERA_FOV), WINDOW_ASPECT, 0.01, 100.0)


def camera_calc_view_matrix() -> mat4:
    return glm.lookAt(v_cam_pos, v_cam_pos + v_cam_front, v_cam_up)


to_radian = lambda angle: angle / 180 * pi


def math_rotation_matrix(rot: vec3) -> mat4:
    rotation_x = glm.rotate(to_radian(rot.x), vec3(1, 0, 0))
    rotation_y = glm.rotate(to_radian(rot.y), vec3(0, 1, 0))
    rotation_z = glm.rotate(to_radian(rot.z), vec3(0, 0, 1))
    return rotation_x * rotation_y * rotation_z


def camera_calc_model_matrix(pos: vec3, rot: vec3, sc: vec3) -> mat4:
    return glm.translate(pos) * math_rotation_matrix(rot) * glm.scale(sc)


def camera_control(controller: MovementController, mouse_delta: vec2):
    camera_control_position(controller)
    camera_control_rotation(mouse_delta)


def camera_control_position(controller: MovementController) -> None:
    global v_cam_pos, v_cam_front, v_cam_up

    # -- Movement vector
    if mode == CameraMode.fly:
        v_movement_fw = v_cam_front

    elif mode == CameraMode.person:
        v_movement_fw = vec3(v_cam_front.x, 0, v_cam_front.z)

    else:
        raise ValueError('Unknown camera mode')

    v_movement_slide = glm.cross(v_movement_fw, v_cam_up)

    # -- Movement processing
    v_cam_delta = vec3(0, 0, 0)
    if controller.w:
        v_cam_delta += v_movement_fw
    if controller.s:
        v_cam_delta -= v_movement_fw
    if controller.a:
        v_cam_delta -= v_movement_slide
    if controller.d:
        v_cam_delta += v_movement_slide

    if v_cam_delta != vec3(0):
        v_cam_delta = glm.normalize(v_cam_delta)

    v_cam_pos += v_cam_delta * (CAMERA_SPEED * 0.01)


def camera_control_rotation(mouse_delta: vec2) -> None:
    global v_cam_front, yaw, pitch

    yaw_delta = mouse_delta.x * MOUSE_SENS
    pitch_delta = -mouse_delta.y * MOUSE_SENS

    yaw += yaw_delta
    pitch += pitch_delta

    if (pitch >  89.0): pitch = 89.0
    if (pitch < -89.0): pitch = -89.0

    v_cam_front = glm.normalize((
        cos(radians(yaw)) * cos(radians(pitch)),
        sin(radians(pitch)),
        sin(radians(yaw)) * cos(radians(pitch))
    ))
