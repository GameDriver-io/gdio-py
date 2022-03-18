# gdio-py
Python bindings for the GameDriver Client API

 - [Quick Start](#Quick-Start)
 - [Changelog](CHANGELOG.md)
 - [API Reference](docs/ApiClient_Reference.md)

## Quick Start

This module requires at least Python 3.7

You can install the latest release directly from the repository by typing the following into a command line:
```bash
pip install git+https://github.com/GameDriver-io/gdio-py.git
```

Here is an example of how you can use the API with the [pytest](https://docs.pytest.org/en/latest/getting-started.html) framework:
```py
import asyncio
import pytest

from gdio.api import ApiClient
from gdio.common.objects import *

# This fixture is run before every test that takes agent_connection as an argument
# scope='session' means every test will use the same connection
@pytest.fixture(scope="session")
async def agent_connection():
    # Create a new agent connection
    api = ApiClient()
    await api.Connect("localhost", 19734)

    # Give the connection instance to the test
    yield api

    # Close the connection when all tests are done
    await api.Disconnect()

@pytest.mark.asyncio
async def test_move(agent_connection):
    api = agent_connection

    # Save the current position of the player
    start_pos = await api.GetObjectPosition("//*[@name='Player']")

    # Move the player to the right
    await api.AxisPress(axisId="Horizontal", value=1.0, numberOfFrames=100)

    # Wait for the player to move before checking the new position
    await api.Wait(500)

    # Save the new position of the player
    end_pos = await api.GetObjectPosition("//*[@name='Player']")

    # Check that the player moved successfully
    assert start_pos != end_pos

@pytest.mark.asyncio
async def test_2(agent_connection):
    api = agent_connection
    # Test some more stuff
    ...
```
