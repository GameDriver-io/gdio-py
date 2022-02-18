# Still used as a fallback because logging doesnt work if pytest doesnt run to completion

from dis import dis
from logging import debug
import os, asyncio
from gdio.api import ApiClient
from gdio.common.objects import *

import ctypes

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

    async def test_callmethod(self):
        api = ApiClient(debug=True)

        isConnected = await api.Connect(autoplay=True)

        if not isConnected:
            return

        await api.Wait(1000)

        await api.CallMethod("//*[@name='Player']/fn:component('TestScript')", "Sum_Void", [1, 1])
        await api.CallMethod("//*[@name='Player']/fn:component('TestScript')", "log4")
        returnValue = await api.CallMethod("//*[@name='Player']/fn:component('TestScript')", "Sum_Return", [1, 1])
        print(returnValue)

        await api.Wait(1000)
        await api.Disconnect()

        await api.Wait(100)
        api.StopEditorPlay()

    async def test_collisionmonitor(self):
        api = ApiClient(debug=True)

        isConnected = await api.Connect(autoplay=True)

        if not isConnected:
            return
        
        #api.ToggleEditorPause()

        await api.Wait(1000)

        
        collision = await api.RegisterCollisionMonitor("//*[@name='Player']")
        
        if collision:
            print(collision)

            event = await api.WaitForCollisionEvent(collision)
            print(event)

        await api.Wait(5000)
        print("Unregistering")
        await api.UnregisterCollisionMonitor(collision)


        
        await api.Wait(5000)
        await api.Disconnect()

        await api.Wait(100)
        api.StopEditorPlay()

    async def test_objectdistance(self):
        api = ApiClient(debug=True)

        isConnected = await api.Connect(autoplay=True)

        if not isConnected:
            return

        await api.Wait(1000)

        distance = await api.GetObjectDistance("//*[@name='Player']", "//*[@name='Platform (1)']")
        if distance:
            print (distance)

        await api.Wait(5000)
        await api.Disconnect()

        await api.Wait(100)
        api.StopEditorPlay()

    async def test_fieldvalue(self):
        api = ApiClient(debug=True)

        isConnected = await api.Connect(autoplay=True)

        if not isConnected:
            return

        await api.Wait(1000)

        isSimulated1 = await api.GetObjectFieldValue(bool, "//Player[@name='Player']/fn:component('UnityEngine.Rigidbody2D')/@simulated")
        isSimulated2 = await api.GetObjectFieldValueByName("//Player[@name='Player']/fn:component('UnityEngine.Rigidbody2D')", "simulated")
        if isSimulated1 and isSimulated2:
            print(isSimulated1)
            print(isSimulated2)

        await api.Wait(5000)
        await api.Disconnect()

        await api.Wait(100)
        api.StopEditorPlay()

    async def test_getobjectpos(self):
        
        api = ApiClient(debug=True)

        isConnected = await api.Connect(autoplay=True)

        if not isConnected:
            return

        await api.Wait(1000)

        ## TEST

        pos = await api.GetObjectPosition("//*[@name='Player']")

        if pos:
            print(pos)

        ## /TEST

        await api.Wait(5000)
        await api.Disconnect()

        await api.Wait(100)
        api.StopEditorPlay()

    async def test_customtypes(self):

        from CustomTypes import CustomColor, Serializer
        
        api = ApiClient(debug=True, customSerializer=Serializer)

        isConnected = await api.Connect(autoplay=True)

        if not isConnected:
            return

        await api.Wait(1000)

        ## TEST

        await api.CallMethod("//*[@name='Player']/fn:component('TestScript')", "Log_Color", [CustomColor(1, 2, 3, 4)])

        ## /TEST

        await api.Wait(5000)
        await api.Disconnect()

        await api.Wait(100)
        api.StopEditorPlay()

if __name__ == '__main__':
    Game = TestFixture()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Game.test_customtypes())