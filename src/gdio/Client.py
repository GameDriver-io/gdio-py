from . import Requests, Objects

import asyncio
import msgpack, uuid
import time
from binascii import crc32

class Client:
    def __init__(self, hostname, port, connectionTimeout):

        self._disposed = False

        self.hostname = hostname
        self.port = port

        self._reader = None
        self._writer = None

        self.connectionTimeout = connectionTimeout

        self.ClientUID = ''

        # These dicts are currently useless,
        # it just helps for them to be here for future reworks.
        self.EventHandlers : {'RequestID' : 'IsFulfilled'} = {}
        self.Results : {'CorrelationID' : 'GDIOMsg'} = {}
        self.EventCollection : {'EventID' : 'IsFulfilled'} = {}

        self.GCD = None

    async def ReadHandler(self):
        raise NotImplementedError
        while not self._disposed:
            await asyncio.sleep(0)

    async def SendMessage(self, obj):
        self.EventHandlers.update(
            {obj.RequestID : False}
        )
        self.log(0, f'Request({obj.GDIOMsg.toList()[0]}): {obj.RequestID} is waiting for a result.')

        await self.WriteMessage(obj)
        return Objects.RequestInfo(self, obj.RequestID, obj.Timestamp)

    async def WriteMessage(self, obj):
        serialized = msgpack.packb(obj.toDict())
        msg = bytes(self.ConstructPayload(serialized))
        self._writer.write(msg)
        await self._writer.drain()

    def ConstructPayload(self, msg):
        assert type(msg) == bytes

        length_bytes = bytearray(len(msg).to_bytes(4, 'little'))
        crcBytes = bytearray(crc32(bytes(msg)).to_bytes(4, 'little'))
        msgBytes = bytearray(msg)

        payload = bytearray(length_bytes + crcBytes + msgBytes)
        
        return payload

    async def InitHandshake(self):

        self.ClientUID = str(uuid.uuid4())

        msg = Objects.ProtocolMessage(
            ClientUID = self.ClientUID,
            GDIOMsg = Requests.HandshakeRequest(
                ClientUID=self.ClientUID,
            )
        )

        requestInfo = await asyncio.wait_for(self.SendMessage(msg), self.connectionTimeout)
        

    async def Connect(self):

        self._reader, self._writer = await asyncio.open_connection(self.hostname, self.port)
        await self.InitHandshake()

        response = await self.Recieve()
        self.GCD = Objects.GameConnectionDetails(**response['GDIOMsg'][1]['GCD'])

        return True

    async def Recieve(self):

        response_length = await self._reader.read(4)
        response_data = await self._reader.read(int.from_bytes(response_length, byteorder='little', signed=False) + 4)

        return msgpack.unpackb(response_data[4:])

    async def Disconnect(self):
        self._disposed = True
        self._writer.close()
        await self._writer.wait_closed()
    
    def log(self, level, message):
        # TODO: log_level
        print(message)
        
    def __repr__(self):
        return self.ClientUID