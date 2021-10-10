import os, asyncio
from gdio.ApiClient import ApiClient
from gdio.Enums import HookingObject as hooks

# TODO: Pytest Fixture
class TestFixture:

    def __init__(self):

        self.api = ApiClient()

    async def Connect(self):
        await self.api.Connect('127.0.0.1', 19734, False, 5)
        #print(await self.api.GetConnectedGameDetails())
        #'''
        #await self.api.LoadScene('Scenes/SampleScene')
        await self.api.Wait(2000)
        await self.api.EnableHooks(hooks.ALL)
        await self.api.Wait(1000)
        await self.test_Screenshot(f'{os.getcwd()}\\android-before.png')
        await self.test_Movement()
        await self.test_Screenshot(f'{os.getcwd()}\\android-after.png')
        await self.api.WaitForEmptyInput(5)
        await self.api.DisableHooks(hooks.ALL)
        await self.api.Wait(2000)

    async def test_Screenshot(self, path):
        await self.api.CaptureScreenshot(path, False, True, timeout=10)

    async def test_Movement(self):
        await self.api.AxisPress('Horizontal', 1.0, 500)
        await self.api.Wait(200)
        await self.api.ButtonPress('Jump', 100)
        await self.api.Wait(700)
        await self.api.ButtonPress('Jump', 100)

    async def test_CallMethod(self):
        # Unused
        await self.api.CallMethod("//*[@name='Player']/fn:component('CustomScript')", "CustomMethod", { "string:The Test was run"})

    async def Disconnect(self):
        await self.api.Disconnect()

if __name__ == '__main__':
    Game = TestFixture()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Game.Connect())