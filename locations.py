from typing import TypedDict
from overlay_lib import RgbaColor, Vector2D

class LocationDict(TypedDict):
    label: list[str]
    elite: list[Vector2D]
    chests: list[Vector2D]
    urns: list[Vector2D]
    alter: list[Vector2D]
    color: RgbaColor
    outline: RgbaColor

# easier to do this for now than convert the data
class Location:
    def __init__(self, location: LocationDict):
        self.label = location["label"]
        self.elite = location["elite"]
        self.chests = location["chests"]
        self.urns = location["urns"]
        self.alter = location["alter"]
        self.color = location["color"]
        self.outline = location["outline"]

# each difficulty has multiple locations
type Versions = dict[int, Location]

class Maps(TypedDict):
    inferno: Versions
    purgatorio: Versions

purple_4k: LocationDict = {
    "label": ["inferno"],
    "elite": [
        Vector2D(1217, 312),
        Vector2D(2889, 762),
        Vector2D(1715, 1158),
    ],
    "chests": [
        Vector2D(2156, 517),
        Vector2D(2695, 603),
        Vector2D(862, 649),
        Vector2D(1512, 744),
        Vector2D(1183, 858),
        Vector2D(2516, 1001),
        Vector2D(888, 1069),
        Vector2D(2204, 1189),
        Vector2D(3116, 1210),
        Vector2D(1338, 1292),
        Vector2D(2524, 1461),
        Vector2D(516, 1468),
        Vector2D(1975, 1509),
        Vector2D(3001, 1656),
        Vector2D(997, 1807),
    ],
    "urns": [
        Vector2D(829, 441),
        Vector2D(2883, 521),
        Vector2D(2373, 570),
        Vector2D(1161, 570),
        Vector2D(1683, 573),
        Vector2D(3004, 703),
        Vector2D(2103, 822),
        Vector2D(875, 907),
        Vector2D(2963, 1009),
        Vector2D(1587, 1028),
        Vector2D(2043, 1051),
        Vector2D(2323, 1280),
        Vector2D(901, 1314),
        Vector2D(1862, 1347),
        Vector2D(1412, 1474),
        Vector2D(2666, 1487),
        Vector2D(1629, 1564),
        Vector2D(1035, 1596),
        Vector2D(2130, 1719),
    ],
    "alter": [Vector2D(1916, 549), Vector2D(1226, 1062), Vector2D(2634, 1139), Vector2D(1555, 425)],
    "alter": [],
    "color": RgbaColor(120, 95, 240, 126),
    "outline": RgbaColor(120, 95, 240, 255),
}

magenta_4k: LocationDict = {
    "label": ["inferno"],
    "elite": [Vector2D(2423, 517), Vector2D(516, 1470), Vector2D(3125, 1795)],
    "chests": [
        Vector2D(1217, 313),
        Vector2D(708, 373),
        Vector2D(1915, 485),
        Vector2D(2455, 830),
        Vector2D(3079, 1005),
        Vector2D(2056, 1050),
        Vector2D(889, 1071),
        Vector2D(2368, 1306),
        Vector2D(1856, 1380),
        Vector2D(2749, 1535),
        Vector2D(1596, 1621),
        Vector2D(2153, 1793),
        Vector2D(997, 1809),
    ],
    "urns": [],
    "alter": [Vector2D(252, 246)],
    "color": RgbaColor(220, 38, 127, 126),
    "outline": RgbaColor(220, 38, 127, 255),
}

yellow_4k: LocationDict = {
    "label": ["inferno"],
    "elite": [Vector2D(1184, 861), Vector2D(2712, 1141), Vector2D(1596, 1620)],
    "chests": [
        Vector2D(708, 373),
        Vector2D(1078, 517),
        Vector2D(1657, 519),
        Vector2D(2889, 763),
        Vector2D(2455, 830),
        Vector2D(759, 890),
        Vector2D(2056, 1050),
        Vector2D(3116, 1213),
        Vector2D(1339, 1295),
        Vector2D(2368, 1306),
        Vector2D(1974, 1510),
        Vector2D(936, 1656),
        Vector2D(3001, 1657),
    ],
    "urns": [],
    "alter": [Vector2D(1288, 824)],
    "color": RgbaColor(76, 255, 0, 126),
    "outline": RgbaColor(76, 255, 0, 255),
}

inferno: Versions = {
    0: Location(purple_4k),
    1: Location(magenta_4k),
    2: Location(yellow_4k),
}
purgatorio: Versions = {
    0: Location(purple_4k),
    1: Location(magenta_4k),
    2: Location(yellow_4k),
}

data: Maps = {"inferno": inferno, "purgatorio": purgatorio}
