# ApiClient-py
 A Python implementation of the GameDriver Unity API

 - [Installation](#Installation)
 - [Changelog](CHANGELOG.md)

## Installation

Install the latest version of the package directly from the repository using:
```sh
pip install https://github.com/ethanavatar/gdio-py.git
```

Alternatively, to make local changes without recompiling, you can clone the repository and install the package in editable (-e) mode.
```sh
clone https://github.com/ethanavatar/gdio-py.git
pip install -e gdio-py
```
This way, the module refers directly to the installed folder rather than the version in site-packages, and all changes made to the source are immediately usable.

After either one of the above steps, the module and its members can be imported and used.
```py
# NOTE: Namespace structure will be changed in the future.
from gdio.ApiClient import ApiClient
from gdio.Objects import Objects

api = ApiClient()
...
```
