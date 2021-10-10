from . import ProtocolObjects, Messages, Exceptions, Serializers, Enums

import asyncio, socket
import msgpack, uuid
import datetime, time
from binascii import crc32

BYTE_ORDER = 'little'
PROTOCOL_VERSION = '2.04.13.2021'

def isEvent(msg):
    return True if msg.GDIOMsg.GetName()[len('Event'):] == 'Event' else False

class Client:
    def __init__(self, hostname, port, connectionTimeout):

        self._disposed = False

        self.hostname = hostname
        self.port = port

        self._reader = None
        self._writer = None

        self.connectionTimeout = connectionTimeout
        self._currentHandshakeState = Enums.HandshakeState.NOT_STARTED

        self.ClientUID = ''

        self.EventHandlers : list = []
        self.EventCollection : list = []
        self.Results : dict = {}
        self.LastEvent : dict = {}

        self.GCD = None

    async def ReadHandler(self, reader=None):
        
        reader = self._reader if reader == None else reader

        print('ReadHandler: Started Task')
        while not self._disposed:
            if reader.at_eof():
                self._disposed = True
                break
            try:
                print('#########Reading#########')
                msg_length = await reader.read(4)
                #print(f'\n{bytes(msg_length)}')

                msg_crc = await reader.read(4)
                #print(bytes(msg_crc))

                msg_data = await reader.read(int.from_bytes(msg_length[:4], byteorder=BYTE_ORDER, signed=False))
                #print(bytes(msg_data))

                unpacked = msgpack.unpackb(msg_data)
                #print(f'\n{unpacked}\n')
                
                msg = ProtocolObjects.ProtocolMessage(**unpacked)
                await self.ProcessMessage(msg)

            except ValueError:
                pass
                print(f'{self.EventHandlers}')

    async def EventsPending(self, eventId):
        return True if eventId in self.EventCollection else False

    async def RemoveEventCollectionId(self, eventId):
        if eventId in self.EventCollection:
            del self.EventCollection[eventId]
    
    async def ProcessMessage(self, msg) -> None:
        print(f'Processing: {msg}')

        if isinstance(msg.GDIOMsg, Messages.Cmd_GenericResponse):
            if msg.GDIOMsg.IsError():
                raise Exception(msg.GDIOMsg.ErrorMessage)
            if msg.GDIOMsg.IsWarning():
                raise Warning(msg.GDIOMsg.WarningMessage)
            if msg.GDIOMsg.IsInformation():
                raise Warning(msg.GDIOMsg.InformationMessage)

        print(f'[RECV] Command: {msg.GDIOMsg.GetName()} in response to {msg.CorrelationId}')
        if self._currentHandshakeState != Enums.HandshakeState.COMPLETE:
            if not isinstance(msg.GDIOMsg, Messages.Cmd_HandshakeResponse):
                print(f'Dropping message before handshake is complete')
                return
            elif self._currentHandshakeState == Enums.HandshakeState.CLIENT_INFORMATION_SENT:
                if msg.GDIOMsg.RC == Enums.HandshakeReasonCode.OK:
                    self.GCD = msg.GDIOMsg.GCD
                    self._currentHandshakeState = Enums.HandshakeState.COMPLETE
                    print('Handshake Complete')
                else:
                    print(f'Handshake Failed: {msg.GDIOMsg.RC}')
                return
            raise Exceptions.CorruptedHandshakeError
        
        if isinstance(msg.GDIOMsg, Messages.Evt_EmptyInput):
            self.SetEventTimestamp(Messages.Evt_EmptyInput)
            return

        # NOTE: `dict.update()` will overwrite the value of overlapping keys
        self.Results.update({msg.CorrelationId : msg.GDIOMsg})
        print(f'Registering Response: {msg.CorrelationId}')
        

    async def GetResult(self, requestId):
        value = None
        while not requestId in self.Results:
            await asyncio.sleep(0)
        print(f'retrieving result for: {requestId}')
        try:
            value = self.Results[requestId]
        except KeyError:
            pass
        else:
            print(f'deleting: {requestId}')
            self.Results.pop(requestId)
            self.EventHandlers.pop(requestId)
        finally:
            return value

    def GetLastEventTimestamp(self, eventType):
        return self.LastEvent[eventType] if eventType in self.LastEvent else 0

    def SetEventTimestamp(self, eventType):
        self.LastEvent.update({eventType : datetime.datetime.now().timestamp()})

    async def WaitForEmptyInput(self, timestamp):
        print('Waiting for empty input')
        while (self.GetLastEventTimestamp(Messages.Evt_EmptyInput) >= timestamp) != True:
            await asyncio.sleep(0)
        return True

    async def SendMessage(self, obj, writer=None):

        writer = self._writer if writer == None else writer

        while obj.RequestId in self.EventHandlers:
            obj.RequestId = str(uuid.uuid4())

        self.EventHandlers.append(obj.RequestId)
        print(f'Sending: {obj.pack()}')
        print(f'RequestId: {obj.RequestId} is waiting for a result.\n')

        await self.WriteMessage(obj, writer)
        return ProtocolObjects.RequestInfo(self, obj.RequestId, obj.Timestamp)

    async def WriteMessage(self, obj, writer=None):

        writer = self._writer if writer == None else writer

        serialized = msgpack.packb(obj, default=Serializers.customSerializer)
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

        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.ClientUID,
            GDIOMsg = Messages.Cmd_HandshakeRequest(
                ProtocolVersion=PROTOCOL_VERSION,
                ClientUID=self.ClientUID,
                channel=None,
                Recording=False
            )
        )
        self._currentHandshakeState = Enums.HandshakeState.CLIENT_INFORMATION_SENT

        requestInfo = await asyncio.wait_for(self.SendMessage(msg, writer), self.connectionTimeout)
        return requestInfo
        
    async def Connect(self, internalComms=False, reader=None, writer=None):

        if internalComms:
            await self.configureChannel()
        else:
            if reader == None and writer == None:
                reader, writer = await asyncio.wait_for(asyncio.open_connection(self.hostname, self.port), self.connectionTimeout)
            self._reader, self._writer = reader, writer
            asyncio.create_task(self.ReadHandler())

        await self.InitHandshake(writer)
        
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