# Changelog

## Upcoming

 - Pending

## 9-15-21

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
 - Clarified and amended previous version notes.

### Removed:
 - Removed `Client.Wait(requestInfo, timeout)`
    - Aside from timeout which has been moved elsewhere, It was essentially just a logger for only `RequestInfo` objects.

## 9-14-21
In this version, every `ApiClient` method handles its own response blind to `CorrelationID`. It relies purely on receival order. As a result, calling a method before the previous one receives its response will mix up the receival order and break everything. I already wrote a POC for the proper way to do this using a ReadHandler loop as an async task, but I will first need to convert basically everything into coroutines.



There are skeletons of all the outward facing methods in `ApiClient`, but most of them will throw a `NotImplementedError`. The same is true for the corresponding request and response objects.

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