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

class Cmd_GetClientListRequest(Message):
    def __init__(self):
        raise NotImplementedError

class Cmd_HandshakeRequest(Message):
    def __init__(self,
            ProtocolVersion=None,
            ClientUID = None,
            channel = None,
            Recording = False,
        ):
        self.ProtocolVersion : str = '' if ProtocolVersion == None else ProtocolVersion
        self.ClientUID : str = '' if ClientUID == None else ClientUID
        self.channel = channel
        self.Recording = Recording

class Cmd_WaitForObjectRequest(Message):
    def __init__(self):
        raise NotImplementedError

class Cmd_WaitForObjectValueRequest(Message):
    def __init__(self):
        raise NotImplementedError

class Cmd_SetTimeScaleRequest(Message):
    def __init__(self):
        raise NotImplementedError

class Cmd_SetObjectValueRequest(Message):
    def __init__(self):
        raise NotImplementedError

class Cmd_SetInputFieldTextRequest(Message):
    def __init__(self):
        raise NotImplementedError

class Cmd_CaptureScreenshotRequest(Message):
    # TODO: default filename
    # TODO: stereo capture mode = LeftEye (Enum)
    def __init__(self,
            StoreInGameFolder = False,
            Filename = None,
            SuperSize = 1,
            Mode = 1
        ):
        self.StoreInGameFolder = False
        self.Filename = Filename if Filename != None else ''
        self.SuperSize = 1
        self.Mode = 1

class Cmd_RotateRequest(Message):
    def __init__(self):
        raise NotImplementedError

class Cmd_RaycastRequest(Message):
    def __init__(self):
        raise NotImplementedError

class Cmd_NavAgentMoveToPointRequest(Message):
    def __init__(self):
        raise NotImplementedError

class Cmd_MouseMoveToObjectRequest(Message):
    def __init__(self):
        raise NotImplementedError

class Cmd_MouseMoveRequest(Message):
    def __init__(self):
        raise NotImplementedError

class Cmd_MouseDragRequest(Message):
    def __init__(self):
        raise NotImplementedError

class Cmd_LoadSceneRequest(Message):
    def __init__(self, SceneName = None):
        self.SceneName = '' if SceneName == None else SceneName

class Cmd_KeyPressRequest(Message):
    def __init__(self):
        raise NotImplementedError

class Cmd_GetObjectValueRequest(Message):
    def __init__(self, HierarchyPath = None, ObjectFieldOrPropertyName = None, TypeFullName = None):

        self.HierarchyPath = '' if HierarchyPath == None else HierarchyPath
        self.ObjectFieldOrPropertyName = '' if ObjectFieldOrPropertyName == None else ObjectFieldOrPropertyName
        self.TypeFullName = '' if TypeFullName == None else TypeFullName

class Cmd_GetSceneNameRequest(Message):
    def __init__(self):
        raise NotImplementedError

class Cmd_GetObjectPositionRequest(Message):
    def __init__(self, ObjectHierarchyPath = None, CameraHierarchyPath = None):

        self.ObjectHierarchyPath = '' if ObjectHierarchyPath == None else ObjectHierarchyPath
        self.CameraHierarchyPath = '' if CameraHierarchyPath == None else CameraHierarchyPath

class Cmd_GetObjectListRequest(Message):
    def __init__(self):
        raise NotImplementedError

class Cmd_GetMousePositionRequest(Message):
    def __init__(self):
        raise NotImplementedError

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

class Cmd_CallMethodRequest(Message):
    # TODO: custom serializer
    def __init__(self, HierarchyPath = None, MethodName = None, Arguments = None, Arguments2 = None, _serializer = None):
        self.HierarchyPath = '' if HierarchyPath == None else HierarchyPath
        self.MethodName = '' if MethodName == None else MethodName
        self.Arguments = [] if Arguments == None else Arguments
        self.Arguments2 = [] if Arguments2 == None else Arguments2
        self._serializer = _serializer

    def SetArguments(self, arguments = None, serializer = None):
        if arguments == None:
            return
        # TODO: Logging with context awareness
        print('CallMethod: Arguments not yet handled. Passing None')
        return

class Cmd_TransferFileRequest(Message):
    def __init__(self):
        raise NotImplementedError

class Cmd_GetObjectInterfacesList(Message):
    def __init__(self):
        raise NotImplementedError

class Cmd_ChangeHookStatusRequest(Message):
    def __init__(self, KeyboardHooksStatus = True, MouseHooksStatus = True, TouchHooksStatus = True, GamepadHooksStatus = True, BitChanged = 0):
        self.KeyboardHooksStatus = KeyboardHooksStatus
        self.MouseHooksStatus = MouseHooksStatus
        self.TouchHooksStatus = TouchHooksStatus
        self.GamepadHooksStatus = GamepadHooksStatus
        self.BitChanged = BitChanged
        
class Cmd_PeekRequest(Message):
    def __init__(self):
        raise NotImplementedError

class Cmd_PokeRequest(Message):
    def __init__(self):
        raise NotImplementedError

class Cmd_TouchEventRequest(Message):
    def __init__(self):
        raise NotImplementedError

class Cmd_TapRequest(Message):
    def __init__(self):
        raise NotImplementedError

class Cmd_ObjectDistanceRequest(Message):
    def __init__(self):
        raise NotImplementedError
                
class Cmd_FlushCacheRequest(Message):
    def __init__(self):
        raise NotImplementedError

class Cmd_ChangeObjectResolverCacheStateRequest(Message):
    def __init__(self, STATE = True):

        self.STATE = STATE

class Cmd_InputManagerStateRequest(Message):
    def __init__(self, IdName, NumberOfFrames, InputType, ChangeValue=0.0):
        self.IdName = IdName
        self.NumberOfFrames = NumberOfFrames
        self.InputType = InputType
        self.ChangeValue = ChangeValue

class Cmd_RegisterCollisionMonitorRequest(Message):
    def __init__(self):
        raise NotImplementedError

class Cmd_GetStatisticsRequest(Message):
    def __init__(self):
        raise NotImplementedError

class Cmd_UnregisterCollisionMonitorRequest(Message):
    def __init__(self):
        raise NotImplementedError

class Cmd_GetGameObjectRequest(Message):
    def __init__(self, HierarchyPath=''):

        self.HierarchyPath = HierarchyPath
        
class Cmd_NavAgentMoveToObjectRequest(Message):
    def __init__(self):
        raise NotImplementedError

class Cmd_GenericResponse(Message):
    def __init__(self,
            StackTrace         = None,
            ErrorMessage       = None,
            InformationMessage = None,
            WarningMessage     = None,
            RC                 = Enums.ResponseCode.OK,
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

class Cmd_GetObjectValueResponse(Cmd_GenericResponse):
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

class Cmd_CaptureScreenshotResponse(Cmd_GenericResponse):
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

class Cmd_HandshakeResponse(Message):
    def __init__(self,
            ReceivedTimestamp,
            RC,
            GCD,
        ):
        self.ReceivedTimestamp = ReceivedTimestamp
        self.RC = RC
        self.GCD = GCD


class Evt_EmptyInput(Message):
    pass

class Cmd_SceneLoaded(Message):
    def __init__(self, SceneName):
        self.SceneName = SceneName