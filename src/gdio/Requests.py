from .Objects import Message

CmdIds = {
    "ChangeObjectResolverCacheStateRequest" : 47,
    "GetSceneNameRequest" : 27,
    "CallMethodRequest" : 33,
    "FlushCacheRequest" : 46,
    "GetObjectPositionRequest" : 28,
    "ObjectDistanceRequest" : 45,
    "PokeRequest" : 42,
    "PeekRequest" : 41,
    "ChangeHookStatusRequest" : 40,
    "TapRequest" : 44,
    "GetObjectValueRequest" : 26,
    "TouchEventRequest" : 43,
    "WaitForObjectRequest" : 8,
    "GenericResponse" : 99,
    "GetGameObjectRequest" : 52,
    "InputManagerStateRequest" : 48,
    "ClickObjectRequest" : 31,
    "GetMousePositionRequest" : 30,
    "UnregisterCollisionMonitorRequest" : 51,
    "GetStatisticsRequest" : 50,
    "RegisterCollisionMonitorRequest" : 49,
    "PeekResponse" : 39,
    "MouseDragRequest" : 23,
    "SetObjectValueRequest" : 13,
    "SetInputFieldTextRequest" : 14,
    "ClickRequest" : 32,
    "WaitForObjectValueRequest" : 10,
    "WaitForObjectValueResponse" : 11,
    "SetTimeScaleRequest" : 12,
    "MouseMoveRequest" : 22,
    "MouseMoveToObjectRequest" : 21,
    "RaycastResponse" : 19,
    "NavAgentMoveToPointRequest" : 20,
    "RaycastRequest" : 18,
    "CaptureScreenshotRequest" : 15,
    "CaptureScreenshotResponse" : 16,
    "RotateRequest" : 17,
    "WaitForObjectResponse" : 9,
    "TransferFileRequest" : 34,
    "GetClientListRequest" : 0,
    "HandshakeRequest" : 1,
    "GetObjectInterfacesList" : 35,
    "GetObjectListResponse" : 38,
    "VectorResponse" : 37,
    "GetObjectValueResponse" : 36,
    "Ping" : 2,
    "Broadcast" : 6,
    "DirectMessage" : 7,
    "LoadSceneRequest" : 24,
    "Pong" : 5,
    "GetClientListResponse" : 3,
    "HandshakeResponse" : 4,
    "KeyPressRequest" : 25,
    "GetObjectListRequest" : 29,
}


## TODO: This place is riddled with mutable defaults.
## TODO: These could probably all be dataclasses instead.

class GetClientListRequest(Message):
    def __init__(self):
        raise NotImplementedError

class HandshakeRequest(Message):
    def __init__(self,
            # TODO: dotenv
            ProtocolVersion=None,
            ClientUID = None,
            channel = None,
            Recording = False,
        ):

        
        self.ProtocolVersion : str = '' if ProtocolVersion == None else ProtocolVersion
        self.ClientUID : str = ClientUID
        self.channel = channel
        self.Recording = Recording

class WaitForObjectRequest(Message):
    def __init__(self):
        raise NotImplementedError

class WaitForObjectValueRequest(Message):
    def __init__(self):
        raise NotImplementedError

class SetTimeScaleRequest(Message):
    def __init__(self):
        raise NotImplementedError

class SetObjectValueRequest(Message):
    def __init__(self):
        raise NotImplementedError

class SetInputFieldTextRequest(Message):
    def __init__(self):
        raise NotImplementedError

class CaptureScreenshotRequest(Message):
    # TODO: default filename
    # TODO: stereo capture mode = LeftEye
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

class RotateRequest(Message):
    def __init__(self):
        raise NotImplementedError

class RaycastRequest(Message):
    def __init__(self):
        raise NotImplementedError

class NavAgentMoveToPointRequest(Message):
    def __init__(self):
        raise NotImplementedError

class MouseMoveToObjectRequest(Message):
    def __init__(self):
        raise NotImplementedError

class MouseMoveRequest(Message):
    def __init__(self):
        raise NotImplementedError

class MouseDragRequest(Message):
    def __init__(self):
        raise NotImplementedError

class LoadSceneRequest(Message):
    def __init__(self):
        raise NotImplementedError

class KeyPressRequest(Message):
    def __init__(self):
        raise NotImplementedError

class GetObjectValueRequest(Message):
    def __init__(self, HierarchyPath = '', ObjectFieldOrPropertyName = '', TypeFullName = ''):

        self.HierarchyPath = HierarchyPath
        self.ObjectFieldOrPropertyName = ObjectFieldOrPropertyName
        self.TypeFullName = TypeFullName

class GetSceneNameRequest(Message):
    def __init__(self):
        raise NotImplementedError

class GetObjectPositionRequest(Message):
    def __init__(self, ObjectHierarchyPath = '', CameraHierarchyPath = ''):

        self.ObjectHierarchyPath = ObjectHierarchyPath
        self.CameraHierarchyPath = CameraHierarchyPath

class GetObjectListRequest(Message):
    def __init__(self):
        raise NotImplementedError

class GetMousePositionRequest(Message):
    def __init__(self):
        raise NotImplementedError

class ClickObjectRequest(Message):
    def __init__(self, MouseButtonId = 0, HierarchyPath = '', CameraHierarchyPath = '', IsDoubleClick = False, FrameCount = 5):

        self.MouseButtonId = MouseButtonId
        self.HierarchyPath = HierarchyPath
        self.CameraHierarchyPath = CameraHierarchyPath
        self.IsDoubleClick = IsDoubleClick
        self.FrameCount = FrameCount

class ClickRequest(Message):
    def __init__(self, IsDoubleClick = False, FrameCount = 5, MouseButtonId = 0, X = 0, Y = 0):

        self.IsDoubleClick = IsDoubleClick
        self.FrameCount = FrameCount
        self.MouseButtonId = MouseButtonId
        self.X = X
        self.Y = Y

class CallMethodRequest(Message):
    # TODO: custom serializer
    def __init__(self, HierarchyPath, MethodName, Arguments = [], Arguments2 = [], _serializer = None):

        self.HierarchyPath = HierarchyPath
        self.MethodName = MethodName
        self.Arguments = Arguments
        self.Arguments2 = Arguments2
        self._serializer = _serializer

    def SetArguments(self, arguments = None, serializer = None):
        if arguments == None:
            return
        # TODO: Logging with context awareness
        print('CallMethod: Arguments not yet handled. Passing None')
        return

class TransferFileRequest(Message):
    def __init__(self):
        raise NotImplementedError

class GetObjectInterfacesList(Message):
    def __init__(self):
        raise NotImplementedError

class ChangeHookStatusRequest(Message):
    def __init__(self, KeyboardHooksStatus = True, MouseHooksStatus = True, TouchHooksStatus = True, GamepadHooksStatus = True, BitChanged = 0):

        self.KeyboardHooksStatus = KeyboardHooksStatus
        self.MouseHooksStatus = MouseHooksStatus
        self.TouchHooksStatus = TouchHooksStatus
        self.GamepadHooksStatus = GamepadHooksStatus
        self.BitChanged = BitChanged
        
class PeekRequest(Message):
    def __init__(self):
        raise NotImplementedError

class PokeRequest(Message):
    def __init__(self):
        raise NotImplementedError

class TouchEventRequest(Message):
    def __init__(self):
        raise NotImplementedError

class TapRequest(Message):
    def __init__(self):
        raise NotImplementedError

class ObjectDistanceRequest(Message):
    def __init__(self):
        raise NotImplementedError
                
class FlushCacheRequest(Message):
    def __init__(self):
        raise NotImplementedError

class ChangeObjectResolverCacheStateRequest(Message):
    def __init__(self, STATE = True):

        self.STATE = STATE

class InputManagerStateRequest(Message):
    def __init__(self, IdName, NumberOfFrames, InputType, ChangeValue=0.0):

        self.IdName = IdName
        self.NumberOfFrames = NumberOfFrames
        self.InputType = InputType
        self.ChangeValue = ChangeValue

class RegisterCollisionMonitorRequest(Message):
    def __init__(self):
        raise NotImplementedError

class GetStatisticsRequest(Message):
    def __init__(self):
        raise NotImplementedError

class UnregisterCollisionMonitorRequest(Message):
    def __init__(self):
        raise NotImplementedError

class GetGameObjectRequest(Message):
    def __init__(self, HierarchyPath=''):

        self.HierarchyPath = HierarchyPath
        
class NavAgentMoveToObjectRequest(Message):
    def __init__(self):
        raise NotImplementedError