from . import Requests, Objects

import asyncio, socket
import msgpack, uuid
import time
from binascii import crc32

class Client:
    def __init__(self, hostname, port, connectionTimeout):

        self._disposed = False

        self.hostname = hostname
        self.port = port
        self.connectionTimeout = connectionTimeout

        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ClientUID = ''

        self.EventCollection = {}

        self.GCD = None

    async def ReadHandler(self):
        while not self._disposed:
            await asyncio.sleep(0)

    def SendMessage(self, obj):

        self.WriteMessage(obj)
        return Objects.RequestInfo(self, obj.RequestID, obj.Timestamp)

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

        msg = Objects.ProtocolMessage(
            ClientUID = self.ClientUID,
            GDIOMsg = Requests.HandshakeRequest(
                ClientUID=self.ClientUID,
            )
        )
        requestInfo = self.SendMessage(msg)
        self.Wait(requestInfo, self.connectionTimeout)
        

    def Connect(self):

        self._client.connect((self.hostname, self.port))
        self.InitHandshake()

        response = self.Recieve()
        self.GCD = Objects.GameConnectionDetails(**response['GDIOMsg'][1]['GCD'])

        return True

    def Recieve(self):

        response_length = self._client.recv(4)
        response_data = self._client.recv(int.from_bytes(response_length, byteorder='little', signed=False) + 4)[4:]

        return msgpack.unpackb(response_data)

    def Disconnect(self):
        self._disposed = True
        self._client.close()
    
    def log(self, level, message):
        # TODO: log_level
        print(message)
        
    async def Wait(self, requestInfo, timeout):
        self._client.settimeout(timeout)
        self.log(0, f'Client: {requestInfo.Client} Waiting for RequestID: {requestInfo.RequestID} at {requestInfo.SentTimestamp}')
    
    def __repr__(self):
        return self.ClientUID