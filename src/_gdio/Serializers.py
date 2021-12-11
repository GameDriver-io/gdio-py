from . import ProtocolObjects, Messages

import msgpack

def IsBuiltin(obj):
    return obj.__class__.__module__ == 'builtins'

class CustomSerializer:
    def Serialize(self, obj):
        pass
    def Deserialize(self, obj):
        pass

class SerializedObject:
    def __init__(self,
            SerializedObjectType : type = None,
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


def customSerializer(obj):
    if isinstance(obj, ProtocolObjects.ProtocolMessage):
        obj.GDIOMsg = obj.GDIOMsg.pack()
        return obj.pack()
    