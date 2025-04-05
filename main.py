import overlay_lib
from overlay_lib import Vector2D, RgbaColor, FlDrawRect, FlDrawCircle
from inputs import get_gamepad
import math
import threading

class XboxController(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):
        # control which version of the map to show
        self.version = 0
        self.VersionPressed = False

        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def left_trigger(self):
        return self.LeftTrigger

    def update(self):
        # update and check for both buttons being released
        if self.VersionPressed:
            self.VersionPressed = self.RightBumper or self.LeftBumper
            return self.version
        
        # only handle this when button is released and pressed again
        if self.RightBumper:
            self.version = (self.version + 1) % 3
            self.VersionPressed = True
        if self.LeftBumper:
            self.version = (self.version - 1) % 3
            self.VersionPressed = True
        return self.version


    def read(self): # return the buttons/triggers that you care about in this methode
        rb = self.RightBumper
        x = self.LeftJoystickX
        y = self.LeftJoystickY
        a = self.A
        b = self.X # b=1, x=2
        rb = self.RightBumper
        return [x, y, a, b, rb]


    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.Y = event.state #previously switched with X
                elif event.code == 'BTN_WEST':
                    self.X = event.state #previously switched with Y
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.LeftDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.RightDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.UpDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.DownDPad = event.state

# this is the value for how many pixels your map is offset
x_offset = 530
y_offset = 290

# don't change this
x_small = 140
y_small = 70

# if it doesn't work just play with this. calculating it is probably slower
ratio = 1.78

purple = {
    "elite": [
        [560, 128],
        [816, 555],
    ],
    "chests": [
        [385, 292],
        [380, 503],
        [548, 409],
        [713, 344],
        [639, 627],
        [213, 711],
        [444, 881],
        [1070, 569],
        [1040, 236],
        [1230, 701],
        [1414, 356],
        [1224, 472],
        [962, 734],
        [1315, 273],
        [1548, 581],
        [1478, 808],
        ],
    "urns": [],
    "shrines": [],
    "color": RgbaColor(120, 95, 240, 127),
}

magenta = {
    "elite": [
        [209, 712],
        [1176, 219],
        [1536, 872],
    ],
    "chests": [
        [298, 157],
        [560, 127],
        [405, 504],
        [761, 791],
        [890, 664],
        [972, 499],
        [921, 214],
        [1179, 384],
        [1137, 629],
        [1345, 747],
        [1511, 474]
        ],
    "urns": [],
    "shrines": [],
    "color": RgbaColor(220, 38, 127, 127),
}

yellow = {
    "elite": [
        [209, 712],
        [1176, 219],
        [1536, 872],
    ],
    "chests": [
        [298, 157],
        [560, 127],
        [405, 504],
        [761, 791],
        [890, 664],
        [972, 499],
        [921, 214],
        [1179, 384],
        [1137, 629],
        [1345, 747],
        [1511, 474]
        ],
    "urns": [],
    "shrines": [],
    "color": RgbaColor(230, 159, 0, 127),
}

# keys map to XboxController.version
data = {
    0: purple,
    1: magenta,
    2: yellow,
}

# transform the coordinates using the constants
def transform(coord):
    x = x_offset + ratio*(coord[0]-x_small)
    y = y_offset + ratio*(coord[1]-y_small)
    return [
        round(x),
        round(y),
    ]

joy = XboxController()

size = 20

def callback():
    version = joy.update()

    # number is from trial and error. might be just my controller
    # seems to be the closest for the xbox controller to show at the same time as map open
    if joy.left_trigger() > 0.524:
        result = []
        color = data[version]['color']

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
    refreshTimeout=10
)

overlay.spawn()