# Still used as a fallback because logging doesnt work if pytest doesnt run to completion

import os, asyncio
from gdio.api import ApiClient
from gdio.common.objects import *

class TestFixture:

    def __init__(self):

        self.api = ApiClient(debug=True)

    async def Connect(self):
        await self.api.Connect('127.0.0.1', 19734, False, 5)
        #print(await self.api.GetConnectedGameDetails())
        #'''
        #await self.api.LoadScene('Scenes/SampleScene')
        await self.api.Wait(2000)
        await self.api.EnableHooks(HookingObject.ALL)
        await self.api.Wait(1000)
        
        await self.api.Tap_XY(600, 275, 1, 5)

if __name__ == '__main__':
    Game = TestFixture()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Game.Connect())