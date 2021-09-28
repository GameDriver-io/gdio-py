import os, asyncio
from gdio.ApiClient import ApiClient

# TODO: Pytest Fixture
class TestFixture:

    def __init__(self):

        self.api = ApiClient()

    async def Connect(self):
        await self.api.Connect('127.0.0.1', 19734, False, 5)
        #print(await self.api.GetConnectedGameDetails())
        await asyncio.sleep(2)
        
        ## <Test Methods>
        await self.api.Wait(200)
        await self.test_Screenshot(f'{os.getcwd()}\\before.png')
        await self.api.EnableHooks()
        await self.test_Movement()
        await self.api.WaitForEmptyInput(5)
        await self.api.DisableHooks()
        await self.test_Screenshot(f'{os.getcwd()}\\after.png')
        await self.api.Wait(200)
        ## </Test Methods>

        await self.Disconnect()

    async def test_Screenshot(self, path):
        await self.api.CaptureScreenshot(path, False, True)

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
    