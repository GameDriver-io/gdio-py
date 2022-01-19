from gdio.plugin import CustomSerializer
import msgpack

class Color:
    def __init__(self, r, g, b, a) -> None:
        self.r = r
        self.g = g
        self.b = b
        self.a = a

class Serializer(CustomSerializer):

    @classmethod
    def pack(cls, obj : Color):
        if isinstance(obj, Color):
            ret = {
                'r': obj.r,
                'g': obj.g,
                'b': obj.b,
                'a': obj.a
            }

        return msgpack.packb(ret)

    @classmethod
    def unpack(cls, obj : Color):
        unpacked = msgpack.unpackb(obj)
        if isinstance(obj, Color):
            ret = Color(unpacked['r'], unpacked['g'], unpacked['b'], unpacked['a'])

        return ret