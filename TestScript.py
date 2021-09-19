import asyncio
from gdio.ApiClient import ApiClient

class TestFixture:

    def __init__(self):

        self.api = ApiClient()

    async def Connect(self):
        await self.api.Connect('127.0.0.1', 19734, False, 5)
        #print(await self.api.GetConnectedGameDetails())
        await asyncio.sleep(2)
        
        ## <Test Methods>
        await self.api.Wait(200)
        await self.test_Screenshot(r'C:\Users\ethan\source\repos\GDIO-py\before.png')
        await self.test_Movement()
        await self.test_Screenshot(r'C:\Users\ethan\source\repos\GDIO-py\after.png')
        await self.api.Wait(200)
        ## </Test Methods>

        await self.Disconnect()

    async def test_Screenshot(self, path):
        await self.api.CaptureScreenshot(path, False, True)

    async def test_Movement(self):
        await self.api.EnableHooks()
        await self.api.AxisPress('Horizontal', 1.0, 500)
        await self.api.Wait(200)
        await self.api.ButtonPress('Jump', 100)
        await self.api.Wait(700)
        await self.api.ButtonPress('Jump', 100)
        await self.api.DisableHooks()

    async def test_CallMethod(self):
        await self.api.CallMethod("//*[@name='Player']/fn:component('CustomScript')", "CustomMethod", { "string:The Test was run"})

    async def Disconnect(self):
        await self.api.Disconnect()

if __name__ == '__main__':
    Game = TestFixture()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        Game.Connect()
    )
    