from pprint import pprint
import overlay_lib
from overlay_lib import Vector2D, RgbaColor, FlDrawRect, FlDrawCircle, DrawText
from inputs import get_gamepad
import math
import threading
from locations import purple, magenta, yellow


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

    def read(self): # return the buttons/triggers that you care about in this methode
        a = self.DownDPad
        b = self.LeftDPad
        c = self.RightDPad
        d = self.UpDPad
        return [a,b,c,d]

    def left_trigger(self):
        return self.LeftTrigger

    def update(self):
        # update and check for both buttons being released
        if self.VersionPressed:
            self.VersionPressed = self.RightDPad or self.LeftDPad
            return self.version
        
        # only handle this when button is released and pressed again
        if self.RightDPad:
            self.version = (self.version + 1) % 3
            self.VersionPressed = True
        if self.LeftDPad:
            self.version = (self.version - 1) % 3
            self.VersionPressed = True
        return self.version

    def _monitor_controller(self):
        while True:
            try:
                events = get_gamepad()
            except:
                # sleep(1.0 / 30.0)
                continue

            for event in events:
                pprint(vars(event))
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
                    # ABS_HAT0X
                # elif event.code == 'BTN_TRIGGER_HAPPY1':
                elif event.code == 'ABS_HAT0X':
                    self.LeftDPad = event.state
                # elif event.code == 'BTN_TRIGGER_HAPPY2':
                elif event.code == 'ABS_HAT1X':
                    self.RightDPad = event.state
                # elif event.code == 'BTN_TRIGGER_HAPPY3':
                elif event.code == 'ABS_HAT0Y':
                    self.UpDPad = event.state
                # elif event.code == 'BTN_TRIGGER_HAPPY4':
                elif event.code == 'ABS_HAT1Y':
                    self.DownDPad = event.state

# keys map to XboxController.version
data = {
    0: purple,
    1: magenta,
    2: yellow,
}

# this is the value for how many pixels your map is offset
x_offset = 530
y_offset = 290

# don't change this
x_small = 140
y_small = 70

# if it doesn't work just play with this. calculating it is probably slower
ratio = 1.78

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