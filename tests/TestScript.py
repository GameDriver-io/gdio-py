# Still used as a fallback because logging doesnt work if pytest doesnt run to completion

from logging import debug
import os, asyncio
from gdio.api import ApiClient
from gdio.common.objects import *

import time

class TestFixture:

    def __init__(self):
        pass

    async def test(self):
        api = ApiClient(debug=True)
        isConnected = await api.Connect()
        if not isConnected:
            return

        await api.Wait(1000)
        gcd = api.GetConnectedGameDetails()
        print(gcd)

        await api.EnableHooks(HookingObject.ALL)

        await api.ButtonPress('Jump', 100)

        await api.DisableHooks(HookingObject.ALL)

        await api.Wait(1000)
        await api.Disconnect()


if __name__ == '__main__':
    Game = TestFixture()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Game.test())