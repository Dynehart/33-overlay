from collections import namedtuple
import threading
from typing import NamedTuple
from helper import HiddenPrints

with HiddenPrints():
    # lmao why does this work?
    import pygame

    pygame.init()

class ControllerState(NamedTuple):
    enabled: bool
    location: str
    version: int

locations = ["inferno", "purgatorio"]

joysticks = []


class XboxController:
    def __init__(self, player: int, num_versions: int):
        # keep an array of all on hand but only reference one
        self.joysticks = []
        self.joystick_index = player

        # control which version of the map to show
        self.num_versions = num_versions
        self.version = 0
        self.AxisX = 0
        self.PrevAxisX = 0

        # control whether enabled or not
        self.enabled = True
        self.location = 0  # 0 for inferno, 1 for purg
        self.AxisY = 0
        self.PrevAxisY = 0

        self.LeftTrigger = -1

        self._monitor_thread = threading.Thread(
            target=self._monitor_controller, args=()
        )
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def _monitor_controller(self):
        while True:
            self.detect_joysticks()

            for event in pygame.event.get():
                if "hat" in event.dict:
                    [self.AxisX, self.AxisY] = event.dict["value"]
                elif "axis" in event.dict and event.dict["axis"] == 4:
                    self.LeftTrigger = event.dict["value"]

    def detect_joysticks(self):
        if len(self.joysticks) == 0:
            # idk why this is necessary but trying to just call
            # pygame.joystick.Joystick(i).init() doesn't work
            # I guess the object needs to persist somewhere?
            for i in range(0, pygame.joystick.get_count()):
                # create an Joystick object in our list
                self.joysticks.append(pygame.joystick.Joystick(i))
                # initialize the appended joystick
                self.joysticks[-1].init()
        elif len(self.joysticks) != pygame.joystick.get_count():
            self.joysticks = []

    def __update_state(self) -> None:
        # this means it's being held
        if self.AxisY == self.PrevAxisY:
            return

        self.PrevAxisY = self.AxisY
        if self.AxisY == 1:
            self.enabled = not self.enabled
        if self.AxisY == -1:
            self.location = (self.location + 1) % len(locations)

    def __update_version(self) -> None:
        # this means it's being held
        if self.AxisX == self.PrevAxisX:
            return

        self.PrevAxisX = self.AxisX
        if self.AxisX == 1:
            self.version = (self.version + 1) % self.num_versions
        if self.AxisX == -1:
            self.version = (self.version - 1) % self.num_versions

    def update(self) -> ControllerState:
        self.__update_state()
        self.__update_version()

        return ControllerState(
            enabled=self.enabled,
            location=locations[self.location],
            version=self.version,
        )


# keepPlaying = True
# clock = pygame.time.Clock()

# class Joystick:
#     def __init__(self):
#         self.joysticks = []

#     def detect_joysticks(self):
#         if len(self.joysticks) == 0:
#             # idk why this is necessary but trying to just call
#             # pygame.joystick.Joystick(i).init() doesn't work
#             # I guess the object needs to persist somewhere?
#             for i in range(0, pygame.joystick.get_count()):
#                 # create an Joystick object in our list
#                 self.joysticks.append(pygame.joystick.Joystick(i))
#                 # initialize the appended joystick
#                 self.joysticks[-1].init()
#         elif len(self.joysticks) != pygame.joystick.get_count():
#             self.joysticks = []
