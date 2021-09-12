import datetime, uuid
from msgpack import Timestamp as msgpackTime
from enum import Enum, auto

def stampify(time : datetime.datetime):
    assert type(time) == datetime.datetime
    timestamp = time.timestamp()
    seconds =  int(timestamp // 1)
    nanoseconds = int(((timestamp - seconds) * 10**9) // 1)
    return (seconds, nanoseconds)

class ResponseCode(Enum):
    OK = auto()
    WARNING = auto()
    ERROR = auto()
    INFORMATION = auto()

class Message:
    def __init__(self, CmdID):
        self._CmdID = CmdID

    def toList(self):

        # TODO: This is probably a bad idea,
        # I should add CmdId somewhere else
        members = {**vars(self)}
        members.pop('_CmdID')

        return [self._CmdID, members]

    def __repr__(self):
        return f'{self.toList()}'

class ProtocolMessage:
    def __init__(self,
            ClientUID       : str,
            GDIOMsg         : Message,
            IsAsync         : bool = False,
        ):

        self.ClientUID = ClientUID
        self.RequestId = str(uuid.uuid4())
        self.CorrelationId = ''
        self.GDIOMsg = GDIOMsg
        self.IsAsync = IsAsync
        self.Timestamp : msgpackTime = msgpackTime(*stampify(datetime.datetime.now()))

    def toDict(self):
        self.GDIOMsg = self.GDIOMsg.toList()
        return vars(self)

    def __repr__(self):
        return f'{self.toDict()}'

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

