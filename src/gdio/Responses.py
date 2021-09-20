from .Objects import Message, ResponseCode

from enum import Enum, auto

## TODO: These could probably all be dataclasses instead.

class GenericResponse(Message):
    def __init__(self,
            StackTrace         = None,
            ErrorMessage       = None,
            InformationMessage = None,
            WarningMessage     = None,
            RC                 = ResponseCode.OK,
            ReturnedValues     = None
        ):

        self.StackTrace =         '' if StackTrace == None else StackTrace
        self.ErrorMessage =       '' if ErrorMessage == None else ErrorMessage
        self.InformationMessage = '' if InformationMessage == None else InformationMessage
        self.WarningMessage =     '' if WarningMessage == None else WarningMessage
        self.RC = RC

    def IsError(self):
        return (len(self.ErrorMessage) > 1)

    def IsInformation(self):
        return (len(self.InformationMessage) > 1)

    def IsWarning(self):
        return (len(self.WarningMessage) > 1)

class GetObjectValueResponse(GenericResponse):
    def __init__(self,
            _cmdID,
            SerializeObjectType,
            Serializer,
            directObject,

            StackTrace,
            ErrorMessage,
            InformationMessage,
            WarningMessage,
            RC,
            ReturnedValues,
        ):
        super().__init__(StackTrace, ErrorMessage, InformationMessage, WarningMessage, RC, ReturnedValues)

        self._CmdID = _cmdID
        self.SerializeObjectType = SerializeObjectType
        self.Serializer = Serializer
        self.directObject = directObject

class CaptureScreenshotResponse(GenericResponse):
    def __init__(self,
            ImageData,
            ImagePath,

            StackTrace,
            ErrorMessage,
            InformationMessage,
            WarningMessage,
            RC,
            ReturnedValues,
        ):
        super().__init__(StackTrace, ErrorMessage, InformationMessage, WarningMessage, RC, ReturnedValues)

        self.ImageData = ImageData
        self.ImagePath = ImagePath



class HandshakeResponse(GenericResponse):
    def __init__(self,
            ReceivedTimestamp,
            RC,
            GCD,
        ):
        self.ReceivedTimestamp = ReceivedTimestamp
        self.RC = RC
        self.GCD = GCD