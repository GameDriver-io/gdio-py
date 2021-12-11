from . import ProtocolObjects, Messages, Serializers, Enums

import asyncio, socket, sys
import msgpack, uuid
import datetime, time
from binascii import crc32

import logging

from .constants import *

isEvent = lambda x: x.startswith('EVENT_')


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

    async def _ReadHandler(self, reader=None):
        
        reader = self._reader if reader == None else reader

        logging.debug('ReadHandler task started')
        while not self._disposed:
            if reader.at_eof():
                self._disposed = True
                break
            try:
                logging.debug('Reading...')
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


    async def EventsPending(self, eventId):
        return True if eventId in self.EventCollection else False

    async def RemoveEventCollectionId(self, eventId):

        if eventId in self.EventCollection:

            del self.EventCollection[eventId]
    
    async def ProcessMessage(self, msg) -> None:
        #logging.debug(f'Processing message: {msg}')

        if isinstance(msg.GDIOMsg, Messages.Cmd_GenericResponse):

            if msg.GDIOMsg.IsError():
                raise Exception(msg.GDIOMsg.ErrorMessage)

            if msg.GDIOMsg.IsWarning():
                raise Warning(msg.GDIOMsg.WarningMessage)

        logging.debug(f'[RECV] {msg.GDIOMsg.GetName()} in response to {msg.CorrelationId}')

        if self._currentHandshakeState != Enums.HandshakeState.COMPLETE:

            if not isinstance(msg.GDIOMsg, Messages.Cmd_HandshakeResponse):

                logging.error(f'Expected handshake response, got {msg.GDIOMsg.GetName()}. Dropping Message before handshake is complete')

                return
            elif self._currentHandshakeState == Enums.HandshakeState.CLIENT_INFORMATION_SENT:

                if msg.GDIOMsg.RC == Enums.HandshakeReasonCode.OK:
                    self.GCD = msg.GDIOMsg.GCD
                    self._currentHandshakeState = Enums.HandshakeState.COMPLETE
                    logging.debug(f'Handshake complete')

                else:
                    logging.error(f'Handshake failed: {msg.GDIOMsg.RC}')

                return

            raise Exception('Handshake failed')
        
        if isinstance(msg.GDIOMsg, Messages.Evt_EmptyInput):

            self.SetEventTimestamp(Messages.Evt_EmptyInput)
            return

        # NOTE: `dict.update()` will overwrite the value of overlapping keys
        #    As far as I know, this should never happen
        logging.debug(f'Registering response for {msg.CorrelationId}')
        self.Results.update({msg.CorrelationId : msg.GDIOMsg})
        
        

    async def GetResult(self, requestId):
        value = None
        while not requestId in self.Results:
            await asyncio.sleep(0)
        logging.debug(f'Getting result for {requestId}')
        try:
            value = self.Results[requestId]
        except KeyError:
            pass
        else:
            logging.debug(f'Got result for {requestId}. Discarding...')
            self.Results.pop(requestId)
            self.EventHandlers.pop(requestId)
        finally:
            return value

    def GetLastEventTimestamp(self, eventType):
        return self.LastEvent[eventType] if eventType in self.LastEvent else 0

    def SetEventTimestamp(self, eventType):
        self.LastEvent.update({eventType : datetime.datetime.now().timestamp()})

    async def WaitForEmptyInput(self, timestamp):
        logging.debug(f'Waiting for empty input...')
        while (self.GetLastEventTimestamp(Messages.Evt_EmptyInput) >= timestamp) != True:
            await asyncio.sleep(0)
        return True

    async def SendMessage(self, obj, writer=None):

        writer = self._writer if writer == None else writer

        while obj.RequestId in self.EventHandlers:
            obj.RequestId = str(uuid.uuid4())

        self.EventHandlers.append(obj.RequestId)
        logging.debug(f'[SEND] {obj.GDIOMsg.GetName()} as {obj.RequestId}. Waiting for a response...')

        serialized = msgpack.packb(obj, default=Serializers.customSerializer)
        msg_payload = await self.ConstructPayload(serialized)
        payload_bytes = bytes(msg_payload)
        writer.write(payload_bytes)
        await writer.drain()

        return ProtocolObjects.RequestInfo(self, obj.RequestId, obj.Timestamp)

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
            asyncio.shield(asyncio.create_task(self._ReadHandler()))

        await self.InitHandshake(writer)
        
        return True

    async def configureChannel(self):
        raise NotImplementedError

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

    def __repr__(self):
        return self.ClientUID