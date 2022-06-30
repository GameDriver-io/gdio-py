import asyncio

from _gdio.ApiClient import verify_hpath

@verify_hpath([0, 1])
async def test_func(hierarchyPath, hpathb):
    pass

if __name__ == "__main__":
    asyncio.run(
        test_func("//*", "sadfsafdd")
    )