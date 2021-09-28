import datetime, uuid
from msgpack import Timestamp as msgpackTime
from enum import IntEnum, auto
from . import Requests

## TODO: This whole file seems like a bad idea

def stampify(time : datetime.datetime):
    assert type(time) == datetime.datetime
    timestamp = time.timestamp()
    seconds =  int(timestamp // 1)
    nanoseconds = int(((timestamp - seconds) * 10**9) // 1)
    return (seconds, nanoseconds)

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

class Message:
    def __init__(self):
        pass

    def GetName(self):
        return f'{self.__class__.__name__}'

    def pack(self):
        return [Requests.CmdIds[self.__class__.__name__], vars(self)]

class ProtocolMessage:
    def __init__(self,
            ClientUID       : str,
            RequestId       : str = None,
            CorrelationId   : str = None,
            GDIOMsg         : Message = None,
            IsAsync         : bool = False,
            Timestamp       : msgpackTime = None
        ):

        self.ClientUID = ClientUID
        self.RequestId = str(uuid.uuid4()) if RequestId == None else RequestId
        self.CorrelationId = '' if CorrelationId == None else CorrelationId
        self.GDIOMsg = GDIOMsg
        self.IsAsync = IsAsync
        self.Timestamp : msgpackTime = msgpackTime(*stampify(datetime.datetime.now())) if Timestamp == None else Timestamp
    
    def pack(self):
        return {
            'ClientUID' : self.ClientUID,
            'RequestId' : self.RequestId,
            'CorrelationId' : self.CorrelationId,
            'GDIOMsg' : self.GDIOMsg.pack(),
            'IsAsync' : self.IsAsync,
            'Timestamp' : self.Timestamp
        }

    def __repr__(self):
        return f'{self.pack()}'

class RequestInfo:
    def __init__(self, client, requestId, sentTimestamp):
        self.Client = client
        self.RequestId = requestId
        self.SentTimestamp = sentTimestamp

    def toDict(self):
        return vars(self)

    def __repr__(self):
        return f'{self.toDict()}'

class GameConnectionDetails:
    def __init__(self,
    # TODO: NO MUTABLE DEFAULTS!!!
            Addr = '',
            Port = 0,
            GamePath = '',
            IsEditor = False,
            Platform = '',
        ):
        self.Addr = Addr
        self.Port = Port
        self.GamePath = GamePath
        self.IsEditor = IsEditor
        self.Platform = Platform

    def toDict(self):
        return vars(self)

    def __repr__(self):
        return f'{self.toDict()}'

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Vector2({self.x}, {self.y})'

class MouseButtons(IntEnum):
    LEFT = auto()
    RIGHT = auto()
    MIDDLE = auto()

class Collision:
    pass