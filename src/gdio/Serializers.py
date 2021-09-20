from . import Objects, Requests, Responses

import msgpack

def customSerializer(obj):
    if isinstance(obj, Objects.ProtocolMessage):
        return obj.pack()
    