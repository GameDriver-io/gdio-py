import pytest, os, asyncio
from gdio.ApiClient import ApiClient
import gdio.Exceptions as Exceptions
from gdio.Enums import KeyCode, HookingObject

@pytest.fixture
async def api_notConnected():
    api = ApiClient()
    yield api

@pytest.fixture
async def api_dummySockets():
    api = ApiClient()
    reader = asyncio.StreamReader
    writer = asyncio.StreamWriter
    await api.Connect(reader=reader, writer=writer)
    yield api

@pytest.fixture
async def api_connectedlocal():
    api = ApiClient()
    await api.Connect()
    yield api

@pytest.mark.parametrize('method, methodArgs', [
    ('AxisPress', ('Horizontal', 1.0, 500)),
    ('ButtonPress', ('Jump', 100)),
    ('CallMethod', ("//*[@name='Player']/fn:component('CustomScript')", "CustomMethod", { "string:The Test was run"})),
    ('CaptureScreenshot', (f'{os.getcwd()}\\before.png', False, True)),
    ('Click', ('A', 1.0, 1.0, 5)), # TODO
    ('ClickEx', ('A', 1.0, 1.0, 5)), # TODO
    ('ClickObject', ()), # TODO
    ('ClickObjectEx', ()), # TODO
    ('DisableHooks', ()),
    ('DisableObjectCaching', ()),
    ('DoubleClick', ()), # TODO
    ('DoubleClickEx', ()), # TODO
    ('DoubleClickObject', ()), # TODO
    ('EnableHooks', ()),
    ('EnableObjectCaching', ()),
    ('FlushObjectLookupCache', ()),
    ('GetConnectedGameDetails', ()),
    ('GetLastFPS', ()), # TODO
    ('GetNextCollisionEvent', ()),# TODO
    ('GetObjectList', ()),
    ('GetSceneName', ()),
    ('WaitForEmptyInput', ()),
])
@pytest.mark.asyncio
class Test_Methods:
    @pytest.mark.skip
    async def test_ClientNotConnected(self, api_notConnected, method, methodArgs):
        api = api_notConnected
        with pytest.raises(Exceptions.ClientNotConnectedError):
            await eval(f'api.{method}{methodArgs}')

@pytest.mark.asyncio
@pytest.mark.skip
async def test_AxisPress(api_connectedlocal):
    api = api_connectedlocal
    await api.LoadScene('SampleScene')
    await api.AxisPress('Horizontal', 1.0, 500)

@pytest.mark.asyncio
@pytest.mark.skip
async def test_ButtonPress(api_connectedlocal):
    api = api_connectedlocal
    await api.LoadScene('SampleScene')
    await api.ButtonPress('Jump', 100)

@pytest.mark.asyncio
@pytest.mark.skip
async def test_KeyPress(api_connectedlocal):
    api = api_connectedlocal
    #await api.LoadScene('SampleScene')
    await api.EnableHooks(HookingObject.ALL)
    await api.Wait(1000)
    await api.KeyPress([KeyCode.Space], 100)
    await api.DisableHooks(HookingObject.ALL)

#('CallMethod_Void', ("//*[@name='Player']/fn:component('CustomScript')", "Call_Test")),

@pytest.mark.asyncio
async def test_CallMethod(api_connectedlocal):
    api = api_connectedlocal
    await api.CallMethod_Void("//*[@name='Player']/fn:component('CustomScript')", "Args_Test", ["string:The Test was run"])