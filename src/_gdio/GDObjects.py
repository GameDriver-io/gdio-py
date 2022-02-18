from dataclasses import dataclass
from enum import IntEnum, auto
from collections import namedtuple

Vector2 = namedtuple('Vector2', ['x', 'y'])
Vector3 = namedtuple('Vector3', ['x', 'y'])
Vector4 = namedtuple('Vector4', ['x', 'y'])

@dataclass
class Quaternion:
    x: float
    y: float
    z: float
    w: float

@dataclass
class FrustumPlanes:
    Left: float
    Right: float
    Top: float
    Bottom: float
    zNear: float
    zFar: float

class Matrix4x4:
    def __init__(self,
            determinant: float,
            inverse, # Matrix4x4
            isIdentitiy: bool,
            lossyScale: Vector3,
            rotation: Quaternion,
            transpose, # Matrix4x4
            m00: float,
            m01: float,
            m02: float,
            m03: float,
            m10: float,
            m11: float,
            m12: float,
            m13: float,
            m20: float,
            m21: float,
            m22: float,
            m23: float,
            m30: float,
            m31: float,
            m32: float,
            m33: float,
        ):
        
        self.determinant = determinant
        self.inverse = inverse
        self.isIdentitiy = isIdentitiy
        self.lossyScale = lossyScale
        self.rotation = rotation
        self.transpose = transpose
        self.m00 = m00
        self.m01 = m01
        self.m02 = m02
        self.m03 = m03
        self.m10 = m10
        self.m11 = m11
        self.m12 = m12
        self.m13 = m13
        self.m20 = m20
        self.m21 = m21
        self.m22 = m22
        self.m23 = m23


class COLLISION_EVENT(IntEnum):
    COLLISION_ENTER = auto()
    COLLISION_STAY = auto()
    COLLISION_EXIT = auto()

@dataclass
class Color:
    r: float
    g: float
    b: float
    a: float

@dataclass
class LiteObject:
    name: str
    instanceId: int

class Transform:
    def __init__(self,
            childCount: int,
            eulerAngles: Vector3,
            forward: Vector3,
            hasChanged: bool,
            hierarchyCapacity: int,
            hierarchyCount: int,
            localEulerAngles: Vector3,
            localPosition: Vector3,
            localRotation: Quaternion,
            localScale: Vector3,
            localToWorldMatrix: Matrix4x4,
            lossyScale: Vector3,
            parent,
            position: Vector3,
            right: Vector3,
            root, # Transform
            rotation: Quaternion,
            up: Vector3,
            worldToLocalMatrix: Matrix4x4,
        ):
        self.childCount = childCount
        self.eulerAngles = eulerAngles
        self.forward = forward
        self.hasChanged = hasChanged
        self.hierarchyCapacity = hierarchyCapacity
        self.hierarchyCount = hierarchyCount
        self.localEulerAngles = localEulerAngles
        self.localPosition = localPosition
        self.localRotation = localRotation
        self.localScale = localScale
        self.localToWorldMatrix = localToWorldMatrix
        self.lossyScale = lossyScale
        self.parent = parent
        self.position = position
        self.right = right
        self.root = root
        self.rotation = rotation
        self.up = up
        self.worldToLocalMatrix = worldToLocalMatrix

class LiteGameObject(LiteObject):
    tag: str
    activeSelf: bool
    sceneName: str
    scenePath: str
    sceneId: int
    hashCode: int
    parentHashCode: int
    position: Vector3
    LocalPosition: Vector3
    rotation: Quaternion
    typeFullName: str
    hierarchyPath: str
    Components: list
    transform: Transform

class PhysicsMaterialCombine(IntEnum):
    Average = 0
    Multiply = 1
    Minimum = 2
    Maximum = 3

class PhysicsMaterial(LiteObject):
    bounciness: float
    dynamicFriction: float
    staticFriction: float
    frictionCombine: PhysicsMaterialCombine
    bounceCombine: PhysicsMaterialCombine


class CollisionDetectionMode(IntEnum):
    Discrete = 0
    Continuous = 1
    ContinuousDynamic = 2
    ContinuousSpeculative = 3

class RigidBodyInterpolation(IntEnum):
    None_ = auto()
    Interpolate = auto()
    Extrapolate = auto()

class RigidBodyConstraints(IntEnum):
    None_ = 0
    FreezePositionX = 2
    FreezePositionY = 4
    FreezePositionZ = 8
    FreezeRotationX = 16
    FreezeRotationY = 32
    FreezeRotationZ = 64
    FreezePosition = 14
    FreezeRotation = 112
    FreezeAll = 126

@dataclass
class Rigidbody:
    angularDrag: float
    angularVelocity: Vector3
    centerOfMass: Vector3
    CollisionDetectionMode: CollisionDetectionMode
    constraints: RigidBodyConstraints
    detectCollisions: bool
    drag: float
    freezeRotation: bool
    inertiaTensor: Vector3
    isKinematic: bool
    mass: float
    maxAngularVelocity: float
    maxDepenetrationVelocity: float
    position: Vector3
    rotation: Quaternion
    sleepThreshold: float
    solverIterations: int
    solverVelocityIterations: int
    useGravity: bool
    velocity: Vector3
    worldCenterOfMass: Vector3

@dataclass
class Bounds:
    center: Vector3
    extents: Vector3
    max: Vector3
    min: Vector3
    size: Vector3

@dataclass
class Collider:
    attachedRigidbody: Rigidbody
    bounds: Bounds
    contactOffset: float
    enabled: bool
    isTrigger: bool
    material: PhysicsMaterial
    sharedMaterial: PhysicsMaterial

@dataclass
class ContactPoint:
    point: Vector3
    normal: Vector3
    distance: float
    otherCollider: Collider
    thisCollider: Collider

class CoordinateConversion(IntEnum):
    None_ = auto()
    Local = auto()
    WorldToScreenPoint = auto()
    WorldToViewportPoint = auto()
    ScreenToWorldPoint = auto()
    ScreenToViewportPoint = auto()
    ViewportToWorldPoint = auto()
    ViewportToScreenPoint = auto()

@dataclass
class GameConnectionDetails:
    Addr: str
    Port: int
    GamePath: str
    IsEditor: bool
    Platform: str

@dataclass
class GDIOUnitTest:
    IsUnitTest: bool

class LiteComponent(LiteObject):
    gameObject: LiteGameObject
    tag: str
    transform: Transform
    typeFullName: str
    hierarchyPath: str

class LogLevel(IntEnum):
    Error = auto()
    Warning = auto()
    Info = auto()
    Debug = auto()
    Trace = auto()

'''
class LogEventArgs(dataclasses.dataclass):
    Level: LogLevel
    Message: object
'''

class MouseButtons(IntEnum):
    Left = auto()
    Right = auto()
    Middle = auto()

class ObjectListFilter(IntEnum):
    Untagged = auto()
    Tagged = auto()
    All = auto()

@dataclass
class RaycastResult:
    type: str
    tag: str
    name: str
    hasButton: bool
    point: Vector3
    typeFullName: str

class Space(IntEnum):
    World = auto()
    Local = auto()