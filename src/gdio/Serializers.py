from . import ProtocolObjects

import msgpack

def customSerializer(obj):
    if isinstance(obj, ProtocolObjects.ProtocolMessage):
        obj.GDIOMsg = obj.GDIOMsg.pack()
        return obj.pack()
    