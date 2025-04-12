from typing import TypedDict
from overlay_lib import RgbaColor

# should probably be a tuple
type Coordinate = list[int]
type Coordinates = list[Coordinate]

class Location(TypedDict):
    label: list[str]
    elite: Coordinates
    chests: Coordinates
    urns: Coordinates
    shrines: Coordinates
    color: RgbaColor
    outline: RgbaColor

# each difficulty has multiple locations
type Versions = dict[int, Location]

class Maps(TypedDict):
    inferno: Versions
    purgatorio: Versions
