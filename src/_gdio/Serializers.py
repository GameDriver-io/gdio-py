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
    def Pack(obj) -> dict:
        if isinstance(obj, GDObjects.Vector2):
            return {'x': obj.x, 'y': obj.y}

        if isinstance(obj, GDObjects.Vector3):
            return {'x': obj.x, 'y': obj.y, 'z': obj.z}

    @staticmethod
    def Unpack(obj) -> object:
        if isinstance(obj, dict):
            if 'x' in obj and 'y' in obj and len(obj) == 2:
                return GDObjects.Vector2(obj['x'], obj['y'])

            if 'x' in obj and 'y' in obj and 'z' in obj and len(obj) == 3:
                return GDObjects.Vector3(obj['x'], obj['y'], obj['z'])

    @staticmethod
    def GetType(obj) -> str:
        ret: str = ''

        if isbuiltin(obj):
            return None

        if isinstance(obj, GDObjects.Vector2):
            ret = 'gdio.common.objects.Vector2'

        elif isinstance(obj, GDObjects.Vector3):
            ret = 'gdio.common.objects.Vector3'

        elif isinstance(obj, GDObjects.Vector4):
            ret = 'gdio.common.objects.Vector4'

        return f'{ret}, gdio.common.objects, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null'