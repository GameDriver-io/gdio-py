
import datetime, uuid
from msgpack import Timestamp as msgpackTime

from collections import namedtuple

from msgpack.ext import Timestamp

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
        self.RequestId = str(uuid.uuid4())
        self.CorrelationId = '' if CorrelationId == None else CorrelationId
        self.GDIOMsg = GDIOMsg
        self.IsAsync = IsAsync
        self.Timestamp : msgpackTime = msgpackTime(*stampify(datetime.datetime.now())) if Timestamp == None else Timestamp
        
        if type(self.GDIOMsg) == list:
            for key, value in Messages.CmdIds.items():
                if value == self.GDIOMsg[0]:
                    messageType = getattr(Messages, key)
                    self.GDIOMsg = messageType(**self.GDIOMsg[1])
                    break
    
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

class SerializedObject:
    def __init__(self,
            SerializedObjectType : str = None,
            NonSerializedObject : object = None,
            SerializedObjectData : list = None,
            CustomSerialization : bool = False
        ):
        self.SerializedObjectType = SerializedObjectType
        self.NonSerializedObject = NonSerializedObject
        self.SerializedObjectData = SerializedObjectData
        self.CustomSerialization = CustomSerialization

    def pack(self):
        return vars(self)


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

Vector2 = namedtuple('Vector2', ['x', 'y'])
Vector3 = namedtuple('Vector3', ['x', 'y'])
Vector4 = namedtuple('Vector4', ['x', 'y'])

class Collision:
    pass

class AutoPlayDetails:
    def __init__(self, GCD = None, Addr = None) -> None:
        self.GCD = GameConnectionDetails() if GCD == None else GCD
        self.Addr = '' if Addr == None else Addr