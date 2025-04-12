from typing import NamedTuple
import overlay_lib
from overlay_lib import Vector2D, FlDrawRect, FlDrawCircle, DrawText
from controller import XboxController
from locations import Location, data


# don't change this
X_OFFSET = 375
Y_OFFSET = 200
OFFSET = Vector2D(375, 200)
FONT_SIZE = 12 # 8
FONT_HEIGHT = FONT_SIZE * 4 # this is a decent approximation

# if it doesn't work just play with this.
# i don't remember how to calculate it
# maybe your resolution / [3840, 2160]
ratio = Vector2D(1, 1)
# this is the value for how many pixels your map is offset
offset = Vector2D(375, 200)
size = 20


def transform(coord: Vector2D) -> Vector2D:
    x = offset.x + ratio.x * (coord.x - OFFSET.x)
    y = offset.y + ratio.y * (coord.y - OFFSET.y)
    return Vector2D(round(x), round(y))


version = 0

joy = XboxController(0, 3)

def callback() -> list:
    result = []

    state = joy.update()
    version = state.version
    enabled = state.enabled
    location = state.location

    curr = data[location][version]
    assert isinstance(curr, Location)

    color = curr.color
    outline = curr.outline
    # number is from trial and error. might be just my controller
    # seems to be the closest for the xbox controller to show at the same time as map open
    if joy.LeftTrigger > 0:
        if not enabled:
            return [DrawText(offset, FONT_SIZE, "disabled", "Times", color, 10)]

        text_offset = offset.y
        for i in range(len(curr.label)):
            text = curr.label[i]
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

        if len(curr.chests):
            text = f"{len(curr.chests)} chests"
            result.append(
                DrawText(Vector2D(offset.x, text_offset), FONT_SIZE, text, "Times", color, 10)
            )
            text_offset += FONT_HEIGHT

        if len(curr.elite):
            text = f"{len(curr.elite)} elites"
            result.append(
                DrawText(Vector2D(offset.x, text_offset), FONT_SIZE, text, "Times", color, 10)
            )
            text_offset += FONT_HEIGHT

        chests = map(transform, curr.chests)
        elites = map(transform, curr.elite)

        for coord in chests:
            result.append(
                FlDrawRect(
                    Vector2D(coord.x - size, coord.y - size),
                    size * 2,
                    size * 2,
                    color,
                    color,
                    0,
                )
            )

        for coord in elites:
            result.append(
                FlDrawCircle(coord, size, color, outline, 5)
            )

    return result


overlay = overlay_lib.Overlay(
    drawlistCallback=callback,
    # increase this if performance is an issue
    refreshTimeout=50,
)

def init():
    overlay.spawn()
