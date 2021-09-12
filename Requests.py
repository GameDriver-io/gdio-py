from Objects import Message

class GetClientListRequest(Message):
    def __init__(self):
        super().__init__(0)

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

class WaitForObjectValueRequest(Message):
    def __init__(self):
        super().__init__(10)

class SetTimeScaleRequest(Message):
    def __init__(self):
        super().__init__(12)

class SetObjectValueRequest(Message):
    def __init__(self):
        super().__init__(13)

class SetInputFieldTextRequest(Message):
    def __init__(self):
        super().__init__(14)

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

class RaycastRequest(Message):
    def __init__(self):
        super().__init__(18)

class NavAgentMoveToPointRequest(Message):
    def __init__(self):
        super().__init__(20)

class MouseMoveToObjectRequest(Message):
    def __init__(self):
        super().__init__(21)

class MouseMoveRequest(Message):
    def __init__(self):
        super().__init__(22)

class MouseDragRequest(Message):
    def __init__(self):
        super().__init__(23)

class LoadSceneRequest(Message):
    def __init__(self):
        super().__init__(24)

class KeyPressRequest(Message):
    def __init__(self):
        super().__init__(25)

class GetObjectValueRequest(Message):
    def __init__(self, HierarchyPath = '', ObjectFieldOrPropertyName = '', TypeFullName = ''):
        super().__init__(26)

        self.HierarchyPath = HierarchyPath
        self.ObjectFieldOrPropertyName = ObjectFieldOrPropertyName
        self.TypeFullName = TypeFullName

class GetSceneNameRequest(Message):
    def __init__(self):
        super().__init__(27)

class GetObjectPositionRequest(Message):
    def __init__(self, ObjectHierarchyPath = '', CameraHierarchyPath = ''):
        super().__init__(28)

        self.ObjectHierarchyPath = ObjectHierarchyPath
        self.CameraHierarchyPath = CameraHierarchyPath

class GetObjectListRequest(Message):
    def __init__(self):
        super().__init__(29)

class GetMousePositionRequest(Message):
    def __init__(self):
        super().__init__(30)

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

class GetObjectInterfacesList(Message):
    def __init__(self):
        super().__init__(35)

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

class PokeRequest(Message):
    def __init__(self):
        super().__init__(42)

class TouchEventRequest(Message):
    def __init__(self):
        super().__init__(43)

class TapRequest(Message):
    def __init__(self):
        super().__init__(44)

class ObjectDistanceRequest(Message):
    def __init__(self):
        super().__init__(45)
                
class FlushCacheRequest(Message):
    def __init__(self):
        super().__init__(46)

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

class GetStatisticsRequest(Message):
    def __init__(self):
        super().__init__(50)

class UnregisterCollisionMonitorRequest(Message):
    def __init__(self):
        super().__init__(51)

class GetGameObjectRequest(Message):
    def __init__(self, HierarchyPath=''):
        super().__init__(52)

        self.HierarchyPath = HierarchyPath
        
class NavAgentMoveToObjectRequest(Message):
    def __init__(self):
        super().__init__()