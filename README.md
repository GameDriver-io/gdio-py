# gdio-py
Python bindings for the GameDriver Client API

 - [Quick Start](#Quick-Start)
 - [Changelog](CHANGELOG.md)
 - [API Reference](docs/ApiClient_Reference.md)

## Quick Start

Install the latest release directly from the repository by typing the following into a command line:
```bash
pip install git+https://github.com/GameDriver-io/gdio-py.git@latest
```

Here is an example of how you can use the API with the [pytest](https://docs.pytest.org/en/latest/getting-started.html) framework:
```py
import asyncio
import pytest

from gdio.api import ApiClient
from gdio.common.objects import *

@pytest.fixture(scope="session")
async def agent_connection():
    # Create a new agent connection
    api = ApiClient()
    await api.Connect('localhost', 19734)

    # Return the connection instance
    yield api

    # Close the connection when all tests are done
    await api.Disconnect()

@pytest.mark.asyncio
async def test_1(agent_connection):
    api = agent_connection
    # Test some stuff
    ...

@pytest.mark.asyncio
async def test_2(agent_connection):
    api = agent_connection
    # Test some more stuff
    ...
```
