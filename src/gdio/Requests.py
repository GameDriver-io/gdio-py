from .Objects import Message

## TODO: This place is riddled with mutable defaults.
## TODO: These could probably all be dataclasses instead.

class GetClientListRequest(Message):
    def __init__(self):
        super().__init__(0)
        raise NotImplementedError

class HandshakeRequest(Message):
    def __init__(self,
            ClientUID,

            # TODO: dotenv
            ProtocolVersion='2.04.13.2021'
        ):
        super().__init__(1)

        
        self.ProtocolVersion : str = ProtocolVersion
        self.ClientUID : str = ClientUID
        self.channel = None
        self.Recording = False

class WaitForObjectRequest(Message):
    def __init__(self):
        super().__init__(8)
        raise NotImplementedError

class WaitForObjectValueRequest(Message):
    def __init__(self):
        super().__init__(10)
        raise NotImplementedError

class SetTimeScaleRequest(Message):
    def __init__(self):
        super().__init__(12)
        raise NotImplementedError

class SetObjectValueRequest(Message):
    def __init__(self):
        super().__init__(13)
        raise NotImplementedError

class SetInputFieldTextRequest(Message):
    def __init__(self):
        super().__init__(14)
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
        super().__init__(15)

        self.StoreInGameFolder = False
        self.Filename = Filename if Filename != None else ''
        self.SuperSize = 1
        self.Mode = 1

class RotateRequest(Message):
    def __init__(self):
        super().__init__(17)
        raise NotImplementedError

class RaycastRequest(Message):
    def __init__(self):
        super().__init__(18)
        raise NotImplementedError

class NavAgentMoveToPointRequest(Message):
    def __init__(self):
        super().__init__(20)
        raise NotImplementedError

class MouseMoveToObjectRequest(Message):
    def __init__(self):
        super().__init__(21)
        raise NotImplementedError

class MouseMoveRequest(Message):
    def __init__(self):
        super().__init__(22)
        raise NotImplementedError

class MouseDragRequest(Message):
    def __init__(self):
        super().__init__(23)
        raise NotImplementedError

class LoadSceneRequest(Message):
    def __init__(self):
        super().__init__(24)
        raise NotImplementedError

class KeyPressRequest(Message):
    def __init__(self):
        super().__init__(25)
        raise NotImplementedError

class GetObjectValueRequest(Message):
    def __init__(self, HierarchyPath = '', ObjectFieldOrPropertyName = '', TypeFullName = ''):
        super().__init__(26)

        self.HierarchyPath = HierarchyPath
        self.ObjectFieldOrPropertyName = ObjectFieldOrPropertyName
        self.TypeFullName = TypeFullName

class GetSceneNameRequest(Message):
    def __init__(self):
        super().__init__(27)
        raise NotImplementedError

class GetObjectPositionRequest(Message):
    def __init__(self, ObjectHierarchyPath = '', CameraHierarchyPath = ''):
        super().__init__(28)

        self.ObjectHierarchyPath = ObjectHierarchyPath
        self.CameraHierarchyPath = CameraHierarchyPath

class GetObjectListRequest(Message):
    def __init__(self):
        super().__init__(29)
        raise NotImplementedError

class GetMousePositionRequest(Message):
    def __init__(self):
        super().__init__(30)
        raise NotImplementedError

class ClickObjectRequest(Message):
    def __init__(self, MouseButtonId = 0, HierarchyPath = '', CameraHierarchyPath = '', IsDoubleClick = False, FrameCount = 5):
        super().__init__(31)

        self.MouseButtonId = MouseButtonId
        self.HierarchyPath = HierarchyPath
        self.CameraHierarchyPath = CameraHierarchyPath
        self.IsDoubleClick = IsDoubleClick
        self.FrameCount = FrameCount

class ClickRequest(Message):
    def __init__(self, IsDoubleClick = False, FrameCount = 5, MouseButtonId = 0, X = 0, Y = 0):
        super().__init__(32)

        self.IsDoubleClick = IsDoubleClick
        self.FrameCount = FrameCount
        self.MouseButtonId = MouseButtonId
        self.X = X
        self.Y = Y

class CallMethodRequest(Message):
    # TODO: custom serializer
    def __init__(self, HierarchyPath, MethodName, Arguments = [], Arguments2 = [], _serializer = None):
        super().__init__(33)

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
        super().__init__(34)
        raise NotImplementedError

class GetObjectInterfacesList(Message):
    def __init__(self):
        super().__init__(35)
        raise NotImplementedError

class ChangeHookStatusRequest(Message):
    def __init__(self, KeyboardHooksStatus = True, MouseHooksStatus = True, TouchHooksStatus = True, GamepadHooksStatus = True, BitChanged = 0):
        super().__init__(40)

        self.KeyboardHooksStatus = KeyboardHooksStatus
        self.MouseHooksStatus = MouseHooksStatus
        self.TouchHooksStatus = TouchHooksStatus
        self.GamepadHooksStatus = GamepadHooksStatus
        self.BitChanged = BitChanged
        
class PeekRequest(Message):
    def __init__(self):
        super().__init__(41)
        raise NotImplementedError

class PokeRequest(Message):
    def __init__(self):
        super().__init__(42)
        raise NotImplementedError

class TouchEventRequest(Message):
    def __init__(self):
        super().__init__(43)
        raise NotImplementedError

class TapRequest(Message):
    def __init__(self):
        super().__init__(44)
        raise NotImplementedError

class ObjectDistanceRequest(Message):
    def __init__(self):
        super().__init__(45)
        raise NotImplementedError
                
class FlushCacheRequest(Message):
    def __init__(self):
        super().__init__(46)
        raise NotImplementedError

class ChangeObjectResolverCacheStateRequest(Message):
    def __init__(self, STATE = True):
        super().__init__(47)

        self.STATE = STATE

class InputManagerStateRequest(Message):
    def __init__(self, IdName, NumberOfFrames, InputType, ChangeValue=0.0):
        super().__init__(48)

        self.IdName = IdName
        self.NumberOfFrames = NumberOfFrames
        self.InputType = InputType
        self.ChangeValue = ChangeValue

class RegisterCollisionMonitorRequest(Message):
    def __init__(self):
        super().__init__(49)
        raise NotImplementedError

class GetStatisticsRequest(Message):
    def __init__(self):
        super().__init__(50)
        raise NotImplementedError

class UnregisterCollisionMonitorRequest(Message):
    def __init__(self):
        super().__init__(51)
        raise NotImplementedError

class GetGameObjectRequest(Message):
    def __init__(self, HierarchyPath=''):
        super().__init__(52)

        self.HierarchyPath = HierarchyPath
        
class NavAgentMoveToObjectRequest(Message):
    def __init__(self):
        # NOTE: not the official cmdID
        super().__init__(100)
        raise NotImplementedError