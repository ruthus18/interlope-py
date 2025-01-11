import typing as t
from dataclasses import dataclass

from .assets import AssetStorage
from .assets import assets_load_from_db
from .camera import MovementController
from .camera import camera_control
from .clock import Clock
from .clock import clock_create
from .clock import clock_update
from .db import Database
from .db import db_create
from .gfx import GfxInstance
from .gfx import gfx_create
from .gfx import gfx_log_info
from .gfx import gfx_should_stop
from .gfx import gfx_stop
from .gui import *
from .input_ import *
from .logging_ex import logging_init
from .scene import Scene
from .scene import scene_draw
from .scene import scene_load_from_config
from .window import WCallbackType
from .window import on_char_wrapper
from .window import on_keyboard_wrapper
from .window import on_scroll_wrapper
from .window import on_window_resize_wrapper
from .window import window_close
from .window import window_create
from .window import window_is_cursor_visible
from .window import window_poll_events
from .window import window_set_callback
from .window import window_set_cursor_visible
from .window import window_should_close
from .window import window_swap_buffers
from .world import World
from .world import world_load_from_db


@dataclass
class Engine:
    window: Window
    gfx: GfxInstance
    clock: Clock
    db: Database
    assets: AssetStorage
    world: World
    scene: Scene

    is_editor_visible: bool = True


e: Engine


def engine_create() -> Engine:
    logging_init()

    window = window_create()
    gfx = gfx_create()
    clock = clock_create()

    window_set_callback(window, WCallbackType.keyboard, on_keyboard)
    window_set_callback(window, WCallbackType.window_resize, on_window_resize)
    window_set_callback(window, WCallbackType.char, on_char)
    window_set_callback(window, WCallbackType.scroll, on_scroll)

    input_init(window)    
    gui_init(window)

    db = db_create()
    assets = assets_load_from_db(db, gfx)
    world = world_load_from_db(db, assets)
    scene = scene_load_from_config(world)

    gfx_log_info()

    # TODO engine state management (menu, scene, editor)
    window_set_cursor_visible(window, False)

    engine = Engine(
        window=window,
        gfx=gfx,
        clock=clock,
        db=db,
        assets=assets,
        world=world,
        scene=scene,
    )
    global e
    e = engine
    return engine


def engine_should_stop(self: Engine) -> bool:
    return gfx_should_stop() or window_should_close(self.window)


def engine_run_draw_loop(self: Engine, on_draw: t.Callable) -> None:
    while not engine_should_stop(self):
        clock_update(self.clock)
        window_poll_events()
        input_update_keyboard()
        input_update_mouse(self.window)
        on_draw()

        engine_handle_controllers(self)
        scene_draw(self.scene, self.gfx)

        if window_is_cursor_visible(self.window):
            gui_process_input()

        if self.is_editor_visible:
            gui_on_draw(self.clock, self.scene)

        window_swap_buffers(self.window)


def engine_handle_controllers(self: Engine) -> None:
    if not window_is_cursor_visible(self.window):
        camera_control(
            MovementController(
                input_is_keypressed(self.window, KEY_W),
                input_is_keypressed(self.window, KEY_S),
                input_is_keypressed(self.window, KEY_A),
                input_is_keypressed(self.window, KEY_D),
            ),
            input_get_mouse_delta(),
        )


def engine_close(self: Engine):
    logger.info('See you')
    window_close(self.window)


@on_keyboard_wrapper
def on_keyboard(window, key, scancode, action, mods) -> None:
    if window_is_cursor_visible(window):
        gui_on_keyboard(window, key, scancode, action, mods)

    if action == w.GLFW_RELEASE:
        return

    if key == KEY_ESC:
        gfx_stop()

    if key == KEY_TILDA:
        cursor = not window_is_cursor_visible(window)
        window_set_cursor_visible(window, cursor)

    if key == KEY_F1:
        e.is_editor_visible = not e.is_editor_visible


@on_window_resize_wrapper
def on_window_resize(window, width, height) -> None:
    # TODO: Recalc perspective matrix and other stuff
    gui_on_window_resize(window, width, height)


@on_scroll_wrapper
def on_scroll(window, x_offset, y_offset) -> None:
    gui_on_scroll(window, x_offset, y_offset)


@on_char_wrapper
def on_char(window, char) -> None:
    gui_on_char(window, char)
