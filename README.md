# ApiClient-py
 A Python implementation of the GameDriver Unity API

 - [Installation](#Installation)
 - [Latest Version Notes](#Latest-Version-Notes)

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

api = ApiClient.ApiClient()
...
```

## Latest Version Notes
### 9-14-21
The way I am handling responses in this version is blatantly wrong because I somehow overlooked the existence of `ReadHandler`. As a result calling a method before the previous one recieves it's respose will mix up the receival order and break everything. I am currently testing the fix for this. There are skeletons of all the outward facing methods in `ApiClient`, but most of them will throw a `NotImplementedError`.

The only currently functioning methods are:
 - AxisPress()
 - ButtonPress()
 - CallMethod() `Barely`
 - CaptureScreenshot()
 - Connect()
 - DisableHooks()
 - DisableObjectCaching()
 - Disconnect()
 - EnableHooks()
 - EnableObjectCaching()
 - FlushObjectLookupCache()
 - GetConnectedGameDetails()
 - GetObjectList()
 - GetSceneName()
 - Wait()
