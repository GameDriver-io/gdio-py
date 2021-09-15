from gdio.ApiClient import ApiClient

class TestFixture:
    def __init__(self):

        self.api = ApiClient()

    def Connect(self):
        self.api.Connect('127.0.0.1', 19734, False, 5)

        print(self.api.GetConnectedGameDetails())

        #self.api.CallMethod("//*[@name='Player']/fn:component('CustomScript')", "CustomMethod", { "string:The Test was run"})

        #self.api.CaptureScreenshot(r'C:\Users\ethan\source\repos\GDIO-py\test.png', False, True)

        self.api.EnableHooks()

        self.api.AxisPress('Horizontal', 1.0, 500)
        self.api.Wait(200)
        self.api.ButtonPress('Jump', 100)
        self.api.Wait(700)
        self.api.ButtonPress('Jump', 100)

        self.api.Wait(500)
        self.Disconnect()

    def Disconnect(self):
        self.api.DisableHooks()
        self.api.Wait(3000)
        self.api.Disconnect()

if __name__ == '__main__':
    Game = TestFixture()
    Game.Connect()