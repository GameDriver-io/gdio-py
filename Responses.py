from Objects import Message, ResponseCode

from enum import Enum, auto

class GenericResponse(Message):
    def __init__(self,
        # TODO: NO MUTABLE DEFAULTS!!!
            CmdID = 99,
            StackTrace = '',
            ErrorMessage = '',
            InformationMessage = '',
            WarningMessage = '',
            RC = ResponseCode.OK,
            ReturnedValues = None
        ):
        super().__init__(CmdID)

        self.StackTrace = StackTrace
        self.ErrorMessage = ErrorMessage
        self.InformationMessage = InformationMessage
        self.WarningMessage = WarningMessage
        self.RC = RC

    def IsError(self):
        return (len(self.ErrorMessage) > 1)

    def IsInformation(self):
        return (len(self.InformationMessage) > 1)

    def IsWarning(self):
        return (len(self.WarningMessage) > 1)

class GetObjectValueResponse(GenericResponse):
    def __init__(self,
            Value,
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
        super().__init__(36, StackTrace, ErrorMessage, InformationMessage, WarningMessage, RC, ReturnedValues)

        self.Value = Value
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
        super().__init__(16, StackTrace, ErrorMessage, InformationMessage, WarningMessage, RC, ReturnedValues)

        self.ImageData = ImageData
        self.ImagePath = ImagePath
