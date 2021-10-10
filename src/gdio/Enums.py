from enum import IntEnum, auto

class MouseButtons(IntEnum):
    LEFT = auto()
    RIGHT = auto()
    MIDDLE = auto()

class HandshakeState(IntEnum):
    NOT_STARTED = 0
    CLIENT_INFORMATION_SENT = 1
    COMPLETE = 2

class ResponseCode(IntEnum):
    OK = 0
    WARNING = 1
    ERROR = 2
    INFORMATION = 3

class HandshakeReasonCode(IntEnum):
    OK = 0
    ERROR = 1
    VERSION_MISMATCH = 2
    DUPLICATE_CLIENTUID = 3

class HookingObject(IntEnum):
    KEYBOARD = 1
    MOUSE = 2
    GAMEPAD = 4
    TOUCHINPUT = 8
    ALL = 0xF