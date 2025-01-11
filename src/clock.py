import logging
import math
from dataclasses import dataclass

from pyglfw import libapi as w

logger = logging.getLogger(__name__)


@dataclass
class Clock:
    current_time: float     # i timestamp
    last_time: float        # i-1 timestamp
    nbframes: int           # Frames counter

    timer_sec: float        # Milliseconds tracker
    sec_passed: bool        # = True in first frame from second passed

    fps: int                # Frames per second


def clock_create() -> Clock:
    return Clock(
        current_time=0.0,
        last_time=0.0,
        nbframes=0,
        timer_sec=0.0,
        sec_passed=False,
        fps=0,
    )


def clock_update(self: Clock) -> None:
    self.last_time = self.current_time
    self.current_time = w.glfwGetTime()

    delta = self.current_time - self.last_time

    self.nbframes += 1
    self.timer_sec += delta

    if self.timer_sec >= 1.0:
        self.sec_passed = True

        self.fps = math.ceil(self.nbframes / self.timer_sec)
        self.timer_sec -= 1.0
        self.nbframes = 0

    elif self.sec_passed:
        self.sec_passed = False
