import enum
import typing as t

from pyglfw import libapi as w
from pyglfw.libapi.c_helper import GLFWwindow as Window

from .config import config


class WCallbackType(enum.StrEnum):
    keyboard = enum.auto()
    window_resize = enum.auto()
    char = enum.auto()
    scroll = enum.auto()


on_keyboard_wrapper = w.GLFWkeyfun
on_window_resize_wrapper = w.GLFWwindowsizefun
on_char_wrapper = w.GLFWcharfun
on_scroll_wrapper = w.GLFWscrollfun


def window_create() -> Window:
    if not w.glfwInit():
        raise RuntimeError('Could not initialize GLFW')

    w.glfwWindowHint(w.GLFW_CONTEXT_VERSION_MAJOR, 4)
    w.glfwWindowHint(w.GLFW_CONTEXT_VERSION_MINOR, 6)
    w.glfwWindowHint(w.GLFW_OPENGL_PROFILE, w.GLFW_OPENGL_CORE_PROFILE)

    if config.WINDOW_BORDER == False:
        w.glfwWindowHint(w.GLFW_DECORATED, False)

    if config.WINDOW_FULLSC:
        monitor = w.glfwGetPrimaryMonitor()
    else:
        monitor = None

    # TODO: set window position and monitor
    window = w.glfwCreateWindow(
        config.WINDOW_WIDTH,
        config.WINDOW_HEIGHT,
        config.WINDOW_TITLE.encode(),
        monitor,
        None,  # share
    )
    w.glfwSetWindowPos(window, *config.WINDOW_POS)

    w.glfwMakeContextCurrent(window)
    w.glfwSwapInterval(1)  # V-Sync

    return window


def window_poll_events() -> None:
    w.glfwPollEvents()


def window_swap_buffers(window: Window) -> None:
    w.glfwSwapBuffers(window)  # draw content (V-Sync)


def window_should_close(window: Window) -> bool:
    return w.glfwWindowShouldClose(window)


def window_close(window: Window) -> None:
    w.glfwDestroyWindow(window)
    w.glfwTerminate()


def window_set_callback(
    window: Window,
    type: WCallbackType,
    callback: t.Callable,
) -> None:
    match type:
        case WCallbackType.keyboard:
            w.glfwSetKeyCallback(window, callback)

        case WCallbackType.window_resize:
            w.glfwSetWindowSizeCallback(window, callback)

        case WCallbackType.char:
            w.glfwSetCharCallback(window, callback)

        case WCallbackType.scroll:
            w.glfwSetScrollCallback(window, callback)

        case _:
            raise RuntimeError


def window_is_cursor_visible(window: Window) -> bool:
    return w.glfwGetInputMode(window, w.GLFW_CURSOR) == w.GLFW_CURSOR_NORMAL


def window_set_cursor_visible(window: Window, is_visible: bool) -> None:
    mode = w.GLFW_CURSOR_NORMAL if is_visible else w.GLFW_CURSOR_DISABLED

    w.glfwSetInputMode(window, w.GLFW_CURSOR, mode)
