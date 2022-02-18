from gdio.plugin import CustomSerializer
import msgpack

class CustomColor:
    def __init__(self, r, g, b, a) -> None:
        self.m_R = r
        self.m_g = g
        self.m_b = b
        self.m_a = a

class Serializer(CustomSerializer):

    @staticmethod
    def Pack(obj : CustomColor):
        if isinstance(obj, CustomColor):
            ret = f'CustomColor:{obj.m_R}|{obj.m_g}|{obj.m_b}|{obj.m_a}'

        return msgpack.packb(ret)

    @staticmethod
    def Unpack(obj):
        unpacked = msgpack.unpackb(obj)
        if '$CustomColor' in unpacked:
            ret = CustomColor(unpacked['r'], unpacked['g'], unpacked['b'], unpacked['a'])

        return ret