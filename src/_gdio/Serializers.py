from . import ProtocolObjects

import msgpack

def IsBuiltin(obj):
    return obj.__class__.__module__ == 'builtins'

class CustomSerializer:
    @staticmethod
    def Pack(obj):
        raise NotImplementedError

    @staticmethod
    def Unpack(obj):
        raise NotImplementedError

def msgSerialize(obj):
    if isinstance(obj, ProtocolObjects.ProtocolMessage):
        return obj.pack()

def msgDeserialize(obj):
    if isinstance(obj, msgpack.Timestamp):
        return obj.to_unix()