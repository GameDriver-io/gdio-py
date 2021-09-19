# ApiClient-py
 A Python implementation of the GameDriver Unity API

 - [Installation](#Installation)
 - [Changelog](CHANGELOG.md)

## Installation

Clone the repository and navigate into it using:
```sh
clone https://github.com/ethanavatar/gdio-py.git
cd gdio-py
```

Install the current directory in locally editable mode:
```sh
pip install -e .
```

Editable mode allows you to make changes to the source files without recompiling, so you should only need to run this once.

You can now import the module and its members via:
```py
# TEMP: Namespace structure will be changed in the future.
from gdio.ApiClient import ApiClient
from gdio.Objects import Objects

api = ApiClient()
...
```
