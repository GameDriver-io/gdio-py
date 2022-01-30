from . import ProtocolObjects, Messages, Serializers, Enums

import asyncio, socket, sys
import msgpack, uuid, json
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
                msg_crc = await reader.read(4)
                msg_data = await reader.read(int.from_bytes(msg_length[:4], byteorder=BYTE_ORDER, signed=False))
                
                #unpacked = msgpack.unpackb(msg_data, object_hook=Serializers.msgDeserialize)
                unpacked = msgpack.unpackb(msg_data)
                #print(f'\n{unpacked}\n')
                
                msg = ProtocolObjects.ProtocolMessage(**unpacked)
                await self.ProcessMessage(msg)

            except ValueError:
                pass


    def EventsPending(self, eventId):
        return True if eventId in self.EventCollection else False

    def RemoveEventCollectionId(self, eventId):

        if eventId in self.EventCollection:

            del self.EventCollection[eventId]

    def GetNextEvent(self, eventId):
        if len(self.EventCollection) == 0:
            raise Exception('Error getting next event. No events registered.')
        for index, key in enumerate(self.EventCollection):
            if key == eventId:
                return self.EventCollection.pop(index)

    async def WaitForNextEvent(self, eventId):
        while True:
            await asyncio.sleep(0)
            try:
                return self.GetNextEvent(eventId)
            except:
                pass
    
    async def ProcessMessage(self, msg) -> None:
        
        # If the message is a generic response,
        if isinstance(msg.GDIOMsg, Messages.Cmd_GenericResponse):
            # check if it has any errors worth reporting.
            if msg.GDIOMsg.IsError():
                raise Exception(msg.GDIOMsg.ErrorMessage)

        # If the message is not a generic response or there are no errors
        logging.debug(f'[RECV] {msg.GDIOMsg.GetName()} in response to {msg.CorrelationId}:\n{json.dumps(msg.pack(), indent=4, default=Serializers.msgDeserialize)}')

        # If the handshake is not complete,
        if self._currentHandshakeState != Enums.HandshakeState.COMPLETE:
            
            # and the message is a not a handshake response,
            if not isinstance(msg.GDIOMsg, Messages.Cmd_HandshakeResponse):
                
                # skip processing the message.
                logging.error(f'Expected handshake response, got {msg.GDIOMsg.GetName()}. Dropping Message before handshake is complete')
                return

            # The handshake is still expecting a response,
            elif self._currentHandshakeState == Enums.HandshakeState.CLIENT_INFORMATION_SENT:

                if msg.GDIOMsg.RC == Enums.HandshakeReasonCode.OK:
                    logging.debug(f'Recieved connection details {msg.GDIOMsg.GCD}')
                    self.GCD = msg.GDIOMsg.GCD
                    self._currentHandshakeState = Enums.HandshakeState.COMPLETE
                    logging.debug(f'Handshake complete')

                else:
                    logging.error(f'Handshake failed: {msg.GDIOMsg.RC}')

                return

            raise Exception('Handshake failed')

        # If the message is an event
        if 'Evt_' in msg.GDIOMsg.GetName():

            logging.debug(f'Recieved event {msg.GDIOMsg.GetName()} in response to {msg.GDIOMsg.CorrelationId}. Registering event...')

            # If the message is an empty input event,
            if isinstance(msg.GDIOMsg, Messages.Evt_EmptyInput):

                # save the timestamp that it was received.
                self.SetEventTimestamp(Messages.Evt_EmptyInput)
                return

            if isinstance(msg.GDIOMsg, Messages.Evt_Collision):

                self.SetEventTimestamp(Messages.Evt_EmptyInput)
                self.EventCollection.Update({msg.CorrelationId : msg.GDIOMsg})
                return

        else:
            # If the message is anything else, register the response data to be grabbed later.

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

    async def SendArbitrary(self, data, writer=None):
        writer = self._writer if writer == None else writer
        
        logging.debug(f'Sending arbitrary data...')
        writer.write(data)
        await writer.drain()

    async def SendMessage(self, obj, writer=None):

        writer = self._writer if writer == None else writer

        while obj.RequestId in self.EventHandlers:
            obj.RequestId = str(uuid.uuid4())

        self.EventHandlers.append(obj.RequestId)
        serialized = msgpack.packb(obj, default=Serializers.msgSerialize)

        logging.debug(f'[SEND] {obj.GDIOMsg.GetName()} as {obj.RequestId}:\n{json.dumps(obj.pack(), indent=4, default=Serializers.msgDeserialize)}')
        
        msg_payload = await self.ConstructPayload(serialized)
        payload_bytes = bytes(msg_payload)
        writer.write(payload_bytes)
        await writer.drain()

        logging.debug(f'{obj.RequestId} is waiting for a response...')

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

        logging.debug('Disconnecting...')

        writer = self._writer if writer == None else writer        

        self._disposed = True
        
        writer.close()
        await writer.wait_closed()

    def __repr__(self):
        return self.ClientUID