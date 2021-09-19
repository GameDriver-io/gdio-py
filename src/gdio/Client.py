from . import Requests, Objects, Responses, Exceptions

import asyncio, socket
import msgpack, uuid
import time
from binascii import crc32

BYTE_ORDER = 'little'

class Client:
    def __init__(self, hostname, port, connectionTimeout):

        self._disposed = False

        self.hostname = hostname
        self.port = port

        self._reader = None
        self._writer = None

        self.connectionTimeout = connectionTimeout
        self._currentHandshakeState = Objects.HandshakeState.NOT_STARTED

        self.ClientUID = ''

        self.EventHandlers : ['RequestId'] = []
        self.EventCollection : ['EventId'] = []
        self.Results : {'CorrelationId' : 'GDIOMsg'} = {}
        

        self.GCD = None

    async def ReadHandler(self, reader=None):
        
        reader = self._reader if reader == None else reader

        print('ReadHandler: Started Task')
        while not self._disposed:
            if reader.at_eof():
                self._disposed = True
                break
            try:
                print('ReadHandler: Iterating')
                #await asyncio.sleep(0)
                print('ReadHandler: Reading')

                msg_length = await reader.read(4)
                #print(bytes(msg_length))

                msg_crc = await reader.read(4)
                #print(bytes(msg_crc))

                msg_data = await reader.read(int.from_bytes(msg_length[:4], byteorder=BYTE_ORDER, signed=False))
                #print(bytes(msg_data))

                unpacked = msgpack.unpackb(msg_data)
                #print(unpacked)
                
                msg = Objects.ProtocolMessage(**unpacked)
                self.ProcessMessage(msg)
            except ValueError as e:
                pass

    async def EventsPending(self, eventId):
        if eventId in self.EventCollection:
            if self.EventCollection[eventId].is_set():
                return True
        return False

    async def RemoveEventCollectionId(self, eventId):
        if eventId in self.EventCollection:
            del self.EventCollection[eventId]
    
    def ProcessMessage(self, msg):
        # TODO: Reconstruct GDIOMsg
        # TODO: GDIOMsg.GetName()
        commandType = msg.GDIOMsg[0]
        gdioMsg = msg.GDIOMsg[1]
        print(f'[RECV] Command: {msg.CorrelationId}')
        if self._currentHandshakeState != Objects.HandshakeState.COMPLETE:
            if commandType != 4:
                print(f'Dropping message before handshake is complete: {commandType}')
                return
            elif self._currentHandshakeState == Objects.HandshakeState.CLIENT_INFORMATION_SENT:
                if Responses.HandshakeResponse(**gdioMsg).RC == Objects.HandshakeReasonCode.OK:
                    self.GCD = Responses.HandshakeResponse(**gdioMsg).GCD
                    self._currentHandshakeState = Objects.HandshakeState.COMPLETE
                    print('Handshake Complete')
                else:
                    print(f'Handshake Failed: {Responses.HandshakeResponse(**gdioMsg).RC}')
                return
            raise Exceptions.CorruptedHandshakeException
            
        print(f'Registering Response: {msg.CorrelationId}')
        # NOTE: `dict.update()` will overwrite the value of overlapping keys
        self.Results.update(
            {msg.CorrelationId : msg.GDIOMsg}
        )

    async def GetResult(self, requestId):
        value = None
        #while not await self.EventsPending(requestId):
        await asyncio.sleep(0)
        try:
            value = self.Results[requestId]
        except KeyError as e:
            pass
        else:
            del self.Results[requestId]
        return value

    async def SendMessage(self, obj, writer=None):

        writer = self._writer if writer == None else writer

        while obj.RequestId in self.EventHandlers:
            obj.RequestId = str(uuid.uuid4())

        self.EventHandlers.append(obj.RequestId)
        print(f'Sending: {obj.toDict()}')
        print(f'RequestId: {obj.RequestId} is waiting for a result.\n')

        

        await self.WriteMessage(obj, writer)
        return Objects.RequestInfo(self, obj.RequestId, obj.Timestamp)

    async def WriteMessage(self, obj, writer=None):

        writer = self._writer if writer == None else writer

        serialized = msgpack.packb(obj.toDict())
        msg_payload = await self.ConstructPayload(serialized)
        payload_bytes = bytes(msg_payload)
        writer.write(payload_bytes)
        await writer.drain()

    async def ConstructPayload(self, msg):
        assert type(msg) == bytes

        length_bytes = bytearray(len(msg).to_bytes(4, BYTE_ORDER))
        crcBytes = bytearray(crc32(bytes(msg)).to_bytes(4, BYTE_ORDER))
        msgBytes = bytearray(msg)

        payload = bytearray(length_bytes + crcBytes + msgBytes)
        
        return payload

    async def InitHandshake(self, writer=None):

        writer = self._writer if writer == None else writer

        self.ClientUID = str(uuid.uuid4())

        msg = Objects.ProtocolMessage(
            ClientUID = self.ClientUID,
            GDIOMsg = Requests.HandshakeRequest(
                ProtocolVersion='2.04.13.2021',
                ClientUID=self.ClientUID,
                channel=None,
                Recording=False
            )
        )
        self._currentHandshakeState = Objects.HandshakeState.CLIENT_INFORMATION_SENT

        requestInfo = await asyncio.wait_for(self.SendMessage(msg, writer), self.connectionTimeout)
        return requestInfo
        
    async def Connect(self, internalComms=False):

        if internalComms:
            await self.configureChannel()
        else:
            self._reader, self._writer = await asyncio.wait_for(asyncio.open_connection(self.hostname, self.port), self.connectionTimeout)
            asyncio.create_task(self.ReadHandler())

        await self.InitHandshake()
        
        return True

    async def configureChannel(self):
        pass

    async def Receive(self, reader=None):

        reader = self._reader if reader == None else reader
        response_length = await reader.read(4)
        response_crc = await reader.read(4)
        response_data = await reader.read(int.from_bytes(response_length, byteorder=BYTE_ORDER, signed=False))

        return msgpack.unpackb(response_data)

    async def Disconnect(self, writer=None):

        writer = self._writer if writer == None else writer

        self._disposed = True
        writer.close()
        await writer.wait_closed()
    
    def log(self, level, message):
        # TODO: log_level
        print(message)
        
    def __repr__(self):
        return self.ClientUID