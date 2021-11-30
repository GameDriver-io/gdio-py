# Still used as a fallback because logging doesnt work if pytest doesnt run to completion

import os, asyncio
from gdio.api import ApiClient
from gdio.common.objects import *

class TestFixture:

    def __init__(self):

        self.api = ApiClient(debug=True)

    async def Connect(self):
        await self.api.Connect('127.0.0.1', 19734, False, 5)

        await self.api.Wait(1000)
        await self.load_scene(self.api, 'MouseMoveObject')

        await self.api.MouseMoveToObject("//*[@name='Cylinder']", 10)
        
    async def load_scene(self, api, name):
        await api.LoadScene(name, 5)
        scene_name = await api.GetSceneName(5)
        assert scene_name == name

if __name__ == '__main__':
    Game = TestFixture()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Game.Connect())