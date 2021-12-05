import pytest, os, asyncio
from gdio.api import ApiClient
from gdio.common.objects import *

TIMEOUT = 5
DEBUG = True

@pytest.fixture
async def api_notConnected():
    api = ApiClient(debug=DEBUG)
    yield api

@pytest.fixture
async def api_dummySockets():
    api = ApiClient(debug=DEBUG)
    reader = asyncio.StreamReader
    writer = asyncio.StreamWriter
    await api.Connect(reader=reader, writer=writer)
    yield api

@pytest.fixture
async def api_connectedlocal():
    api = ApiClient(debug=DEBUG)
    await api.Connect()
    yield api

@pytest.mark.parametrize('method, methodArgs', [
    ('AxisPress',('Horizontal', 1.0, 500, TIMEOUT)),
    ('ButtonPress',('Jump', 100, TIMEOUT)),
    ('CaptureScreenshot',(f'{os.getcwd()}/outputs/screenshot.png', False, True, TIMEOUT)),
    ('ClickEx_Vec2',(MouseButtons.LEFT, Vector2(340, 220), 100, [KeyCode.Space], 1000, [KeyCode.LeftControl], 5, 500, TIMEOUT)),
    ('ClickEx_XY',(MouseButtons.LEFT, 340, 220, 100, [KeyCode.Space], 1000, [KeyCode.LeftControl], 5, 500, TIMEOUT)),
    ('ClickObject',(MouseButtons.LEFT, "//*[@name='Player']", 1000, '', TIMEOUT)),
    ('ClickObjectEx',(MouseButtons.LEFT, "//*[@name='Player']", 1000, '', [KeyCode.Space], 1000, [KeyCode.LeftControl], 5, 500, TIMEOUT)),
    ('Click_Vec2',(MouseButtons.LEFT, Vector2(340, 220), 1000, TIMEOUT)),
    ('Click_XY',(MouseButtons.LEFT, 340, 220, 1000, TIMEOUT)),
    ('DoubleClickEx_Vec2',(MouseButtons.LEFT, Vector2(340, 220), 100, [KeyCode.Space], 1000, [KeyCode.LeftControl], 5, 500, TIMEOUT)),
    ('DoubleClickEx_XY',(MouseButtons.LEFT, 340, 220, 100, [KeyCode.Space], 1000, [KeyCode.LeftControl], 5, 500, TIMEOUT)),
    ('DoubleClickObject',(MouseButtons.LEFT, "//*[@name='Player']", 1000, TIMEOUT)),
    ('DoubleClickObjectEx',(MouseButtons.LEFT, "//*[@name='Player']", 1000, [KeyCode.Space], 1000, [KeyCode.LeftControl], 5, 500, TIMEOUT)),
    ('DoubleClick_Vec2',(MouseButtons.LEFT, Vector2(340, 220), 1000, TIMEOUT)),
    ('DoubleClick_XY',(MouseButtons.LEFT, 340, 220, 1000, TIMEOUT)),
    #('MouseDrag',()),
    #('MouseMoveToObject',()),
    #('MouseMoveToPoint',()),
    #('NavAgentMoveToPoint',()),
    #('RotateObject_AxisAngle',()),
    #('RotateObject_Euler',()),
    #('RotateObject_Quaternion',()),
    #('TapObject',()),
    #('Tap_Vec2',()),
    #('Tap_XY',()),
    #('TouchInput',()),
    #('WaitForEmptyInput',()),
])
@pytest.mark.asyncio
class Test_Methods:
    @pytest.mark.skip
    async def test_InputMethods(self, api_connectedlocal, method, methodArgs):
        api = api_connectedlocal
        method = getattr(api, method)

        await api.EnableHooks(HookingObject.ALL)

        await method(*methodArgs)

        await api.DisableHooks(HookingObject.ALL)

@pytest.mark.asyncio
@pytest.mark.skip
async def test_InputEx(api_connectedlocal):
    api = api_connectedlocal
    await api.EnableHooks(HookingObject.ALL)

    await api.MouseDrag(MouseButtons.LEFT, 340, 220, 1000, 340, 220, True, TIMEOUT)

    await api.DisableHooks(HookingObject.ALL)

# saving for later
'''
@pytest.mark.parametrize('method, methodArgs', [
    ('AxisPress',('Horizontal', 1.0, 500)),
    ('ButtonPress',('Jump', 100)),
    #('CallMethod',(//*[@name='Player']/fn:component('CustomScript')", "CustomMethod", { "string:The Test was run"})),
    #('CallMethod_Void',(//*[@name='Player']/fn:component('CustomScript')", "CustomMethod", { "string:The Test was run"})),
    ('CaptureScreenshot',(f'{os.getcwd()}/screenshot.png', False, True, )),
    #('ClickEx_Vec2',(MouseButtons.LEFT, Vector2(100, 100), 5)), TODO
    #('ClickEx_XY',(MouseButtons.LEFT, 100, 100, 5)), TODO
    ('ClickObject',(MouseButtons.LEFT, "//*[@name='Player']", 1000, '')),
    #('ClickObjectEx',(MouseButtons.LEFT, )), TODO
    ('Click_Vec2',(MouseButtons.LEFT, Vector2(340, 220), 1000)),
    ('Click_XY',(MouseButtons.LEFT, 340, 220, 1000)),
    #('Connect',()),
    #('DisableHooks',()),
    #('DisableObjectCaching',()),
    #('Disconnect',()),
    #('DoubleClickEx_Vec2',()),
    #('DoubleClickEx_XY',()),
    #('DoubleClickObject',()),
    #('DoubleClickObjectEx',()),
    ('DoubleClick_Vec2',(MouseButtons.LEFT, Vector2(340, 220), 1000)),
    ('DoubleClick_XY',(MouseButtons.LEFT, 340, 220, 1000)),
    #('EnableHooks',()),
    #('EnableObjectCaching',()),
    #('FlushObjectLookupCache',()),
    #('GetConnectedGameDetails',()),
    #('GetLastFPS',()),
    #('GetNextCollisionEvent',()),
    #('GetObjectDistance',()),
    #('GetObjectFieldValue',()),
    #('GetObjectFieldValueByName',()),
    #('GetObjectList',()),
    #('GetObjectPosition',()),
    #('GetSceneName',()),
    #('GetVersionString',()),
    #('KeyPress',()),
    #('Launch',()),
    #('LoadScene',()),
    #('ManageAutoPlay',()),
    #('MouseDrag',()),
    #('MouseMoveToObject',()),
    #('MouseMoveToPoint',()),
    #('NavAgentMoveToPoint',()),
    #('Raycast',()),
    #('RegisterCollisionMonitor',()),
    #('RotateObject_AxisAngle',()),
    #('RotateObject_Euler',()),
    #('RotateObject_Quaternion',()),
    #('SetInputFieldText',()),
    #('SetObjectFieldValue',()),
    #('TapObject',()),
    #('Tap_Vec2',()),
    #('Tap_XY',()),
    #('TerminateGame',()),
    #('ToggleEditorPause',()),
    #('ToggleEditorPlay',()),
    #('TouchInput',()),
    #('UnregisterCollisionMonitor',()),
    #('Wait',()),
    #('WaitForCollisionEvent',()),
    #('WaitForEmptyInput',()),
    #('waitForObject',()),
    #('waitForObjectValue', ()),
])
'''