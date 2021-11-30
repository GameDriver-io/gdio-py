import pytest, os, asyncio
from gdio.api import ApiClient
from gdio.common.objects import *

TIMEOUT = 5
DEBUG = True


@pytest.fixture
async def api_connection():
    # Setup
    api = ApiClient(debug=DEBUG)
    await api.Connect('127.0.0.1', 19734, False, TIMEOUT)
    await api.EnableHooks(HookingObject.ALL)

    yield api

    # Tear down
    await api.DisableHooks(HookingObject.ALL)
    await api.Disconnect()

async def load_scene(api, name):
    await api.LoadScene(name, TIMEOUT)
    scene_name = await api.GetSceneName(TIMEOUT)
    assert scene_name == name


@pytest.mark.asyncio
async def test_MouseMoveObject(api_connection):
    api = api_connection

    await api.Wait(1000)
    await load_scene(api, 'MouseMoveObject')

    await api.MouseMoveToObject("//*[@name='Cylinder']", 10)
    # TODO: Drag
