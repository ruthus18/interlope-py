from __future__ import annotations

import logging

import imgui
from glm import vec3
from imgui.integrations import compute_fb_scale
from imgui.integrations.opengl import ProgrammablePipelineRenderer
from pyglfw import libapi as w

from .clock import Clock
from .input_ import KEY_ENTER
from .input_ import input_is_keypressed
from .scene import Scene
from .window import Window

logger = logging.getLogger(__name__)

gui_renderer: _GuiRenderer


GUI_KEYMAP = {
    imgui.KEY_TAB: w.GLFW_KEY_TAB,
    imgui.KEY_LEFT_ARROW: w.GLFW_KEY_LEFT,
    imgui.KEY_RIGHT_ARROW: w.GLFW_KEY_RIGHT,
    imgui.KEY_UP_ARROW: w.GLFW_KEY_UP,
    imgui.KEY_DOWN_ARROW: w.GLFW_KEY_DOWN,
    imgui.KEY_PAGE_UP: w.GLFW_KEY_PAGE_UP,
    imgui.KEY_PAGE_DOWN: w.GLFW_KEY_PAGE_DOWN,
    imgui.KEY_HOME: w.GLFW_KEY_HOME,
    imgui.KEY_END: w.GLFW_KEY_END,
    imgui.KEY_INSERT: w.GLFW_KEY_INSERT,
    imgui.KEY_DELETE: w.GLFW_KEY_DELETE,
    imgui.KEY_BACKSPACE: w.GLFW_KEY_BACKSPACE,
    imgui.KEY_SPACE: w.GLFW_KEY_SPACE,
    imgui.KEY_ENTER: w.GLFW_KEY_ENTER,
    imgui.KEY_ESCAPE: w.GLFW_KEY_ESCAPE,
    imgui.KEY_PAD_ENTER: w.GLFW_KEY_KP_ENTER,
    imgui.KEY_A: w.GLFW_KEY_A,
    imgui.KEY_C: w.GLFW_KEY_C,
    imgui.KEY_V: w.GLFW_KEY_V,
    imgui.KEY_X: w.GLFW_KEY_X,
    imgui.KEY_Y: w.GLFW_KEY_Y,
    imgui.KEY_Z: w.GLFW_KEY_Z,
}


class _GuiRenderer(ProgrammablePipelineRenderer):

    def __init__(self, window: Window):
        super().__init__()
        self.window = window

        self.io.display_size = w.glfwGetFramebufferSize(self.window)

        self.io.get_clipboard_text_fn = \
            lambda: w.glfwGetClipboardString(self.window)

        self.io.set_clipboard_text_fn = \
            lambda text: w.glfwSetClipboardString(self.window, text)

        self._map_keys()
        self._gui_time = None

        self.font_common, self.font_editor = self.load_fonts()

    def load_fonts(self) -> ...:
        font_ui = self.io.fonts.add_font_from_file_ttf(
            'assets/fonts/BerkeleyMono-Bold.ttf', 22
        )
        font_editor = self.io.fonts.add_font_from_file_ttf(
            'assets/fonts/BerkeleyMono-Regular.ttf', 16
        )
        self.refresh_font_texture()
        return font_ui, font_editor

    def _map_keys(self):
        for key, value in GUI_KEYMAP.items():
            self.io.key_map[key] = value

    def process_inputs(self):
        io = imgui.get_io()

        window_size = w.glfwGetWindowSize(self.window)
        fb_size = w.glfwGetFramebufferSize(self.window)

        io.display_size = window_size
        io.display_fb_scale = compute_fb_scale(window_size, fb_size)
        io.delta_time = 1.0 / 60

        if w.glfwGetWindowAttrib(self.window, w.GLFW_FOCUSED):
            io.mouse_pos = w.glfwGetCursorPos(self.window)
        else:
            io.mouse_pos = -1, -1

        io.mouse_down[0] = w.glfwGetMouseButton(self.window, 0)
        io.mouse_down[1] = w.glfwGetMouseButton(self.window, 1)
        io.mouse_down[2] = w.glfwGetMouseButton(self.window, 2)

        current_time = w.glfwGetTime()

        if self._gui_time:
            self.io.delta_time = current_time - self._gui_time
        else:
            self.io.delta_time = 1. / 60.

        if (io.delta_time <= 0.0):
            io.delta_time = 1.0 / 1000.0

        self._gui_time = current_time


def gui_init(window: Window) -> None:
    imgui.create_context()
    global gui_renderer
    gui_renderer = _GuiRenderer(window)


def gui_on_keyboard(window, key, scancode, action, mods):
    io = gui_renderer.io

    if action == w.GLFW_PRESS:
        io.keys_down[key] = True
    elif action == w.GLFW_RELEASE:
        io.keys_down[key] = False

    io.key_ctrl = (
        io.keys_down[w.GLFW_KEY_LEFT_CONTROL] or
        io.keys_down[w.GLFW_KEY_RIGHT_CONTROL]
    )
    io.key_alt = (
        io.keys_down[w.GLFW_KEY_LEFT_ALT] or
        io.keys_down[w.GLFW_KEY_RIGHT_ALT]
    )
    io.key_shift = (
        io.keys_down[w.GLFW_KEY_LEFT_SHIFT] or
        io.keys_down[w.GLFW_KEY_RIGHT_SHIFT]
    )
    io.key_super = (
        io.keys_down[w.GLFW_KEY_LEFT_SUPER] or
        io.keys_down[w.GLFW_KEY_RIGHT_SUPER]
    )


def gui_on_window_resize(window, width, height):
    gui_renderer.io.display_size = width, height


def gui_on_char(window, char):
    # io = imgui.get_io()
    io = gui_renderer.io

    if 0 < char < 0x10000:
        io.add_input_character(char)


def gui_on_scroll(window, x_offset, y_offset):
    io = gui_renderer.io

    io.mouse_wheel_horizontal = x_offset
    io.mouse_wheel = y_offset


def gui_process_input():
    gui_renderer.process_inputs()


def gui_is_keypressed(key) -> bool:
    window = gui_renderer.window
    return input_is_keypressed(window, key)


def gui_on_draw(clock: Clock, scene: Scene) -> None:
    imgui.new_frame()

    gui_draw_fps_counter(clock)
    gui_draw_scene_editor(scene)

    with imgui.font(gui_renderer.font_editor):
        imgui.show_test_window()

    imgui.render()
    gui_renderer.render(imgui.get_draw_data())


def gui_draw_fps_counter(clock: Clock) -> None:
    imgui.begin('FPS Counter', True, (
        imgui.WINDOW_NO_TITLE_BAR |
        imgui.WINDOW_NO_RESIZE |
        imgui.WINDOW_NO_MOVE |
        imgui.WINDOW_NO_BACKGROUND
    ))
    with imgui.font(gui_renderer.font_common):
        imgui.text(str(clock.fps))

    imgui.end()


def gui_draw_scene_editor(scene: Scene) -> None:
    imgui.begin('Scene', True, (
        imgui.WINDOW_MENU_BAR |
        imgui.WINDOW_NO_MOVE |
        imgui.WINDOW_NO_COLLAPSE
    ))

    with imgui.font(gui_renderer.font_editor):
        for obj in scene.objects:
            node = imgui.tree_node(
                f'[{obj.id:#05x}] {obj.ptr.id}',
                imgui.TREE_NODE_BULLET,
            )
            if node:
                imgui.text(f'Object Name: {obj.ptr.name}')

                new, is_active = imgui.checkbox('Active', obj.is_active)
                if new:
                    obj.is_active = is_active

                new, pos = imgui.input_float3('Position', *obj.position)
                if new and gui_is_keypressed(KEY_ENTER):
                    obj.position = vec3(pos)

                new, rot = imgui.input_float3('Rotation', *obj.rotation)
                if new and gui_is_keypressed(KEY_ENTER):
                    obj.rotation = vec3(rot)

                new, sc = imgui.input_float3('Scale', *obj.scale)
                if new and gui_is_keypressed(KEY_ENTER):
                    obj.scale = vec3(sc)

                imgui.tree_pop()

        # imgui.tree_node(
        #     f'[LIGHT] Lamp',
        #     imgui.TREE_NODE_BULLET,
        # )

    imgui.end()
