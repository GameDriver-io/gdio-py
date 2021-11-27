import msgpack
from . import Serializers
from . import ProtocolObjects
from . import Enums

CmdIds = {
    "Cmd_ChangeObjectResolverCacheStateRequest" : 47,
    "Cmd_GetSceneNameRequest" : 27,
    "Cmd_CallMethodRequest" : 33,
    "Cmd_FlushCacheRequest" : 46,
    "Cmd_GetObjectPositionRequest" : 28,
    "Cmd_ObjectDistanceRequest" : 45,
    "Cmd_PokeRequest" : 42,
    "Cmd_PeekRequest" : 41,
    "Cmd_ChangeHookStatusRequest" : 40,
    "Cmd_TapRequest" : 44,
    "Cmd_GetObjectValueRequest" : 26,
    "Cmd_TouchEventRequest" : 43,
    "Cmd_WaitForObjectRequest" : 8,
    "Cmd_GenericResponse" : 99,
    "Cmd_GetGameObjectRequest" : 52,
    "Cmd_InputManagerStateRequest" : 48,
    "Cmd_ClickObjectRequest" : 31,
    "Cmd_GetMousePositionRequest" : 30,
    "Cmd_UnregisterCollisionMonitorRequest" : 51,
    "Cmd_GetStatisticsRequest" : 50,
    "Cmd_RegisterCollisionMonitorRequest" : 49,
    "Cmd_PeekResponse" : 39,
    "Cmd_MouseDragRequest" : 23,
    "Cmd_SetObjectValueRequest" : 13,
    "Cmd_SetInputFieldTextRequest" : 14,
    "Cmd_ClickRequest" : 32,
    "Cmd_WaitForObjectValueRequest" : 10,
    "Cmd_WaitForObjectValueResponse" : 11,
    "Cmd_SetTimeScaleRequest" : 12,
    "Cmd_MouseMoveRequest" : 22,
    "Cmd_MouseMoveToObjectRequest" : 21,
    "Cmd_RaycastResponse" : 19,
    "Cmd_NavAgentMoveToPointRequest" : 20,
    "Cmd_RaycastRequest" : 18,
    "Cmd_CaptureScreenshotRequest" : 15,
    "Cmd_CaptureScreenshotResponse" : 16,
    "Cmd_RotateRequest" : 17,
    "Cmd_WaitForObjectResponse" : 9,
    "Cmd_TransferFileRequest" : 34,
    "Cmd_GetClientListRequest" : 0,
    "Cmd_HandshakeRequest" : 1,
    "Cmd_GetObjectInterfacesList" : 35,
    "Cmd_GetObjectListResponse" : 38,
    "Cmd_VectorResponse" : 37,
    "Cmd_GetObjectValueResponse" : 36,
    "Cmd_Ping" : 2,
    "Cmd_Broadcast" : 6,
    "Cmd_DirectMessage" : 7,
    "Cmd_LoadSceneRequest" : 24,
    "Cmd_Pong" : 5,
    "Cmd_GetClientListResponse" : 3,
    "Cmd_HandshakeResponse" : 4,
    "Cmd_KeyPressRequest" : 25,
    "Cmd_GetObjectListRequest" : 29,

    "Cmd_SceneLoaded" : 81,
    "Evt_EmptyInput" : 80,
}

class Message:
    def __init__(self):
        pass

    def GetName(self):
        return f'{self.__class__.__name__}'

    def pack(self):
        return [CmdIds[self.GetName()], vars(self)]

    def __repr__(self):
        return f'{self.pack()}'

class Cmd_GenericResponse(Message):
    def __init__(self,
            StackTrace : str,
            ErrorMessage : str,
            InformationMessage : str,
            WarningMessage : str,
            RC : Enums.ResponseCode,
            ReturnedValues : list
        ):
        self.StackTrace = StackTrace
        self.ErrorMessage = ErrorMessage
        self.InformationMessage = InformationMessage
        self.WarningMessage = WarningMessage
        self.RC = RC
        self.ReturnedValues = ReturnedValues

    def IsError(self):
        return (len(self.ErrorMessage) > 1)

    def IsInformation(self):
        return (len(self.InformationMessage) > 1)

    def IsWarning(self):
        return (len(self.WarningMessage) > 1)


class Cmd_CallMethodRequest(Message):
    # TODO: custom serializer
    def __init__(self, HierarchyPath = None, MethodName = None, Arguments = None, Arguments2 = None, _serializer = None):
        self.HierarchyPath = '' if HierarchyPath == None else HierarchyPath
        self.MethodName = '' if MethodName == None else MethodName
        self.Arguments = [] if Arguments == None else Arguments
        self.Arguments2 = [] if Arguments2 == None else Arguments2
        self._serializer = _serializer

    def SetArguments(self, arguments = None, serializer = None):
        customSerializer : Serializers.CustomSerializer = self._serializer if serializer == None else serializer
        serializedObjectData = None
        if arguments == None:
            return
        if len(arguments) == 1:
            if not Serializers.IsBuiltin(arguments[0]):
                if (customSerializer == None):
                    raise Exception(f'CustomSerializer is not defined for type: {type(arguments[0])}')
                    
                serializedObjectData = customSerializer.Serialize(arguments[0])

            self.Arguments.append(Serializers.SerializedObject(
                SerializedObjectType = type(arguments[0]),
                SerializedObjectData = serializedObjectData
            ))
            return

        ret = []
        for obj in arguments:
            if isinstance(obj, object):
                if  not Serializers.IsBuiltin(obj) and (customSerializer == None):
                    raise Exception(f'CustomSerializer is not defined for type: {type(obj)}')
                serializedObjectData = msgpack.packb(obj) if customSerializer == None else customSerializer.Serialize(obj)
                if serializedObjectData == None:
                    raise Exception(f'Failed to serialized object of type: {type(obj)}')
                ret.append(
                    Serializers.SerializedObject(
                        SerializedObjectType = type(obj),
                        SerializedObjectData = serializedObjectData,
                        CustomSerialization = True
                    )
                )
            else:
                ret.append(
                    Serializers.SerializedObject(
                        NonSerializedObject=obj
                    )
                )


## CaptureScreenshot

# Request
class Cmd_CaptureScreenshotRequest(Message):
    # TODO: default filename
    # TODO: stereo capture mode = LeftEye (Enum)
    def __init__(self, StoreInGameFolder = False, Filename = None, SuperSize = 1, Mode = 1):
        self.StoreInGameFolder = StoreInGameFolder
        self.Filename = '' if Filename == None else Filename
        self.SuperSize = SuperSize
        self.Mode = Mode

# Response
class Cmd_CaptureScreenshotResponse(Cmd_GenericResponse):
    def __init__(self,
            ImageData : bytes,
            ImagePath : str,
            StackTrace : str,

            # GenericResponse
            ErrorMessage : str,
            InformationMessage : str,
            WarningMessage : str,
            RC : Enums.ResponseCode,
            ReturnedValues : list
            ):
        super().__init__(StackTrace, ErrorMessage, InformationMessage, WarningMessage, RC, ReturnedValues)

        self.ImageData = ImageData
        self.ImagePath = ImagePath


class Cmd_ChangeHookStatusRequest(Message):
    def __init__(self, KeyboardHooksStatus = True, MouseHooksStatus = True, TouchHooksStatus = True, GamepadHooksStatus = True, BitChanged = 0):
        self.KeyboardHooksStatus = KeyboardHooksStatus
        self.MouseHooksStatus = MouseHooksStatus
        self.TouchHooksStatus = TouchHooksStatus
        self.GamepadHooksStatus = GamepadHooksStatus
        self.BitChanged = BitChanged


class Cmd_ChangeObjectResolverCacheStateRequest(Message):
    def __init__(self, STATE = True):
        self.STATE = STATE


class Cmd_ClickObjectRequest(Message):
    def __init__(self, MouseButtonId = 0, HierarchyPath = None, CameraHierarchyPath = None, IsDoubleClick = False, FrameCount = 5):
        self.MouseButtonId = MouseButtonId
        self.HierarchyPath = '' if HierarchyPath == None else HierarchyPath
        self.CameraHierarchyPath = '' if CameraHierarchyPath == None else CameraHierarchyPath
        self.IsDoubleClick = IsDoubleClick
        self.FrameCount = FrameCount


class Cmd_ClickRequest(Message):
    def __init__(self, IsDoubleClick = False, FrameCount = 5, MouseButtonId = 0, X = 0, Y = 0):
        self.IsDoubleClick = IsDoubleClick
        self.FrameCount = FrameCount
        self.MouseButtonId = MouseButtonId
        self.X = X
        self.Y = Y


class Cmd_FlushCacheRequest(Message):
    def __init__(self):
        pass


class Cmd_GetGameObjectRequest(Message):
    def __init__(self, HierarchyPath = None):
        self.HierarchyPath = '' if HierarchyPath == None else HierarchyPath


class Cmd_GetMousePositionRequest(Message):
    def __init__(self):
        pass


class Cmd_GetObjectInterfacesList(Message):
    def __init__(self):
        pass


class Cmd_GetObjectListRequest(Message):
    def __init__(self):
        pass


class Cmd_GetObjectPositionRequest(Message):
    def __init__(self, ObjectHierarchyPath = None, CameraHierarchyPath = None):
        self.ObjectHierarchyPath = '' if ObjectHierarchyPath == None else ObjectHierarchyPath
        self.CameraHierarchyPath = '' if CameraHierarchyPath == None else CameraHierarchyPath


class Cmd_GetObjectValueRequest(Message):
    def __init__(self, HierarchyPath = None, ObjectFieldOrPropertyName = None, TypeFullName = None):
        self.HierarchyPath = '' if HierarchyPath == None else HierarchyPath
        self.ObjectFieldOrPropertyName = '' if ObjectFieldOrPropertyName == None else ObjectFieldOrPropertyName
        self.TypeFullName = '' if TypeFullName == None else TypeFullName

class Cmd_GetObjectValueResponse(Cmd_GenericResponse):
    def __init__(self, _cmdID, SerializeObjectType, Serializer, directObject, StackTrace, ErrorMessage, InformationMessage, WarningMessage, RC, ReturnedValues):
        super().__init__(StackTrace, ErrorMessage, InformationMessage, WarningMessage, RC, ReturnedValues)

        self._CmdID = _cmdID
        self.SerializeObjectType = SerializeObjectType
        self.Serializer = Serializer
        self.directObject = directObject


class Cmd_GetSceneNameRequest(Message):
    def __init__(self):
        pass


class Cmd_GetStatisticsRequest(Message):
    def __init__(self, HierarchyPath = None):
        self.HierarchyPath = '' if HierarchyPath == None else HierarchyPath


class Cmd_InputManagerStateRequest(Message):
    def __init__(self, IdName=None, NumberOfFrames=0, InputType=0, ChangeValue=0.0):
        self.IdName = IdName if IdName else ''
        self.NumberOfFrames = NumberOfFrames
        self.InputType = InputType
        self.ChangeValue = ChangeValue


class Cmd_KeyPressRequest(Message):
    def __init__(self,
            KeyCodes : list = None,
            Modifiers : list = None,
            NumberOfFrames : int = 0,
        ):
        self.KeyCodes = KeyCodes if KeyCodes else []
        self.Modifiers = Modifiers if Modifiers else []
        self.NumberOfFrames = NumberOfFrames


class Cmd_LoadSceneRequest(Message):
    def __init__(self, SceneName = None):
        self.SceneName = SceneName if SceneName else ''


class Cmd_MouseDragRequest(Message):
    def __init__(self, Destination = None, Origin = None, DestinationUTR = None, OriginUTR = None, FrameCount = 0, ButtonId = 0):
        self.Destination = Destination
        self.Origin = Origin
        self.DestinationUTR = DestinationUTR
        self.OriginUTR = OriginUTR
        self.FrameCount = FrameCount
        self.ButtonId = ButtonId


class Cmd_MouseMoveRequest(Message):
    def __init__(self, Destination = None, Origin = None, DestinationUTR = None, OriginUTR = None, FrameCount = 0):
        self.Destination = Destination
        self.Origin = Origin
        self.DestinationUTR = DestinationUTR
        self.OriginUTR = OriginUTR
        self.FrameCount = FrameCount


class Cmd_MouseMoveToObjectRequest(Message):
    def __init__(self, ObjectHierarchyPath = None, Timeout = 30, FrameCount = 5, WaitForObject = True):
        self.ObjectHierarchyPath = ObjectHierarchyPath if ObjectHierarchyPath else ''
        self.Timeout = Timeout
        self.FrameCount = FrameCount
        self.WaitForObject = WaitForObject


class Cmd_NavAgentMoveToPointRequest(Message):
    def __init__(self, Point = None, PointUTR = None, NavAgent_HierarchyPath = None):
        self.Point = Point
        self.PointUTR = PointUTR
        self.NavAgent_HierarchyPath = NavAgent_HierarchyPath if NavAgent_HierarchyPath else ''


class Cmd_NavAgentMoveToObjectRequest(Message):
    def __init__(self):
        raise NotImplementedError


class Cmd_ObjectDistanceRequest(Message):
    def __init__(self, ObjectA_HierarchyPath = None, ObjectB_HierarchyPath = None):
        self.ObjectA_HierarchyPath = ObjectA_HierarchyPath if ObjectA_HierarchyPath else ''
        self.ObjectB_HierarchyPath = ObjectB_HierarchyPath if ObjectB_HierarchyPath else ''


class Cmd_PeekRequest(Message):
    def __init__(self, Address = 0, Size = 0):
        self.Address = Address
        self.Size = Size

class Cmd_PokeRequest(Message):
    def __init__(self, Address = 0, Bytes = None):
        self.Address = Address
        self.Bytes = Bytes if Bytes else []


class Cmd_RaycastRequest(Message):
    def __init__(self, RaycastPoint = None, RaycastPointUTR = None, CameraHierarchyPath = None):
        self.RaycastPoint = RaycastPoint
        self.RaycastPointUTR = RaycastPointUTR
        self.CameraHierarchyPath = CameraHierarchyPath if CameraHierarchyPath else ''

class Cmd_RaycastResponse(Cmd_GenericResponse):
    def __init__(self,
            RaycastResults = None,
            RaycastResultsUTR = None,

            StackTrace = None,
            ErrorMessage = None,
            InformationMessage = None,
            WarningMessage = None,
            RC = None,
            ReturnedValues = None,
        ):
        super().__init__(StackTrace, ErrorMessage, InformationMessage, WarningMessage, RC, ReturnedValues)
        self.RaycastResults = RaycastResults
        self.RaycastResultsUTR = RaycastResultsUTR


class Cmd_RegisterCollisionMonitorRequest(Message):
    def __init__(self, HierarchyPath = None):
        HierarchyPath = '' if HierarchyPath == None else HierarchyPath


class Cmd_RotateRequest(Message):
    def __init__(self,
            HierarchyPath = None,
            WaitForObject = True,
            Timeout = 30,
            Eulers = None,
            Axis = None,
            EulersUTR = None,
            AxisUTR = None,
            Angle = None,
            XAngle = None,
            YAngle = None,
            ZAngle = None,
            Quant = None,
            RelativeTo = Enums.Space.Self,
            QuantUTR = None,
            RelativeToUTR = Enums.Space.Self,
        ):
        self.HierarchyPath = HierarchyPath if HierarchyPath else ''
        self.WaitForObject = WaitForObject
        self.Timeout = Timeout
        self.Eulers = Eulers
        self.Axis = Axis
        self.EulersUTR = EulersUTR
        self.AxisUTR = AxisUTR
        self.Angle = Angle
        self.XAngle = XAngle
        self.YAngle = YAngle
        self.ZAngle = ZAngle
        self.Quant = Quant
        self.RelativeTo = RelativeTo
        self.QuantUTR = QuantUTR
        self.RelativeToUTR = RelativeToUTR


class Cmd_SetInputFieldTextRequest(Message):
    def __init__(self, Timeout = 30, HierarchyPath = None, WaitForObject = False, Value = None):
        self.Timeout = Timeout
        self.HierarchyPath = HierarchyPath if HierarchyPath else ''
        self.WaitForObject = WaitForObject
        self.Value = Value if Value else ''


class Cmd_SetObjectValueRequest(Message):
    def __init__(self, Timeout = 30, HierarchyPath = None, ObjectFieldOrPropertyName = None, WaitForObject = False, Value = None, CustomSerialization = False, SerializedObjectType = None, Serializer = None):
        self.Timeout = Timeout
        self.HierarchyPath = HierarchyPath if HierarchyPath else ''
        self.ObjectFieldOrPropertyName = ObjectFieldOrPropertyName if ObjectFieldOrPropertyName else ''
        self.WaitForObject = WaitForObject
        self.Value = Value
        self.CustomSerialization = CustomSerialization
        self.SerializedObjectType = SerializedObjectType
        self.Serializer = Serializer


class Cmd_SetTimeScaleRequest(Message):
    def __init__(self, Value = 1.0):
        self.Value = Value


class Cmd_TapRequest(Message):
    def __init__(self, TapCount = 1, FrameCount = 5, X = 0, Y = 0, HierarchyPath = None, CameraHierarchyPath = None):
        self.TapCount = TapCount
        self.FrameCount = FrameCount
        self.X = X
        self.Y = Y
        self.HierarchyPath = HierarchyPath if HierarchyPath else ''
        self.CameraHierarchyPath = CameraHierarchyPath if CameraHierarchyPath else ''


class Cmd_TouchEventRequest(Message):
    def __init__(self, FingerId = 0, AltitudeAngle = 0, AzimulthAngle = 0, Pressure = 1, MaximumPossiblePressure = 1, StartPosition = None, DestinationPosition = None, StartPositionUTR = None, DestinationPositionUTR = None, TapCount = 1, Radius = 20, FrameCount = 5):
        self.FingerId = FingerId
        self.AltitudeAngle = AltitudeAngle
        self.AzimulthAngle = AzimulthAngle
        self.Pressure = Pressure
        self.MaximumPossiblePressure = MaximumPossiblePressure
        self.StartPosition = StartPosition
        self.DestinationPosition = DestinationPosition
        self.StartPositionUTR = StartPositionUTR
        self.DestinationPositionUTR = DestinationPositionUTR
        self.TapCount = TapCount
        self.Radius = Radius
        self.FrameCount = FrameCount


class Cmd_TransferFileRequest(Message):
    def __init__(self):
        pass


class Cmd_UnregisterCollisionMonitorRequest(Message):
    def __init__(self, HierarchyPath = None):
        HeirarchyPath = HierarchyPath if HierarchyPath else ''


class Cmd_WaitForObjectRequest(Message):
    def __init__(self, Timeout = 30, HierarchyPath = None):
        self.Timeout = Timeout
        self.HierarchyPath = HierarchyPath if HierarchyPath else ''


class Cmd_WaitForObjectValueRequest(Message):
    def __init__(self, Timeout = 30, HierarchyPath = None, ObjectFieldOrPropertyName = None, Value = None, CustomSerialization = False, SerializedObjectType = None, Serializer = None):
        self.Timeout = Timeout
        self.HierarchyPath = HierarchyPath if HierarchyPath else ''
        self.ObjectFieldOrPropertyName = ObjectFieldOrPropertyName if ObjectFieldOrPropertyName else ''
        self.Value = Value
        self.CustomSerialization = CustomSerialization
        self.SerializedObjectType = SerializedObjectType
        self.Serializer = Serializer






class Cmd_GetClientListRequest(Message):
    def __init__(self):
        raise NotImplementedError

class Cmd_HandshakeRequest(Message):
    def __init__(self, ProtocolVersion=None, ClientUID = None, channel = None, Recording = False):
        self.ProtocolVersion : str = '' if ProtocolVersion == None else ProtocolVersion
        self.ClientUID : str = '' if ClientUID == None else ClientUID
        self.channel = channel
        self.Recording = Recording

class Cmd_HandshakeResponse(Message):
    def __init__(self, ReceivedTimestamp, RC, GCD):
        self.ReceivedTimestamp = ReceivedTimestamp
        self.RC = RC
        self.GCD = GCD


class Evt_EmptyInput(Message):
    pass

class Cmd_SceneLoaded(Message):
    def __init__(self, SceneName):
        self.SceneName = SceneName

class Cmd_ObjectListResponse(Cmd_GenericResponse):
    def __init__(self,
            Objects = None,

            StackTrace = None,
            ErrorMessage = None,
            InformationMessage = None,
            WarningMessage = None,
            RC = None,
            ReturnedValues = None,
        ):
        super().__init__(StackTrace, ErrorMessage, InformationMessage, WarningMessage, RC, ReturnedValues)
        self.Objects = [] if Objects == None else Objects

class Cmd_VectorResponse(Cmd_GenericResponse):
    def __init__(self,
            Value3 = None,
            Value2 = None,
            Value3UTR = None,
            Value2UTR = None,

            StackTrace = None,
            ErrorMessage = None,
            InformationMessage = None,
            WarningMessage = None,
            RC = None,
            ReturnedValues = None,
        ):
        super().__init__(StackTrace, ErrorMessage, InformationMessage, WarningMessage, RC, ReturnedValues)
        self.Value3 = None if Value3 == None else Value3
        self.Value2 = None if Value2 == None else Value2
        self.Value3UTR = Value3UTR
        self.Value2UTR = Value2UTR