from Requests import *
from Objects import *

import msgpack, uuid, socket
import time
from binascii import crc32


class Client:
    def __init__(self, hostname, port, connectionTimeout):

        self.hostname = hostname
        self.port = port
        self.connectionTimeout = connectionTimeout

        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ClientUID = ''

        self.GCD = None

    def SendMessage(self, obj):
        self.WriteMessage(obj)
        return RequestInfo(self, obj.RequestId, obj.Timestamp)

    def WriteMessage(self, obj):
        serialized = msgpack.packb(obj.toDict())
        msg = bytes(self.ConstructPayload(serialized))
        self._client.send(msg)

    def ConstructPayload(self, msg):
        assert type(msg) == bytes

        length_bytes = bytearray(len(msg).to_bytes(4, 'little'))
        crcBytes = bytearray(crc32(bytes(msg)).to_bytes(4, 'little'))
        msgBytes = bytearray(msg)

        payload = bytearray(length_bytes + crcBytes + msgBytes)
        
        return payload

    def InitHandshake(self):

        self.ClientUID = str(uuid.uuid4())

        msg = ProtocolMessage(
            ClientUID = self.ClientUID,
            GDIOMsg = HandshakeRequest(
                ClientUID=self.ClientUID,
            )
        )
        requestInfo = self.SendMessage(msg)
        self.Wait(requestInfo, self.connectionTimeout)
        

    def Connect(self):

        self._client.connect((self.hostname, self.port))
        self.InitHandshake()

        response = self.Recieve()
        self.GCD = GameConnectionDetails(**response['GDIOMsg'][1]['GCD'])

        return True

    def Recieve(self):

        response_length = self._client.recv(4)
        response_data = self._client.recv(int.from_bytes(response_length, byteorder='little', signed=False) + 4)[4:]

        return msgpack.unpackb(response_data)

    def Disconnect(self):
        self._client.close()
    
    def log(self, level, message):
        # TODO: log_level
        print(message)
        
    def Wait(self, RequestInfo, timeout):
        self._client.settimeout(timeout)
        self.log(0, f'Client: {self.ClientUID} Waiting for RequestId: {RequestInfo.RequestId} at {RequestInfo.SentTimestamp}')