# Changelog

## Upcoming
 - Fixing slight differences between this and the original API so that tests can be run in either version without changing timings
 - Custom types as arguments to `ApiClient.CallMethod` and `ApiClient.CallMethod_Void`

# 12-10-2021

### Added
 - Added support for built-in types as arguments in `ApiClient.CallMethod` and `ApiClient.CallMethod_Void`.
 - Added unity editor autoplay support.

### Changed
 - Made minor style changes to the [API reference](docs/ApiClient.md)

# 12-5-2021

### Added
 - Added an [API reference page for `ApiClient`](docs/ApiClient_Reference.md)
   - This uses a generation script that depends on [docsgen-py](https://github.com/ethanavatar/docsgen-py). but it would be useful to port this over to `pdoc](https://pdoc3.github.io/pdoc/) in the future.

### Changed
 - Changed many of the docstrings to be more accurately decriptive.
   - This is being done actively because GitHub Copilot wrote them initially, and they were mostly wrong.

# 11-12-2021
This version made progress on the rest of the client methods. Aside from around 15 of them, their functionality should be mostly complete. However, I have yet to test most of them. It also restuctures the oackage to be less cluttered; at least for the end user

### Added:
 - Added the following methods to `ApiClient`. Their functionality is not guaranteed.
   - `CallMethod` (no argument support)
   - `CallMethod_Void` (no argument support)
   - `ClickObject`
   - `ClickObjectEx`
   - `DoubleClick`
   - `DoubleClickEx`
   - `DoubleClickObject`
   - `DoubleClickObjectEx`
   - `GetLastFPS`
   - `GetObjectPosition`
   - `KeyPress`
   - `LoadScene`
   - `MouseDrag`
   - `MouseMoveToObject`
   - `MouseMoveToPoint`
   - `NavAgentMoveToPoint`
   - `Raycast`
   - `RegisterCollisionMonitor`
   - `RotateObject_Quaternion`
   - `RotateObject_Euler`
   - `RotateObject_AxisAngle`
   - `SetInputFieldText`
   - Any new methods that werent mentioned here have also been added, but will throw a `NotImplementedError` when called.
 - Logging via the standard library.
   - Added an optional `debug` parameter to the `ApiClient` constructor that will enable debug level logging in both stdout and a file in the `logs` directory.
 - Added docstrings to all methods in `ApiClient`.

### Changed
 - Changed the namespacing of the whole package to be closer to that of the original API.
   - Everything is now moved into a sub-package called `_gdio`
   - Another sub-package called `gdio` re-exports the public API in a much cleaner format.
      - This way, all that is visible to the end user are the things that they will actually use.

### Removed
 - Removed the `Exceptions` module.
   - I couldnt think of a way to use it meaningfully.
   - Everything now throws standard exceptions with different messages. Essentially what the module was doing anyway.


# 9-27-2021
This version reworked how messages are packed and unpacked. It also introduces a bug surrounding `ApiClient.WaitForEmptyInput()` where the method will just time out if the EmptyInput arrives before the method call. Otherwise, I'm happy with the overall structure for now. Next version will probably be focused on unit testing using PyTest; that way I can prove functionality across different platforms.

### Added:
 - `ApiClient.WaitForEmptyInput()` that waits until an EmptyInput Event is received.
 - Custom serializers in the [`Serializers.py`](src/gdio/Serializers.py) file.
    - This handles the standard object representations of message objects like `toDict()` and `toList()` used to by invoking the object's`.pack()` method.
    - This is also important to have when I eventually get to implementing arguments in `ApiClient.CallMethod()`
 - [`Events.py`](src/gdio/Events.py) to keep event message definitions.
 - `Message.GetName()` that returns a string representation of the class name.
    - Used in `Client.ProcessMessage()` in order to rebuild responses and do message-type-specific actions.
 - [`requirements_dev.txt`](requirements_dev.txt) holding packages useful to development but not to an end user.
    - Amended [`setup.cfg`](setup.cfg) appropriately.
    - Added [`py.typed`](src/gdio/py.typed) to comply with the [flake8](https://github.com/pycqa/flake8) style checker.
 

### Changed:
 - Moved message IDs outside the message class and into a dict *currently being stored in [`Requests.py`](src/gdio/Requests.py)*.
    - This allows for turning response messages back into message objects by looking up their stored ID.
 - Replaced the behavior of `toDict()` and `toList()` with `pack()` in both the `ProtocolMessage` and `Message` classes. 

### Removed:
 - `Objects.getGDIOMsgData()` that hasn't been used in a few versions because it was mostly used in patchwork functionality.

# 9-19-2021

### Changed:

 - Added a loop in `Client.GetResult()` to check for pending results and retry if there arent any.
    - This has seemingly fixed the main issues from last version... agent side errors strangely.

# 9-18-2021
This version fixed the problem with responses being received in the wrong order. It also has agent-side issues that I don't yet understand.

### Added:
 - Added `Client.GetResult()` which will return a command's response by looking up its RequestId.
 - Added `Client.ProcessMessage()` which will(eventually) convert a response into its appropriate GDIOMsg for it to be registered as an unhandled result in the `Client._results` collection.

### Changed:
 - Passed all response handling to `Client.ReadHandler()`
 - Due to asyncronous response reading, responses are now handled in accordance to their CorrelationId.
    - This also means message responses are no longer bound by the order they are received.

### Deprecated:
 - `Client.Receive()` is no longer referenced.
    - It might still be useful when using the module through a REPL, in which case it will be migrated outside [`Client.py`](src/gdio/Client.py).

# 9-15-2021
This version focused on breaking everything as little as possible whilst changing everything into a coroutine.

### Added:
 - [`CHANGELOG.md`](CHANGELOG.md)

### Changed:
 - Made all methods asyncio coroutines in preparation for the refactor around `Client.ReadHandler`.
    - This means the package no longer uses the [`socket`](https://docs.python.org/3/library/socket.html) module; instead, it uses [asyncio's streams layer'](https://docs.python.org/3/library/asyncio-stream.html) which provides higher level handling via [`StreamReader`](https://docs.python.org/3/library/asyncio-stream.html#asyncio.StreamReader) and [`StreamWriter`](https://docs.python.org/3/library/asyncio-stream.html#asyncio.StreamWriter) objects.
    - This also replaces the global [`socket.settimeout()`](https://docs.python.org/3/library/socket.html#socket.socket.settimeout) with the coroutine dependent [`asyncio.wait_for()`](https://docs.python.org/3/library/asyncio-task.html#timeouts).
 - Made [`TestScript.py`](TestScript.py) more "unit testy" because I got tired of routinely commenting out entire blocks.
 - Made the tests in [`TestScript.py`](TestScript.py) more realistic/practical in order to punish my bad implementation of response messages.
 - Moved the Latest Version Notes section of [`README.md`](README.md) to this file.
    - And replaced the anchor with a link to this file.

### Removed:
 - Removed `Client.Wait(requestInfo, timeout)`
    - Aside from timeout which has been moved elsewhere, It was essentially just a logger for only `RequestInfo` objects.

# 9-14-2021
In this version, every [`ApiClient`](src/gdio/ApiClient.py) method handles its own response blind to CorrelationID. It relies purely on receival order. As a result, calling a method before the previous one receives its response will mix up the receival order and break everything. I already wrote a POC for the proper way to do this using a ReadHandler loop as an async task, but I will first need to convert basically everything into coroutines.

There are skeletons of all the outward facing methods in [`ApiClient`](src/gdio/ApiClient.py), but most of them will throw a `NotImplementedError`. The same is true for the corresponding request and response objects.

The only currently functioning methods are:
```py
 - AxisPress()
 - ButtonPress()
 - CallMethod() # Barely
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
```
