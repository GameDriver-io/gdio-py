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


@pytest.mark.asyncio
async def test_main(api_connection):
    api = api_connection

    await api.Wait(1000)
    scene_name = await api.GetSceneName(TIMEOUT)
    assert scene_name == 'Menu'

    #await api.Tap_XY(600, 275, 1, 5, TIMEOUT)