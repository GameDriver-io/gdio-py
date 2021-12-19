# Still used as a fallback because logging doesnt work if pytest doesnt run to completion

from logging import debug
import os, asyncio
from gdio.api import ApiClient
from gdio.common.objects import *

class TestFixture:

    def __init__(self):
        pass

    async def test(self):
        api = ApiClient(debug=True)
        await api.Connect()

        await api.Wait(1000)
        gcd = api.GetConnectedGameDetails()
        print(gcd)

if __name__ == '__main__':
    Game = TestFixture()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Game.test())