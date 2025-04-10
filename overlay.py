import threading
# import pygame
import overlay_lib
from overlay_lib import Vector2D, RgbaColor, FlDrawRect, FlDrawCircle, DrawText

from helper import HiddenPrints
from locations import purple, magenta, yellow

# lmao why does this work?
with HiddenPrints():
    import pygame

# keys map to XboxController.version
data = {
    0: purple,
    1: magenta,
    2: yellow,
}
pygame.init()
joysticks = []
clock = pygame.time.Clock()
keepPlaying = True

# idk why this is necessary but trying to just call 
# pygame.joystick.Joystick(i).init() doesn't work
# I guess the object needs to persist somewhere?
for i in range(0, pygame.joystick.get_count()):
    # create an Joystick object in our list
    joysticks.append(pygame.joystick.Joystick(i))
    # initialize the appended joystick
    joysticks[-1].init()

# this is the value for how many pixels your map is offset
x_offset = 530
y_offset = 290

# don't change this
x_small = 140
y_small = 70

# if it doesn't work just play with this. calculating it is probably slower
# ratio = 1.78
ratio = 1

size = 20

# transform the coordinates using the constants
def transform(coord):
    x = x_offset + ratio*(coord[0]-x_small)
    y = y_offset + ratio*(coord[1]-y_small)
    return [
        round(x),
        round(y),
    ]

version = 0


class XboxController():
    def __init__(self):
        # control which version of the map to show
        self.version = 0
        self.VersionPressed = False

        self.AxisX = 0
        self.PrevAxisX = 0
        self.LeftTrigger = -1

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def _monitor_controller(self):
        while True:
            for event in pygame.event.get():
                if "hat" in event.dict:
                    [self.AxisX, y] = event.dict["value"]
                elif "axis" in event.dict and event.dict["axis"] == 4:
                    self.LeftTrigger = event.dict["value"]

    def update(self):
        # this means it's being held
        if self.AxisX == self.PrevAxisX:
            return self.version
        
        self.PrevAxisX = self.AxisX
        if self.AxisX == 1:
            self.version = (self.version + 1) % 3
        if self.AxisX == -1:
            self.version = (self.version - 1) % 3

        return self.version

joy = XboxController()

def callback():
    version = joy.update()

    # number is from trial and error. might be just my controller
    # seems to be the closest for the xbox controller to show at the same time as map open
    if joy.LeftTrigger > 0:
        color = data[version]['color']
        curr =  data[version]

        result = []

        for i in range(len(curr['label'])):
            text = data[version]['label'][i]
            result.append(
            DrawText(Vector2D(x_offset, y_offset+36*i), 8, text ,"Times", color, 10)
            )


        chests = map(transform, data[version]['chests'])
        elites = map(transform, data[version]['elite'])
        for coord in chests:
            result.append(
                FlDrawCircle(Vector2D(coord[0], coord[1]), size, color, color, 0)
            )

        for coord in elites:
            result.append(
                FlDrawRect(Vector2D(coord[0], coord[1]), size*2, size*2, color, color, 0)
            )
        return result
    return []

overlay = overlay_lib.Overlay(
    drawlistCallback=callback,
    # increase this if performance is an issue
    refreshTimeout=50
)

overlay.spawn()