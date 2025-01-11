import logging
from dataclasses import dataclass

from glm import vec2
from pyglfw import libapi as w

from .config import config
from .window import Window

logger = logging.getLogger(__name__)


@dataclass
class InputState:
    mouse_x: float
    mouse_y: float
    mouse_delta: vec2

    _first: bool = True  # FIXME no way...


state: InputState


def input_init(window: Window) -> None:
    upd_mouse_x, upd_mouse_y = w.glfwGetCursorPos(window)

    global state
    state = InputState(
        mouse_x=upd_mouse_x,
        mouse_y=upd_mouse_y,
        mouse_delta=vec2(0),
    )


def input_is_keypressed(window: Window, key: int) -> bool:
    return (w.glfwGetKey(window, key) == w.GLFW_PRESS)


def input_update_keyboard() -> None:
    w.glfwPollEvents()


def input_update_mouse(window: Window) -> None:
    upd_mouse_x, upd_mouse_y = w.glfwGetCursorPos(window)

    global state
    delta_x = (upd_mouse_x - state.mouse_x) / config.WINDOW_WIDTH
    delta_y = (upd_mouse_y - state.mouse_y) / config.WINDOW_HEIGHT

    # FIXME
    # Temporary solution to fix camera random moving at first frame
    if not state._first:
        state.mouse_delta = vec2(delta_x, delta_y)
    else:
        # Just skip first iteration and mark that
        # we are REALLY ready to update mouse delta :)
        state._first = False

    state.mouse_x = upd_mouse_x
    state.mouse_y = upd_mouse_y


def input_get_mouse_delta() -> vec2:
    return state.mouse_delta


# -- Keycodes
#
KEY_ESC = w.GLFW_KEY_ESCAPE
KEY_TILDA = w.GLFW_KEY_GRAVE_ACCENT
KEY_ENTER = w.GLFW_KEY_ENTER

KEY_A = w.GLFW_KEY_A
KEY_B = w.GLFW_KEY_B
KEY_C = w.GLFW_KEY_C
KEY_D = w.GLFW_KEY_D
KEY_E = w.GLFW_KEY_E
KEY_F = w.GLFW_KEY_F
KEY_G = w.GLFW_KEY_G
KEY_H = w.GLFW_KEY_H
KEY_I = w.GLFW_KEY_I
KEY_J = w.GLFW_KEY_J
KEY_K = w.GLFW_KEY_K
KEY_L = w.GLFW_KEY_L
KEY_M = w.GLFW_KEY_M
KEY_N = w.GLFW_KEY_N
KEY_O = w.GLFW_KEY_O
KEY_P = w.GLFW_KEY_P
KEY_Q = w.GLFW_KEY_Q
KEY_R = w.GLFW_KEY_R
KEY_S = w.GLFW_KEY_S
KEY_T = w.GLFW_KEY_T
KEY_U = w.GLFW_KEY_U
KEY_V = w.GLFW_KEY_V
KEY_W = w.GLFW_KEY_W
KEY_X = w.GLFW_KEY_X
KEY_Y = w.GLFW_KEY_Y
KEY_Z = w.GLFW_KEY_Z

KEY_1 = w.GLFW_KEY_1
KEY_2 = w.GLFW_KEY_2
KEY_3 = w.GLFW_KEY_3
KEY_4 = w.GLFW_KEY_4
KEY_5 = w.GLFW_KEY_5
KEY_6 = w.GLFW_KEY_6
KEY_7 = w.GLFW_KEY_7
KEY_8 = w.GLFW_KEY_8
KEY_9 = w.GLFW_KEY_9
KEY_0 = w.GLFW_KEY_0

KEY_F1 = w.GLFW_KEY_F1
KEY_F2 = w.GLFW_KEY_F2
KEY_F3 = w.GLFW_KEY_F3
KEY_F4 = w.GLFW_KEY_F4
KEY_F5 = w.GLFW_KEY_F5
KEY_F6 = w.GLFW_KEY_F6
KEY_F7 = w.GLFW_KEY_F7
KEY_F8 = w.GLFW_KEY_F8
KEY_F9 = w.GLFW_KEY_F9
KEY_F10 = w.GLFW_KEY_F10
KEY_F11 = w.GLFW_KEY_F11
KEY_F12 = w.GLFW_KEY_F12
