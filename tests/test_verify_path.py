import asyncio
import pytest

from _gdio.ApiClient import verify_hpath

@pytest.mark.asyncio
async def test_verify_path():
    
    @verify_hpath(0)
    async def test_func(hierarchyPath):
        pass

    await test_func("/test/path")