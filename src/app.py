import logging

from .engine import Engine
from .engine import engine_close
from .engine import engine_create
from .engine import engine_run_draw_loop
from .window import *

logger = logging.getLogger(__name__)


engine: Engine


def run_application():
    global engine
    engine = engine_create()

    # TODO: add user window callbacks (need support of adding multiple callbacks)
    engine_run_draw_loop(engine, on_draw)
    engine_close(engine)


# bed = None


# def on_draw():
#     global bed
#     if bed is None:
#         bed = [o for o in engine.scene.objects if o.ptr.id == 'bed01_single'][0]
    
#     delta = 0.8
#     if bed.rotation.y >= 360:
#         bed.rotation.y -= 360

#     bed.rotation.y += delta

def on_draw(): ...