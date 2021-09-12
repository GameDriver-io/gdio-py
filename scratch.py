import binascii
from ctypes import *
import array
import msgpack, datetime
import Requests

buf = b'\x0C\x00\x00\x00\xA3\x1C\x29\x1C\x48\x65\x6C\x6C\x6F\x20\x57\x6F\x72\x6C\x64\x21'


class Crc32:

    def __init__(self):
        num = c_uint(3988292384)
        self.table = [c_uint()] * 256

        num2 = c_uint(0)
        num3 = c_uint(0)
        while num3.value < len(self.table):
            num2 = num3
            num4 = 8
            while num4 > 0:
                num2 = c_uint((num2.value >> 1) if (num2.value & 1) != 1 else (num2.value >> 1) ^ num.value)
                num4 -= 1
                self.table[num3.value] = num2
            num3 = c_uint(num3.value + 1)

    def ComputeChecksumBytes(self, buf):
        return c_uint(self.ComputeChecksum(buf)).value

    def ComputeChecksum(self, buf, byteLength = 0):
        num = len(buf) if byteLength == 0 else byteLength
        num2 = c_uint(4294967295)
        i = 0
        while i < num:
            b = c_uint((num2.value & 0xFF) ^ buf[i])
            num2 = c_uint((num2.value >> 8) ^ self.table[b.value].value)
            i += 1
        return ~num2.value

def ConstructPayload(msg):
    payload = [0x00] * (4 + 4 + len(msg))
    crc = Crc32()
    crcHash = crc.ComputeChecksumBytes(bytes(msg))
    print(sourceArray.to_bytes(4, 'little'))

    for i in range(len(list(len(msg).to_bytes(4, 'little')))):
        array[i] = list(len(msg).to_bytes(4, 'little'))[i]

    
def payloadTest():
    print(buf)
    ConstructPayload(b'Hello World!')

def spans():
    SerializedObjectType = [180, 83, 101, 114, 105, 97, 108, 105, 122, 101,100, 79, 98, 106, 101, 99, 116, 84, 121, 112, 101]
    NonSerializedObject = [179, 78, 111, 110, 83, 101, 114, 105, 97, 108, 105, 122, 101, 100, 79, 98, 106, 101, 99, 116]
    SerializedObjectData = [180, 83, 101, 114, 105, 97, 108, 105, 122, 101, 100, 79, 98, 106, 101, 99, 116, 68, 97, 116, 97]
    CustomSerialization = [179, 67, 117, 115, 116, 111, 109, 83, 101, 114, 105, 97, 108, 105, 122, 97, 116, 105, 111, 110]

    print( f'{bytes(SerializedObjectType)} : {"/".join([hex(i) for i in SerializedObjectType])}' )
    print( f'{bytes(NonSerializedObject)} : {"/".join([hex(i) for i in NonSerializedObject])}' )
    print( f'{bytes(SerializedObjectData)} : {"/".join([hex(i) for i in SerializedObjectData])}' )
    print( f'{bytes(CustomSerialization)} : {"/".join([hex(i) for i in CustomSerialization])}' )
#spans()

def mpack_example():

    useful_dict = {
        "id": 1,
        "created": datetime.datetime.now(),
    }

    def decode_datetime(obj):
        if '__datetime__' in obj:
            obj = datetime.datetime.strptime(obj["as_str"], "%Y%m%dT%H:%M:%S.%f")
        return obj

    def encode_datetime(obj):
        if isinstance(obj, datetime.datetime):
            return {'__datetime__': True, 'as_str': obj.strftime("%Y%m%dT%H:%M:%S.%f")}
        return obj


    packed_dict = msgpack.packb(useful_dict, default=encode_datetime, use_bin_type=True)
    this_dict_again = msgpack.unpackb(packed_dict, object_hook=decode_datetime, raw=False)


#request = Requests.InputRequest('Horizontal', 100, 1)
#print(request)

buf2 = b"\xf5\x00\x00\x00\xb6\xb2\x07\x41\x86\xa9\x43\x6c\x69\x65\x6e\x74\x55\x49\x44\xd9\x24\x33\x36\x64\x66\x62\x33\x62\x33\x2d\x34\x32\x36\x62\x2d\x34\x36\x31\x32\x2d\x38\x34\x65\x63\x2d\x39\x34\x36\x61\x39\x62\x39\x35\x61\x34\x63\x32\xa9\x52\x65\x71\x75\x65\x73\x74\x49\x64\xd9\x24\x38\x66\x37\x30\x39\x64\x61\x34\x2d\x62\x33\x38\x36\x2d\x34\x30\x61\x33\x2d\x62\x32\x39\x36\x2d\x63\x30\x38\x36\x38\x35\x38\x32\x65\x30\x36\x37\xad\x43\x6f\x72\x72\x65\x6c\x61\x74\x69\x6f\x6e\x49\x64\xa0\xa7\x47\x44\x49\x4f\x4d\x73\x67\x92\xd2\x00\x00\x00\x28\x85\xb3\x4b\x65\x79\x62\x6f\x61\x72\x64\x48\x6f\x6f\x6b\x73\x53\x74\x61\x74\x75\x73\xc3\xb0\x4d\x6f\x75\x73\x65\x48\x6f\x6f\x6b\x73\x53\x74\x61\x74\x75\x73\xc3\xb0\x54\x6f\x75\x63\x68\x48\x6f\x6f\x6b\x73\x53\x74\x61\x74\x75\x73\xc3\xb2\x47\x61\x6d\x65\x70\x61\x64\x48\x6f\x6f\x6b\x73\x53\x74\x61\x74\x75\x73\xc3\xaa\x42\x69\x74\x43\x68\x61\x6e\x67\x65\x64\x0f\xa7\x49\x73\x41\x73\x79\x6e\x63\xc2\xa9\x54\x69\x6d\x65\x73\x74\x61\x6d\x70\xd7\xff\x3b\xe3\x03\x10\x61\x31\x90\x6a"
print( msgpack.unpackb(buf2[8:]) )