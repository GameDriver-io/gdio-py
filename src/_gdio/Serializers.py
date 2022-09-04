from inspect import isbuiltin
from _gdio import GDObjects
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


class DefaultSerializer:
    @staticmethod
    def Pack(obj: object) -> dict:
        if obj.__module__ == GDObjects.__name__:
            return vars(obj)

        elif IsBuiltin(obj):
            return obj

    @staticmethod
    def Unpack(obj: object) -> object:
        if obj.__module__ == GDObjects.__name__:
            return obj.from_dict(obj)


    @staticmethod
    def GetType(obj) -> str:

        if isbuiltin(obj):
            return None

        elif obj.__module__ == GDObjects.__name__:
            return f'gdio.common.objects.{obj.__class__.__name__}, gdio.common.objects, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null'