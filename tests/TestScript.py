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

            event = api.GetNextCollisionEvent(collision)
            print(event)


        
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

        distance = await api.GetObjectFieldValue(float, "//Player[@name='Player']/fn:component('UnityEngine.Rigidbody2D')/@simulated")
        if distance:
            print (distance)

        await api.Wait(5000)
        await api.Disconnect()

        await api.Wait(100)
        api.StopEditorPlay()


if __name__ == '__main__':
    Game = TestFixture()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Game.test_fieldvalue())