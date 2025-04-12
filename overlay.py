from typing import NamedTuple
import overlay_lib
from overlay_lib import Vector2D, FlDrawRect, FlDrawCircle, DrawText
from controller import XboxController
from locations import data

# class Vector2D(NamedTuple):
#     x: int
#     y: int

# don't change this
X_OFFSET = 375
Y_OFFSET = 200
OFFSET = Vector2D(375, 200)
FONT_SIZE = 12 # 8
FONT_HEIGHT = FONT_SIZE * 4 # this is a decent approximation

# keys map to XboxController.version

# joysticks = []

# def detect_joysticks():
#     if len(joysticks) == 0:
#         # idk why this is necessary but trying to just call
#         # pygame.joystick.Joystick(i).init() doesn't work
#         # I guess the object needs to persist somewhere?
#         for i in range(0, pygame.joystick.get_count()):
#             # create an Joystick object in our list
#             joysticks.append(pygame.joystick.Joystick(i))
#             # initialize the appended joystick
#             joysticks[-1].init()
# pygame.init()
# clock = pygame.time.Clock()
# keepPlaying = True


# we need to figure out where the map starts/ends for several aspect ratios
# 16:9 at 3840 has 375 and 3465
#         2160 has 200 and 1940
# 3840-375=3465
# with a ratio of 1/10.24 we can just


# if it doesn't work just play with this.
# i don't remember how to calculate it
# maybe your resolution / [3840, 2160]
ratio = Vector2D(1, 1)
# this is the value for how many pixels your map is offset
offset = Vector2D(375, 200)
size = 20


def transform(coord):
    x = offset.x + ratio.x * (coord[0] - OFFSET.x)
    y = offset.y + ratio.y * (coord[1] - OFFSET.y)
    return [round(x), round(y)]


version = 0

joy = XboxController(0, 3)

def callback() -> list:
    result = []

    state = joy.update()
    version = state.version
    enabled = state.enabled
    location = state.location

    curr = data[location][version]
    color = curr["color"]
    outline = curr["outline"]

    # number is from trial and error. might be just my controller
    # seems to be the closest for the xbox controller to show at the same time as map open
    if joy.LeftTrigger > 0:
        if not enabled:
            return [DrawText(offset, FONT_SIZE, "disabled", "Times", color, 10)]

        text_offset = offset.y
        for i in range(len(curr["label"])):
            text = curr["label"][i]
            result.append(
                DrawText(
                    Vector2D(offset.x, text_offset),
                    FONT_SIZE,
                    text,
                    "Times",
                    color,
                    10,
                )
            )
            text_offset += FONT_HEIGHT

        for key in curr:
            if key != "chests" and key != "elite":
                continue

            text = f"{len(curr[key])} {key}"
            result.append(
                DrawText(Vector2D(offset.x, text_offset), FONT_SIZE, text, "Times", color, 10)
            )
            text_offset += FONT_HEIGHT

        chests = map(transform, curr["chests"])
        elites = map(transform, curr["elite"])

        for coord in chests:
            result.append(
                FlDrawRect(
                    Vector2D(coord[0] - size, coord[1] - size),
                    size * 2,
                    size * 2,
                    color,
                    color,
                    0,
                )
            )

        for coord in elites:
            result.append(
                FlDrawCircle(Vector2D(coord[0], coord[1]), size, color, outline, 5)
            )

    return result


overlay = overlay_lib.Overlay(
    drawlistCallback=callback,
    # increase this if performance is an issue
    refreshTimeout=50,
)

overlay.spawn()
