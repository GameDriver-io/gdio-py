
import datetime, uuid
from msgpack import Timestamp as msgpackTime

from . import Messages

# I dont know where to put this method
stampify = lambda time: (int(time.timestamp() // 1), int(((time.timestamp() - int(time.timestamp() // 1)) * 10**9) // 1))

class ProtocolMessage:
    def __init__(self,
            ClientUID       : str,
            RequestId       : str = None,
            CorrelationId   : str = None,
            GDIOMsg         : Messages.Message = None,
            IsAsync         : bool = False,
            Timestamp       : msgpackTime = None
        ):

        self.ClientUID = ClientUID
        self.RequestId = str(uuid.uuid4()) if RequestId == None else RequestId
        self.CorrelationId = '' if CorrelationId == None else CorrelationId
        self.GDIOMsg = GDIOMsg
        self.IsAsync = IsAsync
        self.Timestamp : msgpackTime = msgpackTime(*stampify(datetime.datetime.now())) if Timestamp == None else Timestamp
        
        if type(self.GDIOMsg) == list:
            for key, value in Messages.CmdIds.items():
                if value == self.GDIOMsg[0]:
                    self.GDIOMsg = eval(f'Messages.{key}(**self.GDIOMsg[1])')
                    break
    
    def pack(self):
        return {
            'ClientUID' : self.ClientUID,
            'RequestId' : self.RequestId,
            'CorrelationId' : self.CorrelationId,
            'GDIOMsg' : self.GDIOMsg,
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

class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f'Vector3({self.x}, {self.y}, {self.z})'

class Vector4:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __repr__(self):
        return f'Vector4({self.x}, {self.y}, {self.z}, {self.w})'

class Collision:
    pass

class AutoPlayDetails:
    def __init__(self, GCD = None, Addr = None) -> None:
        self.GCD = GameConnectionDetails() if GCD == None else GCD
        self.Addr = '' if Addr == None else Addr