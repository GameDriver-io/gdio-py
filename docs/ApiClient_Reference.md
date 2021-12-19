# `class` ApiClient

GameDriver.io Unity API Client class.

## Methods

| Method Name | Summary |
| ---- | ---- |
| [`AxisPress`](#AxisPress) -> `bool` |  Presses the target axis for the specified number of frames.  |
| [`ButtonPress`](#ButtonPress) -> `bool` |  Presses the target button for the specified number of frames.  |
| [`CallMethod`](#CallMethod) -> `bool` |  Calls a method on the target object.  |
| [`CallMethod_Void`](#CallMethod_Void) -> `bool` |  Calls a void method on the target object.  |
| [`CaptureScreenshot`](#CaptureScreenshot) -> `str` |  Captures a screenshot of the currently connected app.  |
| [`ClickEx_Vec2`](#ClickEx_Vec2) -> `bool` |  Clicks a mouse button at the target coordinates with modifier keys.  |
| [`ClickEx_XY`](#ClickEx_XY) -> `bool` |  Clicks a mouse button at the target coordinates with modifier keys.  |
| [`ClickObject`](#ClickObject) -> `bool` |  Clicks a mouse button at the position of the target object.  |
| [`ClickObjectEx`](#ClickObjectEx) -> `bool` |  Clicks a mouse button at the position of the target object with modifier keys.  |
| [`Click_Vec2`](#Click_Vec2) -> `bool` |  Clicks a mouse button at the target coordinates.  |
| [`Click_XY`](#Click_XY) -> `bool` |  Clicks a mouse button at the target coordinates.  |
| [`Connect`](#Connect) -> `bool` |  Connects to an agent at the target hostname and port.  |
| [`DisableHooks`](#DisableHooks) -> `bool` |  Disables the ability to preform the target input type from the ApiClient.  |
| [`DisableObjectCaching`](#DisableObjectCaching) -> `bool` |  Disables object caching for HierarchyPath resolution.  |
| [`Disconnect`](#Disconnect) -> `None` |  Disconnects from the agent.  |
| [`DoubleClickEx_Vec2`](#DoubleClickEx_Vec2) -> `bool` |  Clicks the mouse at the given coordinates.  |
| [`DoubleClickEx_XY`](#DoubleClickEx_XY) -> `bool` |  Clicks the mouse at the given coordinates.  |
| [`DoubleClickObject`](#DoubleClickObject) -> `bool` |  Clicks the mouse at the given coordinates.  |
| [`DoubleClickObjectEx`](#DoubleClickObjectEx) -> `bool` |  Clicks the mouse at the given coordinates.  |
| [`DoubleClick_Vec2`](#DoubleClick_Vec2) -> `bool` |  Clicks the mouse at the given coordinates.  |
| [`DoubleClick_XY`](#DoubleClick_XY) -> `bool` |  Clicks the mouse at the given coordinates.  |
| [`EnableHooks`](#EnableHooks) -> `bool` |  Enables the given hooking object.  |
| [`EnableObjectCaching`](#EnableObjectCaching) -> `bool` |  Enables object caching.  |
| [`FlushObjectLookupCache`](#FlushObjectLookupCache) -> `bool` |  Flushes the object lookup cache.  |
| [`GetConnectedGameDetails`](#GetConnectedGameDetails) -> `ProtocolObjects.GameConnectionDetails` |  Gets the details of the connected game.  |
| [`GetLastFPS`](#GetLastFPS) -> `float` |  Gets the last FPS value.  |
| [`GetNextCollisionEvent`](#GetNextCollisionEvent) -> `ProtocolObjects.Collision` |  (**Not Implemented**) Gets the next collision event.  |
| [`GetObjectDistance`](#GetObjectDistance) -> `float` |  (**Not Implemented**) Gets the distance between two objects.  |
| [`GetObjectFieldValue`](#GetObjectFieldValue) -> `t` |  (**Not Implemented**) Gets the value of a field on an object.  |
| [`GetObjectFieldValueByName`](#GetObjectFieldValueByName) -> `t` |  (**Not Implemented**) Gets the value of a field on an object.  |
| [`GetObjectList`](#GetObjectList) -> `bool` |  Gets the list of objects.  |
| [`GetObjectPosition`](#GetObjectPosition) -> `ProtocolObjects.Vector3` |  Gets the position of an object.  |
| [`GetSceneName`](#GetSceneName) -> `bool` |  Gets the name of the scene.  |
| [`GetVersionString`](#GetVersionString) -> `str` |  (**Not Implemented**) Gets the version string of the agent.  |
| [`KeyPress`](#KeyPress) -> `bool` |  Presses a key.  |
| [`Launch`](#Launch) -> `None` |  (**Not Implemented**) Launches a process.  |
| [`LoadScene`](#LoadScene) -> `bool` |  Loads a scene.  |
| [`MouseDrag`](#MouseDrag) -> `bool` |  Drags the mouse.  |
| [`MouseMoveToObject`](#MouseMoveToObject) -> `bool` |  Moves the mouse to an object.  |
| [`MouseMoveToPoint`](#MouseMoveToPoint) -> `bool` |  Moves the mouse to a point.  |
| [`NavAgentMoveToPoint`](#NavAgentMoveToPoint) -> `bool` |  Moves the nav agent to a point.  |
| [`Raycast`](#Raycast) -> `list` |  Performs a raycast.  |
| [`RegisterCollisionMonitor`](#RegisterCollisionMonitor) -> `bool` |  Registers a collision monitor.  |
| [`RotateObject_AxisAngle`](#RotateObject_AxisAngle) -> `bool` |  Rotates an object.  |
| [`RotateObject_Euler`](#RotateObject_Euler) -> `bool` |  Rotates an object.  |
| [`RotateObject_Quaternion`](#RotateObject_Quaternion) -> `bool` |  Rotates an object.  |
| [`SetInputFieldText`](#SetInputFieldText) -> `bool` |  Sets the text of an input field.  |
| [`SetObjectFieldValue`](#SetObjectFieldValue) -> `bool` |  (**Not Implemented**) Sets the value of an object field.  |
| [`TapObject`](#TapObject) -> `bool` |  Taps an object.  |
| [`Tap_Vec2`](#Tap_Vec2) -> `bool` |  Taps an object.  |
| [`Tap_XY`](#Tap_XY) -> `bool` |  Taps an object.  |
| [`TerminateGame`](#TerminateGame) -> `bool` |  (**Not Implemented**) Terminates the game.  |
| [`ToggleEditorPause`](#ToggleEditorPause) -> `bool` |  (**Not Implemented**) Toggles the editor pause.  |
| [`ToggleEditorPlay`](#ToggleEditorPlay) -> `bool` |  (**Not Implemented**) Toggles the editor play.  |
| [`TouchInput`](#TouchInput) -> `bool` |  Touches an object.  |
| [`UnregisterCollisionMonitor`](#UnregisterCollisionMonitor) -> `bool` |  Unregisters a collision monitor.  |
| [`Wait`](#Wait) -> `None` |  Waits for a specified number of miliseconds.  |
| [`WaitForCollisionEvent`](#WaitForCollisionEvent) -> `ProtocolObjects.Collision` |  (**Not Implemented**) Waits for a collision event.  |
| [`WaitForEmptyInput`](#WaitForEmptyInput) -> `bool` |  Waits for an empty input event.  |
| [`waitForObject`](#waitForObject) -> `bool` |  (**Not Implemented**) Waits for an object.  |
| [`waitForObjectValue`](#waitForObjectValue) -> `bool` |  (**Not Implemented**) Waits for an object value.  |
### <a id='AxisPress'></a> AxisPress(axisId : `str`, value : `float`, numberOfFrames : `int`, timeout : `int`) -> `bool`

 Presses the target axis for the specified number of frames. 

#### Returns

 `True` if the command was sent successfully, `False` otherwise. 

#### Parameters

 - axisId : `str` -  The name of the target input axis as defined in the Unity Input Manager. 
 - value : `float` -  The value of change on the target axis from -1.0 to +1.0. 
 - numberOfFrames : `int` -  The number of frames to hold the input for. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()

 # Move the horizontal axis to the right for 100 frames.
 await api.AxisPress(axisId='Horizontal', value=1.0, numberOfFrames=100)
 ```
 ### <a id='ButtonPress'></a> ButtonPress(buttonId : `str`, numberOfFrames : `int`, timeout : `int`) -> `bool`

 Presses the target button for the specified number of frames. 

#### Returns

 `True` if the command was sent successfully, `False` otherwise. 

#### Parameters

 - buttonId : `str` -  The name of the target input button as defined in the Unity Input Manager. 
 - numberOfFrames : `int` -  The number of frames to hold the input for. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 # Press the Jump button for 100 frames.
 await api.ButtonPress(buttonId='Jump', numberOfFrames=100)
 ```
 ### <a id='CallMethod'></a> CallMethod(t : `type`, hierarchyPath : `str`, methodName : `str`, arguments : `list[any]`, timeout : `int`) -> `bool`

 Calls a method on the target object. 

#### Returns

 The return value of the target method of type `t`. 

#### Parameters

 - t : `type` -  The type of the return value. 
 - hierarchyPath : `str` -  The HierarchyPath for an object and the script attached to it. 
 - methodName : `str` -  The name of the method to call within the script. 
 - arguments : `list[any]` -  The list of arguments to pass into the method. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.CallMethod(t=int, hierarchyPath="//*[@name='Player']/fn:component('PlayerController')", methodName="Jump")
 ```
 ### <a id='CallMethod_Void'></a> CallMethod_Void(hierarchyPath : `str`, methodName : `str`, arguments : `list[any]`, timeout : `int`) -> `bool`

 Calls a void method on the target object. 

#### Returns

 `True` if the command was sent successfully, `False` otherwise. 

#### Parameters

 - hierarchyPath : `str` -  The HierarchyPath for an object and the script attached to it. 
 - methodName : `str` -  The name of the method to call within the script. 
 - arguments : `list[any]` -  The list of arguments to pass into the method. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()

 # Call the `Jump` method on the `Player` object at the scene root.
 await api.CallMethod("//*[@name='Player']/fn:component('PlayerController')", "Jump")
 ```
 ### <a id='CaptureScreenshot'></a> CaptureScreenshot(filename : `str`, storeInGameFolder : `bool`, overwriteExisting : `bool`, timeout : `int`) -> `str`

 Captures a screenshot of the currently connected app. 

#### Returns

 The path and filename of the screen capture. 

#### Parameters

 - filename : `str` -  The path and filename of the screen capture. 
 - storeInGameFolder : `bool` -  (**Not Implemented**) Save the screenshot on the device the game is running on rather than returning it to the client. 
 - overwriteExisting : `bool` -  Overwrite if the file already exists. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.CaptureScreenshot(filename='/path/to/file')
 ```
 ### <a id='ClickEx_Vec2'></a> ClickEx_Vec2(buttonId : `MouseButtons`, position : `ProtocolObjects.Vector2`, clickFrameCount : `int`, keys : `list[KeyCode]`, keysNumberOfFrames : `int`, modifiers : `list[KeyCode]`, modifiersNumberOfFrames : `int`, delayAfterModifiersMsec : `int`, timeout : `int`) -> `bool`

 Clicks a mouse button at the target coordinates with modifier keys. 

#### Returns

 `True` if the command was sent successfully, `False` otherwise. 

#### Parameters

 - buttonId : `MouseButtons` -  The button to click. 
 - position : `ProtocolObjects.Vector2` -  The position in screen coordinates at which to click. 
 - clickFrameCount : `int` -  The number of frames to click for. 
 - keys : `list[KeyCode]` -  The list of keys to press while clicking. 
 - keysNumberOfFrames : `int` -  The number of frames to hold the keys for. 
 - modifiers : `list[KeyCode]` -  The list of modifier keys to press while clicking. 
 - modifiersNumberOfFrames : `int` -  The number of frames to hold the modifier keys for. 
 - delayAfterModifiersMsec : `int` -  The number of milliseconds to wait after pressing the modifiers before clicking the keys. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 # Shift+Left click the screen at (100, 100) for 5 frames.
 await api.ClickEx_XY(buttonId=MouseButtons.Left, position=(100, 100), clickFrameCount=5, keys=[KeyCode.LShift], keysNumberOfFrames=5)
 ```
 ### <a id='ClickEx_XY'></a> ClickEx_XY(buttonId : `MouseButtons`, x : `float`, y : `float`, clickFrameCount : `int`, keys : `list[KeyCode]`, keysNumberOfFrames : `int`, modifiers : `list[KeyCode]`, modifiersNumberOfFrames : `int`, delayAfterModifiersMsec : `int`, timeout : `int`) -> `bool`

 Clicks a mouse button at the target coordinates with modifier keys. 

#### Returns

 `True` if the command was sent successfully, `False` otherwise. 

#### Parameters

 - buttonId : `MouseButtons` -  The button to click. 
 - x : `float` -  The x position in screen coordinates at which to click. 
 - y : `float` -  The y position in screen coordinates at which to click. 
 - clickFrameCount : `int` -  The number of frames to click for. 
 - keys : `list[KeyCode]` -  The list of keys to press while clicking. 
 - keysNumberOfFrames : `int` -  The number of frames to hold the keys for. 
 - modifiers : `list[KeyCode]` -  The list of modifier keys to press while clicking. 
 - modifiersNumberOfFrames : `int` -  The number of frames to hold the modifier keys for. 
 - delayAfterModifiersMsec : `int` -  The number of milliseconds to wait after pressing the modifiers before clicking the keys. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 # Shift+Left click the screen at (100, 100) for 5 frames.
 await api.ClickEx_XY(buttonId=MouseButtons.Left, x=100, y=100, clickFrameCount=5, keys=[KeyCode.LShift], keysNumberOfFrames=5)
 ```
 ### <a id='ClickObject'></a> ClickObject(buttonId : `MouseButtons`, hierarchyPath : `str`, frameCount : `int`, cameraHierarchyPath : `str`, timeout : `int`) -> `bool`

 Clicks a mouse button at the position of the target object. 

#### Returns

 `True` if the command was sent successfully, `False` otherwise. 

#### Parameters

 - buttonId : `MouseButtons` -  The button to click. 
 - hierarchyPath : `str` -  The hierarchy path of the object to click. 
 - frameCount : `int` -  The number of frames to click for. 
 - cameraHierarchyPath : `str` -  The hierarchy path of the camera to use to find the object. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 # Left click the screen at the position of the `Player` object for 5 frames.
 await api.ClickObject(buttonId=MouseButtons.Left, hierarchyPath="//*[@name='Player']", frameCount=5)
 ```
 ### <a id='ClickObjectEx'></a> ClickObjectEx(buttonId : `MouseButtons`, hierarchyPath : `str`, frameCount : `int`, cameraHierarchyPath : `str`, keys : `list`, keysNumberOfFrames : `int`, modifiers : `list`, modifiersNumberOfFrames : `int`, delayAfterModifiersMsec : `int`, timeout : `int`) -> `bool`

 Clicks a mouse button at the position of the target object with modifier keys. 

#### Returns

 True if the command was sent successfully, False otherwise. 

#### Parameters

 - buttonId : `MouseButtons` -  The button to click. 
 - hierarchyPath : `str` -  The hierarchy path of the object to click. 
 - frameCount : `int` -  The number of frames to click for. 
 - cameraHierarchyPath : `str` -  The hierarchy path of the camera to use to find the object. 
 - keys : `list` -  The keys to press. 
 - keysNumberOfFrames : `int` -  The number of frames to hold the keys for. 
 - modifiers : `list` -  The modifiers to press. 
 - modifiersNumberOfFrames : `int` -  The number of frames to hold the modifiers for. 
 - delayAfterModifiersMsec : `int` -  The number of milliseconds to wait after pressing the modifiers. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 # Shift+Left click the screen at the position of the `Player` object for 5 frames.
 await api.ClickObjectEx(buttonId=MouseButtons.Left, hierarchyPath="//*[@name='Player']", frameCount=5, keys=[KeyCode.LShift], keysNumberOfFrames=5)
 ```
 ### <a id='Click_Vec2'></a> Click_Vec2(buttonId : `MouseButtons`, position : `ProtocolObjects.Vector2`, clickFrameCount : `int`, timeout : `int`) -> `bool`

 Clicks a mouse button at the target coordinates. 

#### Returns

 `True` if the command was sent successfully, `False` otherwise. 

#### Parameters

 - buttonId : `MouseButtons` -  The button to click. 
 - position : `ProtocolObjects.Vector2` -  The position in screen coordinates at which to click. 
 - clickFrameCount : `int` -  The number of frames to click for. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 # Left click the screen at (100, 100) for 5 frames.
 await api.Click_XY(ButtonId=MouseButtons.Left, position=(100, 100), clickFrameCount=5)
 ```
 ### <a id='Click_XY'></a> Click_XY(buttonId : `MouseButtons`, x : `float`, y : `float`, clickFrameCount : `int`, timeout : `int`) -> `bool`

 Clicks a mouse button at the target coordinates. 

#### Returns

 `True` if the command was sent successfully, `False` otherwise. 

#### Parameters

 - buttonId : `MouseButtons` -  The button to click. 
 - x : `float` -  The x position in screen coordinates at which to click. 
 - y : `float` -  The y position in screen coordinates at which to click. 
 - clickFrameCount : `int` -  The number of frames to click for. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 # Left click the screen at (100, 100) for 5 frames.
 await api.Click_XY(ButtonId=MouseButtons.Left, x=100, y=100, clickFrameCount=5)
 ```
 ### <a id='Connect'></a> Connect(hostname : `str`, port : `int`, autoplay : `bool`, timeout : `int`, autoPortResolution : `bool`) -> `bool`

 Connects to an agent at the target hostname and port. 

#### Returns

 True if nothing went wrong while trying to connect; None otherwise 

#### Parameters

 - hostname : `str` -  The hostname of the device running the target game. 
 - port : `int` -  The port that the target Gamedriver agent is configured to use. 
 - autoplay : `bool` -  (**Not Implemented**) Start the game automatically within the Unity Editor. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 
 - autoPortResolution : `bool` -  (**Not Implemented**) Automatically resolve the port a Gamedriver Agent is running on. 



#### Example


 ```python
 api = ApiClient()
 if await api.Connect(hostname='localhost', port=19734):
 print("Connected!")
 ```
 ### <a id='DisableHooks'></a> DisableHooks(HookingObject : `str`, timeout : `int`) -> `bool`

 Disables the ability to preform the target input type from the ApiClient. 

#### Returns

 True if the command was sent successfully, False otherwise. 

#### Parameters

 - HookingObject : `str` -  The input type to disable. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 # Disable Keyboard, Mouse, Touch and Controller hooks globally.
 await api.DisableHooks(hookingObject=HookingObject.All)
 ```
 ### <a id='DisableObjectCaching'></a> DisableObjectCaching(timeout : `int`) -> `bool`

 Disables object caching for HierarchyPath resolution. 

#### Returns

 `True` if the command was sent successfully, `False` otherwise. 

#### Parameters

 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.DisableObjectCaching()
 ```
 ### <a id='Disconnect'></a> Disconnect() -> `None`

 Disconnects from the agent. 

#### Returns

 None. 

#### Parameters




#### Example


 ```python
 api = ApiClient()
 await api.Connect()

 await api.Disconnect()
 ```
 ### <a id='DoubleClickEx_Vec2'></a> DoubleClickEx_Vec2(buttonId : `MouseButtons`, position : `ProtocolObjects.Vector2`, clickFrameCount : `int`, keys : `list`, keysNumberOfFrames : `int`, modifiers : `list`, modifiersNumberOfFrames : `int`, delayAfterModifiersMsec : `int`, timeout : `int`) -> `bool`

 Clicks the mouse at the given coordinates. 

#### Returns

 True if the command was sent successfully, False otherwise. 

#### Parameters

 - buttonId : `MouseButtons` -  The button to click. 
 - position : `ProtocolObjects.Vector2` -  The position to click at. 
 - clickFrameCount : `int` -  The number of frames to click. 
 - keys : `list` -  The list of keys to press. 
 - keysNumberOfFrames : `int` -  The number of frames to press the keys. 
 - modifiers : `list` -  The list of modifiers to press. 
 - modifiersNumberOfFrames : `int` -  The number of frames to press the modifiers. 
 - delayAfterModifiersMsec : `int` -  The number of milliseconds to wait after pressing the modifiers. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.DoubleClickEx_Vec2(MouseButtons.LEFT, ProtocolObjects.Vector2(500, 500), 5, [KeyCode.SHIFT, KeyCode.CONTROL], 5, [KeyCode.SHIFT, KeyCode.CONTROL], 3, 500)
 ```
 ### <a id='DoubleClickEx_XY'></a> DoubleClickEx_XY(buttonId : `MouseButtons`, x : `float`, y : `float`, clickFrameCount : `int`, keys : `list`, keysNumberOfFrames : `int`, modifiers : `list`, modifiersNumberOfFrames : `int`, delayAfterModifiersMsec : `int`, timeout : `int`) -> `bool`

 Clicks the mouse at the given coordinates. 

#### Returns

 True if the command was sent successfully, False otherwise. 

#### Parameters

 - buttonId : `MouseButtons` -  The button to click. 
 - x : `float` -  The x position to click at. 
 - y : `float` -  The y position to click at. 
 - clickFrameCount : `int` -  The number of frames to click. 
 - keys : `list` -  The list of keys to press. 
 - keysNumberOfFrames : `int` -  The number of frames to press the keys. 
 - modifiers : `list` -  The list of modifiers to press. 
 - modifiersNumberOfFrames : `int` -  The number of frames to press the modifiers. 
 - delayAfterModifiersMsec : `int` -  The number of milliseconds to wait after pressing the modifiers. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.DoubleClickEx_XY(MouseButtons.LEFT, 500, 500, 5, [KeyCode.SHIFT, KeyCode.CONTROL], 5, [KeyCode.SHIFT, KeyCode.CONTROL], 3, 500)
 ```
 ### <a id='DoubleClickObject'></a> DoubleClickObject(buttonId : `MouseButtons`, hierarchyPath : `str`, frameCount : `int`, timeout : `int`) -> `bool`

 Clicks the mouse at the given coordinates. 

#### Returns

 True if the command was sent successfully, False otherwise. 

#### Parameters

 - buttonId : `MouseButtons` -  The button to click. 
 - hierarchyPath : `str` -  The hierarchy path of the object to click. 
 - frameCount : `int` -  The number of frames to click. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.DoubleClickObject(MouseButtons.LEFT, "HierarchyPath", 5)
 ```
 ### <a id='DoubleClickObjectEx'></a> DoubleClickObjectEx(buttonId : `MouseButtons`, hierarchyPath : `str`, clickFrameCount : `int`, keys : `list`, keysNumberOfFrames : `int`, modifiers : `list`, modifiersNumberOfFrames : `int`, delayAfterModifiersMsec : `int`, timeout : `int`) -> `bool`

 Clicks the mouse at the given coordinates. 

#### Returns

 True if the command was sent successfully, False otherwise. 

#### Parameters

 - buttonId : `MouseButtons` -  The button to click. 
 - hierarchyPath : `str` -  The hierarchy path of the object to click. 
 - clickFrameCount : `int` -  The number of frames to click. 
 - keys : `list` -  The list of keys to press. 
 - keysNumberOfFrames : `int` -  The number of frames to press the keys. 
 - modifiers : `list` -  The list of modifiers to press. 
 - modifiersNumberOfFrames : `int` -  The number of frames to press the modifiers. 
 - delayAfterModifiersMsec : `int` -  The number of milliseconds to wait after pressing the modifiers. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.DoubleClickObjectEx(MouseButtons.LEFT, "HierarchyPath", 5, [KeyCode.SHIFT, KeyCode.CONTROL], 5, [KeyCode.SHIFT, KeyCode.CONTROL], 3, 500)
 ```
 ### <a id='DoubleClick_Vec2'></a> DoubleClick_Vec2(buttonId : `MouseButtons`, position : `ProtocolObjects.Vector2`, clickFrameCount : `int`, timeout : `int`) -> `bool`

 Clicks the mouse at the given coordinates. 

#### Returns

 True if the command was sent successfully, False otherwise. 

#### Parameters

 - buttonId : `MouseButtons` -  The button to click. 
 - position : `ProtocolObjects.Vector2` -  The position to click at. 
 - clickFrameCount : `int` -  The number of frames to click. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.DoubleClick_Vec2(MouseButtons.LEFT, ProtocolObjects.Vector2(500, 500), 5)
 ```
 ### <a id='DoubleClick_XY'></a> DoubleClick_XY(buttonId : `MouseButtons`, x : `float`, y : `float`, clickFrameCount : `int`, timeout : `int`) -> `bool`

 Clicks the mouse at the given coordinates. 

#### Returns

 `True` if the command was sent successfully, `False` otherwise. 

#### Parameters

 - buttonId : `MouseButtons` -  The button to click. 
 - x : `float` -  The x position to click at. 
 - y : `float` -  The y position to click at. 
 - clickFrameCount : `int` -  The number of frames to click. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.DoubleClick_XY(MouseButtons.LEFT, 500, 500, 5)
 ```
 ### <a id='EnableHooks'></a> EnableHooks(hookingObject : `HookingObject`, timeout : `int`) -> `bool`

 Enables the given hooking object. 

#### Returns

 True if the command was sent successfully, False otherwise. 

#### Parameters

 - hookingObject : `HookingObject` -  The hooking object to enable. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.EnableHooks(HookingObject.MOUSE)
 ```
 ### <a id='EnableObjectCaching'></a> EnableObjectCaching(timeout : `int`) -> `bool`

 Enables object caching. 

#### Returns

 True if the command was sent successfully, False otherwise. 

#### Parameters

 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.EnableObjectCaching()
 ```
 ### <a id='FlushObjectLookupCache'></a> FlushObjectLookupCache(timeout : `int`) -> `bool`

 Flushes the object lookup cache. 

#### Returns

 True if the command was sent successfully, False otherwise. 

#### Parameters

 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.FlushObjectLookupCache()
 ```
 ### <a id='GetConnectedGameDetails'></a> GetConnectedGameDetails() -> `ProtocolObjects.GameConnectionDetails`

 Gets the details of the connected game. 

#### Returns

 The details of the connected game. 

#### Parameters




#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 details = await api.GetConnectedGameDetails()
 print(details.GameName)
 ```
 ### <a id='GetLastFPS'></a> GetLastFPS(timeout : `int`) -> `float`

 Gets the last FPS value. 

#### Returns

 The last FPS value. 

#### Parameters

 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 fps = await api.GetLastFPS()
 print(fps)
 ```
 ### <a id='GetNextCollisionEvent'></a> GetNextCollisionEvent() -> `ProtocolObjects.Collision`

 (**Not Implemented**) Gets the next collision event. 

#### Returns

 The next collision event. 

#### Parameters




#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 collision = await api.GetNextCollisionEvent()
 print(collision.ObjectA.Name)
 ```
 ### <a id='GetObjectDistance'></a> GetObjectDistance(objectA_HierarchyPath : `str`, objectB_HierarchyPath : `str`, timeout : `int`) -> `float`

 (**Not Implemented**) Gets the distance between two objects. 

#### Returns

 The distance between the objects. 

#### Parameters

 - objectA_HierarchyPath : `str` -  The hierarchy path of the first object. 
 - objectB_HierarchyPath : `str` -  The hierarchy path of the second object. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 distance = await api.GetObjectDistance('ObjectA', 'ObjectB')
 print(distance)
 ```
 ### <a id='GetObjectFieldValue'></a> GetObjectFieldValue(t : `type`, hierarchyPath : `str`, timeout : `int`) -> `t`

 (**Not Implemented**) Gets the value of a field on an object. 

#### Returns

 The value of the field. 

#### Parameters

 - t : `type` -  The type of the field. 
 - hierarchyPath : `str` -  The hierarchy path of the object. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 value = await api.GetObjectFieldValue(type(int), 'ObjectA')
 print(value)
 ```
 ### <a id='GetObjectFieldValueByName'></a> GetObjectFieldValueByName(hierarchyPath : `str`, fieldName : `str`, timeout : `int`) -> `t`

 (**Not Implemented**) Gets the value of a field on an object. 

#### Returns

 The value of the field. 

#### Parameters

 - hierarchyPath : `str` -  The hierarchy path of the object. 
 - fieldName : `str` -  The name of the field. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 value = await api.GetObjectFieldValueByName('ObjectA', 'Position')
 print(value)
 ```
 ### <a id='GetObjectList'></a> GetObjectList(timeout : `int`) -> `bool`

 Gets the list of objects. 

#### Returns

 True if successful, false otherwise. 

#### Parameters

 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 objects = await api.GetObjectList()
 print(objects)
 ```
 ### <a id='GetObjectPosition'></a> GetObjectPosition(hierarchyPath : `str`, coordSpace : `CoordinateConversion`, cameraHierarchyPath : `str`, timeout : `int`) -> `ProtocolObjects.Vector3`

 Gets the position of an object. 

#### Returns

 The position of the object. 

#### Parameters

 - hierarchyPath : `str` -  The hierarchy path of the object. 
 - coordSpace : `CoordinateConversion` -  The coordinate space to use. 
 - cameraHierarchyPath : `str` -  The hierarchy path of the camera to use. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 position = await api.GetObjectPosition('ObjectA')
 print(position)
 ```
 ### <a id='GetSceneName'></a> GetSceneName(timeout : `int`) -> `bool`

 Gets the name of the scene. 

#### Returns

 True if successful, false otherwise. 

#### Parameters

 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 sceneName = await api.GetSceneName()
 print(sceneName)
 ```
 ### <a id='GetVersionString'></a> GetVersionString() -> `str`

 (**Not Implemented**) Gets the version string of the agent. 

#### Returns

 The version string of the agent. 

#### Parameters




#### Example


 ```python
 api = ApiClient()
 print(api.GetVersionString())
 ```
 ### <a id='KeyPress'></a> KeyPress(keys : `list`, numberOfFrames : `int`, modifiers : `list`, modifiersNumberOfFrames : `int`, delayAfterModifiersMsec : `int`, timeout : `int`) -> `bool`

 Presses a key. 

#### Returns

 True if successful, false otherwise. 

#### Parameters

 - keys : `list` -  The keys to press. 
 - numberOfFrames : `int` -  The number of frames to press the keys. 
 - modifiers : `list` -  The modifiers to press. 
 - modifiersNumberOfFrames : `int` -  The number of frames to press the modifiers. 
 - delayAfterModifiersMsec : `int` -  The delay after pressing the modifiers. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.KeyPress(['A', 'B'], 10)
 ```
 ### <a id='Launch'></a> Launch(filename : `str`, arguments : `str`) -> `None`

 (**Not Implemented**) Launches a process. 

#### Returns



#### Parameters

 - filename : `str` -  The filename of the process to launch. 
 - arguments : `str` -  The arguments to launch the process with. 



#### Example


 ```python
 # TODO
 ```
 ### <a id='LoadScene'></a> LoadScene(sceneName : `str`, timeout : `int`) -> `bool`

 Loads a scene. 

#### Returns

 True if successful, false otherwise. 

#### Parameters

 - sceneName : `str` -  The name of the scene to load. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.LoadScene('SceneA')
 ```
 ### <a id='MouseDrag'></a> MouseDrag(button : `MouseButtons`, dx : `float`, dy : `float`, frameCount : `float`, ox : `float`, oy : `float`, waitForEmptyInput : `bool`, timeout : `int`) -> `bool`

 Drags the mouse. 

#### Returns

 True if successful, false otherwise. 

#### Parameters

 - button : `MouseButtons` -  The button to drag with. 
 - dx : `float` -  The amount to drag the mouse in the X direction. 
 - dy : `float` -  The amount to drag the mouse in the Y direction. 
 - frameCount : `float` -  The number of frames to drag the mouse. 
 - ox : `float` -  The offset X of the mouse. 
 - oy : `float` -  The offset Y of the mouse. 
 - waitForEmptyInput : `bool` -  Whether or not to wait for the mouse to be empty before continuing. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.MouseDrag(MouseButtons.Left, 10, 10, 10)
 ```
 ### <a id='MouseMoveToObject'></a> MouseMoveToObject(objectHierarchyPath : `str`, frameCount : `float`, waitForObject : `bool`, waitForEmptyInput : `bool`, timeout : `int`) -> `bool`

 Moves the mouse to an object. 

#### Returns

 True if successful, false otherwise. 

#### Parameters

 - objectHierarchyPath : `str` -  The object hierarchy path of the object to move to. 
 - frameCount : `float` -  The number of frames to move the mouse. 
 - waitForObject : `bool` -  Whether or not to wait for the object to be found. 
 - waitForEmptyInput : `bool` -  Whether or not to wait for the mouse to be empty before continuing. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.MouseMoveToObject('/root/SceneA/UI/ButtonA', 10)
 ```
 ### <a id='MouseMoveToPoint'></a> MouseMoveToPoint(dx : `float`, dy : `float`, frameCount : `float`, ox : `float`, oy : `float`, waitForEmptyInput : `bool`, timeout : `int`) -> `bool`

 Moves the mouse to a point. 

#### Returns

 True if successful, false otherwise. 

#### Parameters

 - dx : `float` -  The amount to move the mouse in the X direction. 
 - dy : `float` -  The amount to move the mouse in the Y direction. 
 - frameCount : `float` -  The number of frames to move the mouse. 
 - ox : `float` -  The offset X of the mouse. 
 - oy : `float` -  The offset Y of the mouse. 
 - waitForEmptyInput : `bool` -  Whether or not to wait for the mouse to be empty before continuing. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.MouseMoveToPoint(10, 10, 10)
 ```
 ### <a id='NavAgentMoveToPoint'></a> NavAgentMoveToPoint(navAgent_HierarchyPath : `str`, dx : `float`, dy : `float`, waitForMoveToComplete : `bool`, timeout : `int`) -> `bool`

 Moves the nav agent to a point. 

#### Returns

 True if successful, false otherwise. 

#### Parameters

 - navAgent_HierarchyPath : `str` -  The object hierarchy path of the nav agent to move. 
 - dx : `float` -  The amount to move the nav agent in the X direction. 
 - dy : `float` -  The amount to move the nav agent in the Y direction. 
 - waitForMoveToComplete : `bool` -  Whether or not to wait for the nav agent to reach the destination. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.NavAgentMoveToPoint('/root/SceneA/NavAgentA', 10, 10)
 ```
 ### <a id='Raycast'></a> Raycast(raycastPoint : `ProtocolObjects.Vector3`, cameraHierarchyPath : `str`, timeout : `int`) -> `list`

 Performs a raycast. 

#### Returns

 The raycast results. 

#### Parameters

 - raycastPoint : `ProtocolObjects.Vector3` -  The raycast point. 
 - cameraHierarchyPath : `str` -  The hierarchy path of the camera to use for the raycast. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()

 raycastPoint = ProtocolObjects.Vector3(10, 10, 10)
 cameraHierarchyPath = '/root/SceneA/CameraA'
 raycastResults = await api.Raycast(raycastPoint, cameraHierarchyPath)
 ```
 ### <a id='RegisterCollisionMonitor'></a> RegisterCollisionMonitor(HierarchyPath : `str`, timeout : `int`) -> `bool`

 Registers a collision monitor. 

#### Returns

 True if successful, false otherwise. 

#### Parameters

 - HierarchyPath : `str` -  The hierarchy path of the object to monitor. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.RegisterCollisionMonitor('/root/SceneA/ObjectA')
 ```
 ### <a id='RotateObject_AxisAngle'></a> RotateObject_AxisAngle(hierarchyPath : `str`, xAngle : `float`, yAngle : `float`, zAngle : `float`, relativeTo : `Space`, waitForObject : `bool`, timeout : `int`) -> `bool`

 Rotates an object. 

#### Returns

 True if successful, false otherwise. 

#### Parameters

 - hierarchyPath : `str` -  The hierarchy path of the object to rotate. 
 - xAngle : `float` -  The X angle to rotate the object by. 
 - yAngle : `float` -  The Y angle to rotate the object by. 
 - zAngle : `float` -  The Z angle to rotate the object by. 
 - relativeTo : `Space` -  The space to rotate the object in. 
 - waitForObject : `bool` -  Whether or not to wait for the object to rotate. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.RotateObject_AxisAngle('/root/SceneA/ObjectA', 1, 1, 1)
 ```
 ### <a id='RotateObject_Euler'></a> RotateObject_Euler(hierarchyPath : `str`, euler : `ProtocolObjects.Vector3`, relativeTo : `Space`, waitForObject : `bool`, timeout : `int`) -> `bool`

 Rotates an object. 

#### Returns

 True if successful, false otherwise. 

#### Parameters

 - hierarchyPath : `str` -  The hierarchy path of the object to rotate. 
 - euler : `ProtocolObjects.Vector3` -  The Euler angles to rotate the object by. 
 - relativeTo : `Space` -  The space to rotate the object in. 
 - waitForObject : `bool` -  Whether or not to wait for the object to rotate. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.RotateObject_Euler('/root/SceneA/ObjectA', ProtocolObjects.Vector3(1, 1, 1))
 ```
 ### <a id='RotateObject_Quaternion'></a> RotateObject_Quaternion(hierarchyPath : `str`, quaternion : `ProtocolObjects.Vector4`, waitForObject : `bool`, timeout : `int`) -> `bool`

 Rotates an object. 

#### Returns

 True if successful, false otherwise. 

#### Parameters

 - hierarchyPath : `str` -  The hierarchy path of the object to rotate. 
 - quaternion : `ProtocolObjects.Vector4` -  The quaternion to rotate the object by. 
 - waitForObject : `bool` -  Whether or not to wait for the object to rotate. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.RotateObject_Quaternion('/root/SceneA/ObjectA', ProtocolObjects.Vector4(1, 1, 1, 1))
 ```
 ### <a id='SetInputFieldText'></a> SetInputFieldText(hierarchyPath : `str`, text : `str`, waitForObject : `bool`, timeout : `int`) -> `bool`

 Sets the text of an input field. 

#### Returns

 True if successful, false otherwise. 

#### Parameters

 - hierarchyPath : `str` -  The hierarchy path of the input field. 
 - text : `str` -  The text to set the input field to. 
 - waitForObject : `bool` -  Whether or not to wait for the object to be set. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.SetInputFieldText('/root/SceneA/ObjectA', 'Hello World')
 ```
 ### <a id='SetObjectFieldValue'></a> SetObjectFieldValue() -> `bool`

 (**Not Implemented**) Sets the value of an object field. 

#### Returns

 True if successful, false otherwise. 

#### Parameters




#### Example

### <a id='TapObject'></a> TapObject(hierarchyPath : `str`, tapCount : `int`, frameCount : `int`, cameraHierarchyPath : `str`, timeout : `int`) -> `bool`

 Taps an object. 

#### Returns

 True if successful, false otherwise. 

#### Parameters

 - hierarchyPath : `str` -  The hierarchy path of the object to tap. 
 - tapCount : `int` -  The number of times to tap the object. 
 - frameCount : `int` -  The number of frames to tap the object. 
 - cameraHierarchyPath : `str` -  The hierarchy path of the camera to use when tapping. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.TapObject('/root/SceneA/ObjectA')
 ```
 ### <a id='Tap_Vec2'></a> Tap_Vec2(position : `ProtocolObjects.Vector2`, tapCount : `int`, frameCount : `int`, timeout : `int`) -> `bool`

 Taps an object. 

#### Returns

 True if successful, false otherwise. 

#### Parameters

 - position : `ProtocolObjects.Vector2` -  The position to tap. 
 - tapCount : `int` -  The number of times to tap the object. 
 - frameCount : `int` -  The number of frames to tap the object. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.Tap_Vec2(ProtocolObjects.Vector2(1, 1))
 ```
 ### <a id='Tap_XY'></a> Tap_XY(x : `float`, y : `float`, tapCount : `int`, frameCount : `int`, timeout : `int`) -> `bool`

 Taps an object. 

#### Returns

 True if successful, false otherwise. 

#### Parameters

 - x : `float` -  The X coordinate to tap. 
 - y : `float` -  The Y coordinate to tap. 
 - tapCount : `int` -  The number of times to tap the object. 
 - frameCount : `int` -  The number of frames to tap the object. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.Tap_XY(1, 1)
 ```
 ### <a id='TerminateGame'></a> TerminateGame() -> `bool`

 (**Not Implemented**) Terminates the game. 

#### Returns

 True if successful, false otherwise. 

#### Parameters




#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.TerminateGame()
 ```
 ### <a id='ToggleEditorPause'></a> ToggleEditorPause() -> `bool`

 (**Not Implemented**) Toggles the editor pause. 

#### Returns

 True if successful, false otherwise. 

#### Parameters




#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.ToggleEditorPause()
 ```
 ### <a id='ToggleEditorPlay'></a> ToggleEditorPlay() -> `bool`

 (**Not Implemented**) Toggles the editor play. 

#### Returns

 True if successful, false otherwise. 

#### Parameters




#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.ToggleEditorPlay()
 ```
 ### <a id='TouchInput'></a> TouchInput(x1 : `float`, y1 : `float`, x2 : `float`, y2 : `float`, fingerId : `int`, tapCount : `int`, frameCount : `int`, waitForEmptyInput : `bool`, radius : `float`, pressure : `float`, altitudeAngle : `float`, azmulthAngle : `float`, maximumPossiblePressure : `float`, timeout : `int`) -> `bool`

 Touches an object. 

#### Returns

 True if successful, false otherwise. 

#### Parameters

 - x1 : `float` -  The X coordinate of the first touch point. 
 - y1 : `float` -  The Y coordinate of the first touch point. 
 - x2 : `float` -  The X coordinate of the second touch point. 
 - y2 : `float` -  The Y coordinate of the second touch point. 
 - fingerId : `int` -  The finger ID. 
 - tapCount : `int` -  The number of times to tap the object. 
 - frameCount : `int` -  The number of frames to tap the object. 
 - waitForEmptyInput : `bool` -  Whether to wait for an empty input. 
 - radius : `float` -  The radius of the touch. 
 - pressure : `float` -  The pressure of the touch. 
 - altitudeAngle : `float` -  The altitude angle of the touch. 
 - azmulthAngle : `float` -  The azmulth angle of the touch. 
 - maximumPossiblePressure : `float` -  The maximum possible pressure of the touch. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.TouchInput(1, 1, 1, 1, 1)
 ```
 ### <a id='UnregisterCollisionMonitor'></a> UnregisterCollisionMonitor(hierarchyPath : `str`, timeout : `int`) -> `bool`

 Unregisters a collision monitor. 

#### Returns

 True if successful, false otherwise. 

#### Parameters

 - hierarchyPath : `str` -  The hierarchy path of the object to monitor. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.UnregisterCollisionMonitor('/root/SceneA/ObjectA')
 ```
 ### <a id='Wait'></a> Wait(miliseconds : `int`) -> `None`

 Waits for a specified number of miliseconds. 

#### Returns



#### Parameters

 - miliseconds : `int` -  The number of miliseconds to wait. 



#### Example


 ```python
 api = ApiClient()
 
 await api.Wait(1000)
 ```
 ### <a id='WaitForCollisionEvent'></a> WaitForCollisionEvent(eventId : `str`, timeout : `int`) -> `ProtocolObjects.Collision`

 (**Not Implemented**) Waits for a collision event. 

#### Returns

 The collision event message. 

#### Parameters

 - eventId : `str` -  The event ID. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.WaitForCollisionEvent('123')
 ```
 ### <a id='WaitForEmptyInput'></a> WaitForEmptyInput(timeout : `int`) -> `bool`

 Waits for an empty input event. 

#### Returns

 `True` if the event was recieved in time, `False` otherwise. 

#### Parameters

 - timeout : `int` -  The number of seconds to wait for the event to be processed 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.WaitForEmptyInput()
 ```
 ### <a id='waitForObject'></a> waitForObject(hierarchyPath : `str`, timeout : `int`) -> `bool`

 (**Not Implemented**) Waits for an object. 

#### Returns

 True if successful, false otherwise. 

#### Parameters

 - hierarchyPath : `str` -  The hierarchy path of the object to wait for. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.WaitForObject('/root/SceneA/ObjectA')
 ```
 ### <a id='waitForObjectValue'></a> waitForObjectValue(hierarchyPath : `str`, timeout : `int`) -> `bool`

 (**Not Implemented**) Waits for an object value. 

#### Returns

 True if successful, false otherwise. 

#### Parameters

 - hierarchyPath : `str` -  The hierarchy path of the object to wait for. 
 - timeout : `int` -  The number of seconds to wait for the command to be recieved by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.WaitForObjectValue('/root/SceneA/ObjectA')
 ```
 