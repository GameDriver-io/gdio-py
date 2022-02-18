# `class` ApiClient

GameDriver.io Unity API Client class.

## Methods

| Method Name | Summary |
| ---- | ---- |
| [`AxisPress`](#AxisPress) -> `bool` |  Send arbitrary axis states to the game. Defaults to LEFT ALT/CTRL/SHIFT/WINDOWS(COMMAND)  |
| [`ButtonPress`](#ButtonPress) -> `bool` |  Send arbitrary button states to the game. Defaults to LEFT ALT/CTRL/SHIFT/WINDOWS(COMMAND)  |
| [`CallMethod`](#CallMethod) -> `bool` |  Execute a method on an object  |
| [`CaptureScreenshot`](#CaptureScreenshot) -> `str` |  Capture a screenshot of the currently running game.  |
| [`ClickEx_Vec2`](#ClickEx_Vec2) -> `bool` |  Clicks a mouse button at the target coordinates along with keypresses.  |
| [`ClickEx_XY`](#ClickEx_XY) -> `bool` |  Clicks a mouse button at the target coordinates along with keypresses.  |
| [`ClickObject`](#ClickObject) -> `bool` |  Clicks a mouse button at the position of the target object.  |
| [`ClickObjectEx`](#ClickObjectEx) -> `bool` |  Clicks a mouse button at the position of the target object along with keypresses.  |
| [`Click_Vec2`](#Click_Vec2) -> `bool` |  Clicks a mouse button at the target coordinates.  |
| [`Click_XY`](#Click_XY) -> `bool` |  Clicks a mouse button at the target coordinates.  |
| [`Connect`](#Connect) -> `bool` |  Connects to an agent at the target hostname and port.  |
| [`DisableHooks`](#DisableHooks) -> `bool` |  Disables the ability to preform the target input type from the ApiClient.  |
| [`DisableObjectCaching`](#DisableObjectCaching) -> `bool` |  Disables object caching of objects for HierarchyPath resolution.  |
| [`Disconnect`](#Disconnect) -> `None` |  Disconnects from the agent.  |
| [`DoubleClickEx_Vec2`](#DoubleClickEx_Vec2) -> `bool` |  Double-clicks the mouse at the target coordinates.  |
| [`DoubleClickEx_XY`](#DoubleClickEx_XY) -> `bool` |  Double-clicks the mouse at the target coordinates.  |
| [`DoubleClickObject`](#DoubleClickObject) -> `bool` |  Double-clicks the mouse at the target coordinates.  |
| [`DoubleClickObjectEx`](#DoubleClickObjectEx) -> `bool` |  Double-clicks the mouse at the target coordinates.  |
| [`DoubleClick_Vec2`](#DoubleClick_Vec2) -> `bool` |  Double-clicks a mouse button at the target coordinates.  |
| [`DoubleClick_XY`](#DoubleClick_XY) -> `bool` |  Double-clicks a mouse button at the target coordinates.  |
| [`EnableHooks`](#EnableHooks) -> `bool` |  Enables the given hooking object.  |
| [`EnableObjectCaching`](#EnableObjectCaching) -> `bool` |  Enables caching of objects for hierarchyPath resolution.  |
| [`FlushObjectLookupCache`](#FlushObjectLookupCache) -> `bool` |  Flushes the object lookup cache.  |
| [`GetConnectedGameDetails`](#GetConnectedGameDetails) -> `ProtocolObjects.GameConnectionDetails` |  Gets the details of the connected game.  |
| [`GetLastFPS`](#GetLastFPS) -> `float` |  Gets the last reported FPS value.  |
| [`GetNextCollisionEvent`](#GetNextCollisionEvent) -> `ProtocolObjects.Collision` |  Gets the next collision event.  |
| [`GetObjectDistance`](#GetObjectDistance) -> `float` |  Gets the distance between two objects.  |
| [`GetObjectFieldValue`](#GetObjectFieldValue) -> `t` |  Gets the value of a field on an object.  |
| [`GetObjectFieldValueByName`](#GetObjectFieldValueByName) -> `t` |  Gets the value of a field on an object by field name.  |
| [`GetObjectList`](#GetObjectList) -> `bool` |  Gets the list of objects in the scene.  |
| [`GetObjectPosition`](#GetObjectPosition) -> `ProtocolObjects.Vector3` |  Gets the position of an object.  |
| [`GetSceneName`](#GetSceneName) -> `bool` |  Gets the name of the active scene.  |
| [`KeyPress`](#KeyPress) -> `bool` |  Presses a key.  |
| [`Launch`](#Launch) -> `bool` |  Launches an executable.  |
| [`LoadScene`](#LoadScene) -> `bool` |  Loads a scene by name.  |
| [`MouseDrag`](#MouseDrag) -> `bool` |  Drags the mouse.  |
| [`MouseMoveToObject`](#MouseMoveToObject) -> `bool` |  Moves the mouse to an object.  |
| [`MouseMoveToPoint`](#MouseMoveToPoint) -> `bool` |  Moves the mouse to an absolute point on screen.  |
| [`NavAgentMoveToPoint`](#NavAgentMoveToPoint) -> `bool` |  Moves the nav agent to a point.  |
| [`Raycast`](#Raycast) -> `list` |  Perform a Raycast to a point to find out what is in that position.  |
| [`RegisterCollisionMonitor`](#RegisterCollisionMonitor) -> `bool` |  Registers a collision monitor to recieve collision events on an object.  |
| [`RotateObject_AxisAngle`](#RotateObject_AxisAngle) -> `bool` |  Rotates an object using absolute axis angles.  |
| [`RotateObject_Euler`](#RotateObject_Euler) -> `bool` |  Rotates an object using euler angles.  |
| [`RotateObject_Quaternion`](#RotateObject_Quaternion) -> `bool` |  Rotates an object using a quaternion.  |
| [`SetInputFieldText`](#SetInputFieldText) -> `bool` |  Sets the text of an InputField or TMP_InputField.  |
| [`SetObjectFieldValue`](#SetObjectFieldValue) -> `bool` |  Set the field or property of an object.  |
| [`StopEditorPlay`](#StopEditorPlay) -> `None` |  Stops Play Mode in the Unity Editor.  |
| [`TapObject`](#TapObject) -> `bool` |  Tap the handheld device at the target position.  |
| [`Tap_Vec2`](#Tap_Vec2) -> `bool` |  Tap the handheld device at the target position.  |
| [`Tap_XY`](#Tap_XY) -> `bool` |  Tap the handheld device at the target position.  |
| [`TerminateGame`](#TerminateGame) -> `None` |  Terminates the game.  |
| [`ToggleEditorPause`](#ToggleEditorPause) -> `bool` |  Toggles Pause in the Unity Editor while Play Mode is active.  |
| [`ToggleEditorPlay`](#ToggleEditorPlay) -> `bool` |  Toggles Play Mode in the Unity Editor.  |
| [`TouchInput`](#TouchInput) -> `bool` |  Touches an object.  |
| [`UnregisterCollisionMonitor`](#UnregisterCollisionMonitor) -> `bool` |  Unregisters a collision monitor to stop recieving collision events on an object.  |
| [`Wait`](#Wait) -> `None` |  Waits for a specified number of miliseconds.  |
| [`WaitForCollisionEvent`](#WaitForCollisionEvent) -> `ProtocolObjects.Collision` |  Waits for a new collision event.  |
| [`WaitForEmptyInput`](#WaitForEmptyInput) -> `None` |  Waits for an empty input event.  |
| [`WaitForObject`](#WaitForObject) -> `bool` |  Waits for an object to exist.  |
| [`waitForObjectValue`](#waitForObjectValue) -> `bool` |  Wait for an object to exist and have a specific value for a specified field/property.  |
### <a id='AxisPress'></a> AxisPress(axisId : `str`, value : `float`, numberOfFrames : `int`, timeout : `int`) -> `bool`

 Send arbitrary axis states to the game. Defaults to LEFT ALT/CTRL/SHIFT/WINDOWS(COMMAND) 

#### Returns

 `True` if the command was sent successfully, `False` otherwise. 

#### Parameters

 - axisId : `str` -  The name of the target input axis as defined in the Unity Input Manager (Old). 
 - value : `float` -  The value of change on the target axis from -1.0 to +1.0. 
 - numberOfFrames : `int` -  The number of frames to hold the input for. 
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 # Move the horizontal axis to the right for 100 frames.
 await api.AxisPress(axisId='Horizontal', value=1.0, numberOfFrames=100)
 ```
 ### <a id='ButtonPress'></a> ButtonPress(buttonId : `str`, numberOfFrames : `int`, timeout : `int`) -> `bool`

 Send arbitrary button states to the game. Defaults to LEFT ALT/CTRL/SHIFT/WINDOWS(COMMAND) 

#### Returns

 `True` if the command was sent successfully, `False` otherwise. 

#### Parameters

 - buttonId : `str` -  The name of the target input button as defined in the Unity Input Manager (Old). 
 - numberOfFrames : `int` -  The number of frames to hold the input for. 
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 # Press the Jump button for 100 frames.
 await api.ButtonPress(buttonId='Jump', numberOfFrames=100)
 ```
 ### <a id='CallMethod'></a> CallMethod(hierarchyPath : `str`, methodName : `str`, arguments : `list[any]`, timeout : `int`) -> `bool`

 Execute a method on an object 

#### Returns

 The return value of the target method of type `t`. 

#### Parameters

 - hierarchyPath : `str` -  The HierarchyPath for a script attached to an object where the target method is defined. 
 - methodName : `str` -  The name of the method to call. 
 - arguments : `list[any]` -  The list of arguments to pass into the method. 
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 # Set the color of the `Player` object to red using its method `SetColor`.
 await api.CallMethod(hierarchyPath="//*[@name='Player']/fn:component('Box')", methodName="SetColor", arguments=[255, 0, 0])
 ```
 ### <a id='CaptureScreenshot'></a> CaptureScreenshot(filename : `str`, storeInGameFolder : `bool`, overwriteExisting : `bool`, timeout : `int`) -> `str`

 Capture a screenshot of the currently running game. 

#### Returns

 The path and filename of the screen capture. 

#### Parameters

 - filename : `str` -  The absolute path and filename of the screen capture. 
 - storeInGameFolder : `bool` -  Save the screenshot on the device the game is running on rather than returning it to the client. 
 - overwriteExisting : `bool` -  Overwrite if the file already exists. 
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 await api.CaptureScreenshot(filename='/path/to/file/screenshot.png')
 ```
 ### <a id='ClickEx_Vec2'></a> ClickEx_Vec2(buttonId : `MouseButtons`, position : `ProtocolObjects.Vector2`, clickFrameCount : `int`, keys : `list[KeyCode]`, keysNumberOfFrames : `int`, modifiers : `list[KeyCode]`, modifiersNumberOfFrames : `int`, delayAfterModifiersMsec : `int`, timeout : `int`) -> `bool`

 Clicks a mouse button at the target coordinates along with keypresses. 

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
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 # Shift+Left click the screen at (100, 100) for 5 frames.
 await api.ClickEx_XY(buttonId=MouseButtons.Left, position=(100, 100), clickFrameCount=5, keys=[KeyCode.LShift], keysNumberOfFrames=5)
 ```
 ### <a id='ClickEx_XY'></a> ClickEx_XY(buttonId : `MouseButtons`, x : `float`, y : `float`, clickFrameCount : `int`, keys : `list[KeyCode]`, keysNumberOfFrames : `int`, modifiers : `list[KeyCode]`, modifiersNumberOfFrames : `int`, delayAfterModifiersMsec : `int`, timeout : `int`) -> `bool`

 Clicks a mouse button at the target coordinates along with keypresses. 

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
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
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
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 # Left click the screen at the position of the `Player` object for 5 frames.
 await api.ClickObject(buttonId=MouseButtons.Left, hierarchyPath="//*[@name='Player']", frameCount=5)
 ```
 ### <a id='ClickObjectEx'></a> ClickObjectEx(buttonId : `MouseButtons`, hierarchyPath : `str`, frameCount : `int`, cameraHierarchyPath : `str`, keys : `list`, keysNumberOfFrames : `int`, modifiers : `list`, modifiersNumberOfFrames : `int`, delayAfterModifiersMsec : `int`, timeout : `int`) -> `bool`

 Clicks a mouse button at the position of the target object along with keypresses. 

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
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
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
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
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
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 # Left click the screen at (100, 100) for 5 frames.
 await api.Click_XY(ButtonId=MouseButtons.Left, x=100, y=100, clickFrameCount=5)
 ```
 ### <a id='Connect'></a> Connect(hostname : `str`, port : `int`, autoplay : `bool`, timeout : `int`) -> `bool`

 Connects to an agent at the target hostname and port. 

#### Returns

 True if nothing went wrong while trying to connect; None otherwise 

#### Parameters

 - hostname : `str` -  The hostname of the device running the target game. 
 - port : `int` -  The port that the target Gamedriver agent is configured to listen on. 
 - autoplay : `bool` -  Start the game automatically within the Unity Editor. 
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



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
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 
 # Disable Mouse Hooks
 await api.DisableHooks(HookingObject.MOUSE)

 # Disable Gamepad Hooks
 await api.DisableHooks(HookingObject.GAMEPAD)

 # or just disable everything at once
 await api.DisableHooks(HookingObject.ALL)
 ```
 ### <a id='DisableObjectCaching'></a> DisableObjectCaching(timeout : `int`) -> `bool`

 Disables object caching of objects for HierarchyPath resolution. 

#### Returns

 `True` if the command was sent successfully, `False` otherwise. 

#### Parameters

 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 await api.DisableObjectCaching()
 ```
 ### <a id='Disconnect'></a> Disconnect() -> `None`

 Disconnects from the agent. 

#### Returns

 None. 

#### Parameters




#### Example


 ```python
 await api.Disconnect()
 ```
 ### <a id='DoubleClickEx_Vec2'></a> DoubleClickEx_Vec2(buttonId : `MouseButtons`, position : `ProtocolObjects.Vector2`, clickFrameCount : `int`, keys : `list`, keysNumberOfFrames : `int`, modifiers : `list`, modifiersNumberOfFrames : `int`, delayAfterModifiersMsec : `int`, timeout : `int`) -> `bool`

 Double-clicks the mouse at the target coordinates. 

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
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 # Double-click the left mouse button at (500, 500) while pressing Shift and Control
 await api.DoubleClickEx_Vec2(MouseButtons.LEFT, ProtocolObjects.Vector2(500, 500), 5, [KeyCode.SHIFT, KeyCode.CONTROL], 5, [KeyCode.SHIFT, KeyCode.CONTROL], 5, 500)
 ```
 ### <a id='DoubleClickEx_XY'></a> DoubleClickEx_XY(buttonId : `MouseButtons`, x : `float`, y : `float`, clickFrameCount : `int`, keys : `list`, keysNumberOfFrames : `int`, modifiers : `list`, modifiersNumberOfFrames : `int`, delayAfterModifiersMsec : `int`, timeout : `int`) -> `bool`

 Double-clicks the mouse at the target coordinates. 

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
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 # Double-click the left mouse button at (500, 500) while pressing Shift and Control
 await api.DoubleClickEx_XY(MouseButtons.LEFT, 500, 500, 5, [KeyCode.SHIFT, KeyCode.CONTROL], 5, [KeyCode.SHIFT, KeyCode.CONTROL], 5, 500)
 ```
 ### <a id='DoubleClickObject'></a> DoubleClickObject(buttonId : `MouseButtons`, hierarchyPath : `str`, frameCount : `int`, timeout : `int`) -> `bool`

 Double-clicks the mouse at the target coordinates. 

#### Returns

 True if the command was sent successfully, False otherwise. 

#### Parameters

 - buttonId : `MouseButtons` -  The button to click. 
 - hierarchyPath : `str` -  The hierarchy path of the object to click. 
 - frameCount : `int` -  The number of frames to click. 
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 # Double-click the position of the `Player` object
 await api.DoubleClickObject(MouseButtons.LEFT, "//*[@name='Player']", 5)
 ```
 ### <a id='DoubleClickObjectEx'></a> DoubleClickObjectEx(buttonId : `MouseButtons`, hierarchyPath : `str`, clickFrameCount : `int`, keys : `list`, keysNumberOfFrames : `int`, modifiers : `list`, modifiersNumberOfFrames : `int`, delayAfterModifiersMsec : `int`, timeout : `int`) -> `bool`

 Double-clicks the mouse at the target coordinates. 

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
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 # Double-click the position of the `Player` object while pressing Shift and Control
 await api.DoubleClickObjectEx(MouseButtons.LEFT, "//*[@name='Player']", 5, [KeyCode.SHIFT, KeyCode.CONTROL], 5, [KeyCode.SHIFT, KeyCode.CONTROL], 5, 500)
 ```
 ### <a id='DoubleClick_Vec2'></a> DoubleClick_Vec2(buttonId : `MouseButtons`, position : `Vector2`, clickFrameCount : `int`, timeout : `int`) -> `bool`

 Double-clicks a mouse button at the target coordinates. 

#### Returns

 `True` if the command was sent successfully, `False` otherwise. 

#### Parameters

 - buttonId : `MouseButtons` -  The button to click. 
 - position : `Vector2` -  The position to click at. 
 - clickFrameCount : `int` -  The number of frames to click for. 
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 # Double-click the left mouse button at (500, 500)
 await api.DoubleClick_XY(MouseButtons.LEFT, (500, 500), 5)
 ```
 ### <a id='DoubleClick_XY'></a> DoubleClick_XY(buttonId : `MouseButtons`, x : `float`, y : `float`, clickFrameCount : `int`, timeout : `int`) -> `bool`

 Double-clicks a mouse button at the target coordinates. 

#### Returns

 `True` if the command was sent successfully, `False` otherwise. 

#### Parameters

 - buttonId : `MouseButtons` -  The button to click. 
 - x : `float` -  The x position to click at. 
 - y : `float` -  The y position to click at. 
 - clickFrameCount : `int` -  The number of frames to click for. 
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 # Double-click the left mouse button at (500, 500)
 await api.DoubleClick_XY(MouseButtons.LEFT, 500, 500, 5)
 ```
 ### <a id='EnableHooks'></a> EnableHooks(hookingObject : `HookingObject`, timeout : `int`) -> `bool`

 Enables the given hooking object. 

#### Returns

 True if the command was sent successfully, False otherwise. 

#### Parameters

 - hookingObject : `HookingObject` -  The hooking object to enable. 
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 # Enable Mouse Hooks
 await api.EnableHooks(HookingObject.MOUSE)

 # Enable Gamepad Hooks
 await api.EnableHooks(HookingObject.GAMEPAD)

 # or just enable everything at once
 await api.EnableHooks(HookingObject.ALL)
 ```
 ### <a id='EnableObjectCaching'></a> EnableObjectCaching(timeout : `int`) -> `bool`

 Enables caching of objects for hierarchyPath resolution. 

#### Returns

 True if the command was sent successfully, False otherwise. 

#### Parameters

 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 await api.EnableObjectCaching()
 ```
 ### <a id='FlushObjectLookupCache'></a> FlushObjectLookupCache(timeout : `int`) -> `bool`

 Flushes the object lookup cache. 

#### Returns

 True if the command was sent successfully, False otherwise. 

#### Parameters

 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 await api.FlushObjectLookupCache()
 ```
 ### <a id='GetConnectedGameDetails'></a> GetConnectedGameDetails() -> `ProtocolObjects.GameConnectionDetails`

 Gets the details of the connected game. 

#### Returns

 The details of the connected game. 

#### Parameters




#### Example


 ```python
 details = await api.GetConnectedGameDetails()
 print(details.GameName)
 ```
 ### <a id='GetLastFPS'></a> GetLastFPS(timeout : `int`) -> `float`

 Gets the last reported FPS value. 

#### Returns

 The last FPS value. 

#### Parameters

 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 fps = await api.GetLastFPS()
 print(fps)
 ```
 ### <a id='GetNextCollisionEvent'></a> GetNextCollisionEvent() -> `ProtocolObjects.Collision`

 Gets the next collision event. 

#### Returns

 The next collision event. 

#### Parameters




#### Example


 ```python
 # Get the next collision event that happens on the `player` object
 id = await api.RegisterCollisionMonitor("//*[@name='Player']")
 collision = await api.GetNextCollisionEvent(id)
 print(collision)
 ```
 ### <a id='GetObjectDistance'></a> GetObjectDistance(objectA_HierarchyPath : `str`, objectB_HierarchyPath : `str`, timeout : `int`) -> `float`

 Gets the distance between two objects. 

#### Returns

 The distance between the objects. 

#### Parameters

 - objectA_HierarchyPath : `str` -  The hierarchy path of the first object. 
 - objectB_HierarchyPath : `str` -  The hierarchy path of the second object. 
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 distance = await api.GetObjectDistance("//*[@name='ObjectA']", "//*[@name='ObjectB']")
 print(distance)
 ```
 ### <a id='GetObjectFieldValue'></a> GetObjectFieldValue(t : `type`, hierarchyPath : `str`, timeout : `int`) -> `t`

 Gets the value of a field on an object. 

#### Returns

 The value of the field. 

#### Parameters

 - t : `type` -  The type of the field. 
 - hierarchyPath : `str` -  The hierarchy path of the target field. 
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 # Check to see if the `Player` object is active in the scene
 value = await api.GetObjectFieldValue(bool, "//Player[@name='Player']/@active")
 print(value)
 ```
 ### <a id='GetObjectFieldValueByName'></a> GetObjectFieldValueByName(hierarchyPath : `str`, fieldName : `str`, timeout : `int`) -> `t`

 Gets the value of a field on an object by field name. 

#### Returns

 The value of the field. 

#### Parameters

 - hierarchyPath : `str` -  The hierarchy path of the object. 
 - fieldName : `str` -  The name of the field. 
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 # Check to see if the `Player` object is active in the scene
 value = await api.GetObjectFieldValueByName('//*[@name='Player']', 'active')
 print(value)
 ```
 ### <a id='GetObjectList'></a> GetObjectList(timeout : `int`) -> `bool`

 Gets the list of objects in the scene. 

#### Returns

 True if successful, False otherwise. 

#### Parameters

 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
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
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 # Get the position of the `Player` object in screen space
 position = await api.GetObjectPosition("//*[@name='Player']", CoordinateConversion.SCREEN_SPACE)
 print(position)
 ```
 ### <a id='GetSceneName'></a> GetSceneName(timeout : `int`) -> `bool`

 Gets the name of the active scene. 

#### Returns

 True if successful, False otherwise. 

#### Parameters

 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 sceneName = await api.GetSceneName()
 print(sceneName)
 ```
 ### <a id='KeyPress'></a> KeyPress(keys : `list`, numberOfFrames : `int`, modifiers : `list`, modifiersNumberOfFrames : `int`, delayAfterModifiersMsec : `int`, timeout : `int`) -> `bool`

 Presses a key. 

#### Returns

 True if successful, False otherwise. 

#### Parameters

 - keys : `list` -  The keys to press. 
 - numberOfFrames : `int` -  The number of frames to press the keys. 
 - modifiers : `list` -  The modifiers to press. 
 - modifiersNumberOfFrames : `int` -  The number of frames to press the modifiers. 
 - delayAfterModifiersMsec : `int` -  The delay after pressing the modifiers. 
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 await api.KeyPress([KeyCode.A, KeyCode.B, KeyCode.C], 10)
 ```
 ### <a id='Launch'></a> Launch(filename : `str`, arguments : `str`) -> `bool`

 Launches an executable. 

#### Returns

 The process object. 

#### Parameters

 - filename : `str` -  The filename of the process to launch. 
 - arguments : `str` -  The arguments to launch the process with. 



#### Example


 ```python
 game_process = api.Launch("/path/to/executable.exe", "arg1 arg2")

 api.TerminateGame(game_process)
 ```
 ### <a id='LoadScene'></a> LoadScene(sceneName : `str`, timeout : `int`) -> `bool`

 Loads a scene by name. 

#### Returns

 True if successful, False otherwise. 

#### Parameters

 - sceneName : `str` -  The name of the scene to load. 
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 await api.LoadScene('SceneA')
 ```
 ### <a id='MouseDrag'></a> MouseDrag(button : `MouseButtons`, dx : `float`, dy : `float`, frameCount : `float`, ox : `float`, oy : `float`, waitForEmptyInput : `bool`, timeout : `int`) -> `bool`

 Drags the mouse. 

#### Returns

 True if successful, False otherwise. 

#### Parameters

 - button : `MouseButtons` -  The button to drag with. 
 - dx : `float` -  The amount to drag the mouse in the X direction. 
 - dy : `float` -  The amount to drag the mouse in the Y direction. 
 - frameCount : `float` -  The number of frames to drag the mouse. 
 - ox : `float` -  The offset X of the mouse. 
 - oy : `float` -  The offset Y of the mouse. 
 - waitForEmptyInput : `bool` -  Whether or not to wait for the mouse to be empty before continuing. 
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 # Drag the mouse to (10, 10) over the next 100 frames
 await api.MouseDrag(MouseButtons.Left, 10, 10, 100)
 ```
 ### <a id='MouseMoveToObject'></a> MouseMoveToObject(objectHierarchyPath : `str`, frameCount : `float`, waitForObject : `bool`, waitForEmptyInput : `bool`, timeout : `int`) -> `bool`

 Moves the mouse to an object. 

#### Returns

 True if successful, False otherwise. 

#### Parameters

 - objectHierarchyPath : `str` -  The object hierarchy path of the object to move to. 
 - frameCount : `float` -  The number of frames to move the mouse. 
 - waitForObject : `bool` -  Whether or not to wait for the object to be found. 
 - waitForEmptyInput : `bool` -  Whether or not to wait for the mouse to be empty before continuing. 
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 # Move the mouse to the object 'Box' over the next 100 frames
 await api.MouseMoveToObject("//*[@name='Box']", 100)
 ```
 ### <a id='MouseMoveToPoint'></a> MouseMoveToPoint(dx : `float`, dy : `float`, frameCount : `float`, ox : `float`, oy : `float`, waitForEmptyInput : `bool`, timeout : `int`) -> `bool`

 Moves the mouse to an absolute point on screen. 

#### Returns

 True if successful, False otherwise. 

#### Parameters

 - dx : `float` -  The amount to move the mouse in the X direction. 
 - dy : `float` -  The amount to move the mouse in the Y direction. 
 - frameCount : `float` -  The number of frames to move the mouse. 
 - ox : `float` -  The offset X of the mouse. 
 - oy : `float` -  The offset Y of the mouse. 
 - waitForEmptyInput : `bool` -  Whether or not to wait for the mouse to be empty before continuing. 
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 # Move the mouse to (10, 10) over the next 100 frames
 await api.MouseMoveToPoint(10, 10, 100)
 ```
 ### <a id='NavAgentMoveToPoint'></a> NavAgentMoveToPoint(navAgent_HierarchyPath : `str`, dx : `float`, dy : `float`, waitForMoveToComplete : `bool`, timeout : `int`) -> `bool`

 Moves the nav agent to a point. 

#### Returns

 True if successful, False otherwise. 

#### Parameters

 - navAgent_HierarchyPath : `str` -  The object hierarchy path of the nav agent to move. 
 - dx : `float` -  The amount to move the nav agent in the X direction. 
 - dy : `float` -  The amount to move the nav agent in the Y direction. 
 - waitForMoveToComplete : `bool` -  Whether or not to wait for the nav agent to reach the destination. 
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 # Move the nav agent to (100, 100)
 await api.NavAgentMoveToPoint("//*[@name='Agent']", 100, 100)
 ```
 ### <a id='Raycast'></a> Raycast(raycastPoint : `ProtocolObjects.Vector3`, cameraHierarchyPath : `str`, timeout : `int`) -> `list`

 Perform a Raycast to a point to find out what is in that position. 

#### Returns

 The raycast results. 

#### Parameters

 - raycastPoint : `ProtocolObjects.Vector3` -  The raycast point. 
 - cameraHierarchyPath : `str` -  The hierarchy path of the camera to use for the raycast. 
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 raycastPoint = ProtocolObjects.Vector3(100, 100, 100)
 raycastResults = await api.Raycast(raycastPoint)
 ```
 ### <a id='RegisterCollisionMonitor'></a> RegisterCollisionMonitor(HierarchyPath : `str`, timeout : `int`) -> `bool`

 Registers a collision monitor to recieve collision events on an object. 

#### Returns

 The Id of the collision monitor 

#### Parameters

 - HierarchyPath : `str` -  The hierarchy path of the object to monitor. 
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 # Begin recieving collision events that occur on the `Player` object
 monitorid = await api.RegisterCollisionMonitor("//*[@name='Player']")

 # Wait for a collision event
 await api.WaitForCollisionEvent(monitorid)

 # Stop recieving collision events on the `Player` object
 await api.UnregisterCollisionMonitor("//*[@name='Player']")
 ```
 ### <a id='RotateObject_AxisAngle'></a> RotateObject_AxisAngle(hierarchyPath : `str`, xAngle : `float`, yAngle : `float`, zAngle : `float`, relativeTo : `Space`, waitForObject : `bool`, timeout : `int`) -> `bool`

 Rotates an object using absolute axis angles. 

#### Returns

 True if successful, False otherwise. 

#### Parameters

 - hierarchyPath : `str` -  The hierarchy path of the object to rotate. 
 - xAngle : `float` -  The X angle to rotate the object by. 
 - yAngle : `float` -  The Y angle to rotate the object by. 
 - zAngle : `float` -  The Z angle to rotate the object by. 
 - relativeTo : `Space` -  The space to rotate the object in. 
 - waitForObject : `bool` -  Whether or not to wait for the object to rotate. 
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 # Rotate the `box` object by 10 degrees around the X axis, 20 degrees around the Y axis, and 30 degrees around the Z axis
 await api.RotateObject_AxisAngle("//*[@name='Box']", 10, 20, 30)
 ```
 ### <a id='RotateObject_Euler'></a> RotateObject_Euler(hierarchyPath : `str`, euler : `ProtocolObjects.Vector3`, relativeTo : `Space`, waitForObject : `bool`, timeout : `int`) -> `bool`

 Rotates an object using euler angles. 

#### Returns

 True if successful, False otherwise. 

#### Parameters

 - hierarchyPath : `str` -  The hierarchy path of the object to rotate. 
 - euler : `ProtocolObjects.Vector3` -  The Euler angles to rotate the object by. 
 - relativeTo : `Space` -  The space to rotate the object in. 
 - waitForObject : `bool` -  Whether or not to wait for the object to rotate. 
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 # Rotate the `box` object by 10 degrees around the X axis
 # then rotate it by 20 degrees around the new relative Y axis
 # then rotate it by 30 degrees around the new relative Z axis
 await api.RotateObject_Euler("//*[@name='Box']", ProtocolObjects.Vector3(10, 20, 30))
 ```
 ### <a id='RotateObject_Quaternion'></a> RotateObject_Quaternion(hierarchyPath : `str`, quaternion : `ProtocolObjects.Vector4`, waitForObject : `bool`, timeout : `int`) -> `bool`

 Rotates an object using a quaternion. 

#### Returns

 True if successful, False otherwise. 

#### Parameters

 - hierarchyPath : `str` -  The hierarchy path of the object to rotate. 
 - quaternion : `ProtocolObjects.Vector4` -  The quaternion to rotate the object by. 
 - waitForObject : `bool` -  Whether or not to wait for the object to rotate. 
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 # Rotate the `box` object by a quaternion of (0, 0, 0, 1)
 await api.RotateObject_Quaternion("//*[@name='Box']", Vector4(0, 0, 0, 1))
 ```
 ### <a id='SetInputFieldText'></a> SetInputFieldText(hierarchyPath : `str`, text : `str`, waitForObject : `bool`, timeout : `int`) -> `bool`

 Sets the text of an InputField or TMP_InputField. 

#### Returns

 True if successful, False otherwise. 

#### Parameters

 - hierarchyPath : `str` -  The hierarchy path of the input field. 
 - text : `str` -  The text to set the input field to. 
 - waitForObject : `bool` -  Whether or not to wait for the object to be set. 
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 # Set the text of the `InputField` object to `Hello World`
 await api.SetInputFieldText("//FilterInputTxt[@name='TextMeshPro InputField']", "Hello World")
 ```
 ### <a id='SetObjectFieldValue'></a> SetObjectFieldValue(hierarchyPath : `str`, fieldName : `str`, value : `object`, waitForObject : `bool`, timeout : `int`) -> `bool`

 Set the field or property of an object. 

#### Returns

 True if successful, False otherwise. 

#### Parameters

 - hierarchyPath : `str` -  The hierarchy path of the object. 
 - fieldName : `str` -  The name of the field or property to set. 
 - value : `object` -  The value to set the field or property to. 
 - waitForObject : `bool` -  If True, wait for the object to exist if it doesn't. 
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example

### <a id='StopEditorPlay'></a> StopEditorPlay() -> `None`

 Stops Play Mode in the Unity Editor. 

#### Returns



#### Parameters




#### Example


 ```python
 api.StopEditorPlay()
 ```
 ### <a id='TapObject'></a> TapObject(hierarchyPath : `str`, tapCount : `int`, frameCount : `int`, cameraHierarchyPath : `str`, timeout : `int`) -> `bool`

 Tap the handheld device at the target position. 

#### Returns

 True if successful, False otherwise. 

#### Parameters

 - hierarchyPath : `str` -  The hierarchy path of the object to tap. 
 - tapCount : `int` -  The number of times to tap the object. 
 - frameCount : `int` -  The number of frames to tap the object. 
 - cameraHierarchyPath : `str` -  The hierarchy path of the camera to use when tapping. 
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 # Tap the `TextMeshPro InputField` object
 await api.TapObject("//FilterInputTxt[@name='TextMeshPro InputField']")
 ```
 ### <a id='Tap_Vec2'></a> Tap_Vec2(position : `Vector2`, tapCount : `int`, frameCount : `int`, timeout : `int`) -> `bool`

 Tap the handheld device at the target position. 

#### Returns

 True if successful, False otherwise. 

#### Parameters

 - position : `Vector2` -  The position to tap. 
 - tapCount : `int` -  The number of times to tap the object. 
 - frameCount : `int` -  The number of frames to tap the object. 
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 await api.Tap_Vec2(Vector2(100, 100))
 ```
 ### <a id='Tap_XY'></a> Tap_XY(x : `float`, y : `float`, tapCount : `int`, frameCount : `int`, timeout : `int`) -> `bool`

 Tap the handheld device at the target position. 

#### Returns

 True if successful, False otherwise. 

#### Parameters

 - x : `float` -  The X coordinate to tap. 
 - y : `float` -  The Y coordinate to tap. 
 - tapCount : `int` -  The number of times to tap the object. 
 - frameCount : `int` -  The number of frames to tap the object. 
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 await api.Tap_XY(100, 100)
 ```
 ### <a id='TerminateGame'></a> TerminateGame() -> `None`

 Terminates the game. 

#### Returns



#### Parameters




#### Example


 ```python
 game_process = api.Launch("/path/to/executable.exe", "arg1 arg2")

 api.TerminateGame(game_process)
 ```
 ### <a id='ToggleEditorPause'></a> ToggleEditorPause() -> `bool`

 Toggles Pause in the Unity Editor while Play Mode is active. 

#### Returns

 True if successful, False otherwise. 

#### Parameters




#### Example


 ```python
 api.ToggleEditorPause()
 ```
 ### <a id='ToggleEditorPlay'></a> ToggleEditorPlay() -> `bool`

 Toggles Play Mode in the Unity Editor. 

#### Returns

 True if successful, False otherwise. 

#### Parameters




#### Example


 ```python
 api.ToggleEditorPlay()
 ```
 ### <a id='TouchInput'></a> TouchInput(x1 : `float`, y1 : `float`, x2 : `float`, y2 : `float`, fingerId : `int`, tapCount : `int`, frameCount : `int`, waitForEmptyInput : `bool`, radius : `float`, pressure : `float`, altitudeAngle : `float`, azmulthAngle : `float`, maximumPossiblePressure : `float`, timeout : `int`) -> `bool`

 Touches an object. 

#### Returns

 True if successful, False otherwise. 

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
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 # Performs a single touch input from 0,0 to 100, 100 with a single "finger" over a duration of 50 frames
 await api.TouchInput(Vector2(0, 0), Vector2(100, 100), 0, 1, 50);
 ```
 ### <a id='UnregisterCollisionMonitor'></a> UnregisterCollisionMonitor(hierarchyPath : `str`, timeout : `int`) -> `bool`

 Unregisters a collision monitor to stop recieving collision events on an object. 

#### Returns

 True if successful, False otherwise. 

#### Parameters

 - hierarchyPath : `str` -  The hierarchy path of the object to monitor. 
 - timeout : `int` -  The number of seconds to wait for the command to be processed by the agent. 



#### Example


 ```python
 # Begin recieving collision events that occur on the `Player` object
 monitorid = await api.RegisterCollisionMonitor("//*[@name='Player']")

 # Wait for a collision event
 await api.WaitForCollisionEvent(monitorid)

 # Stop recieving collision events on the `Player` object
 await api.UnregisterCollisionMonitor("//*[@name='Player']")
 ```
 ### <a id='Wait'></a> Wait(miliseconds : `int`) -> `None`

 Waits for a specified number of miliseconds. 

#### Returns



#### Parameters

 - miliseconds : `int` -  The number of miliseconds to wait. 



#### Example


 ```python
 # Waits for 1 second
 await api.Wait(1000)
 ```
 ### <a id='WaitForCollisionEvent'></a> WaitForCollisionEvent(eventId : `str`, timeout : `int`) -> `ProtocolObjects.Collision`

 Waits for a new collision event. 

#### Returns

 The collision event message. 

#### Parameters

 - eventId : `str` -  The Id of the collision monitor to wait for an event from. 
 - timeout : `int` -  The number of seconds to wait for the event to be processed 



#### Example


 ```python
 # Begin recieving collision events that occur on the `Player` object
 monitorid = await api.RegisterCollisionMonitor("//*[@name='Player']")

 # Wait for a collision event
 await api.WaitForCollisionEvent(monitorid)

 # Stop recieving collision events on the `Player` object
 await api.UnregisterCollisionMonitor("//*[@name='Player']")
 ```
 ### <a id='WaitForEmptyInput'></a> WaitForEmptyInput(timeout : `int`) -> `None`

 Waits for an empty input event. 

#### Returns



#### Parameters

 - timeout : `int` -  The number of seconds to wait for the event to be processed 



#### Example


 ```python
 await api.WaitForEmptyInput()
 ```
 ### <a id='WaitForObject'></a> WaitForObject(hierarchyPath : `str`, timeout : `int`) -> `bool`

 Waits for an object to exist. 

#### Returns

 True if successful, False otherwise. 

#### Parameters

 - hierarchyPath : `str` -  The hierarchy path of the object to wait for. 
 - timeout : `int` -  The number of seconds to wait for the object to exist. 



#### Example


 ```python
 # Waits for the `Key` object to exist
 await api.WaitForObject('//*[@name='Key']')
 ```
 ### <a id='waitForObjectValue'></a> waitForObjectValue(hierarchyPath : `str`, fieldOrPropertyName : `str`, value : `str`, timeout : `int`) -> `bool`

 Wait for an object to exist and have a specific value for a specified field/property. 

#### Returns

 True if successful, False otherwise. 

#### Parameters

 - hierarchyPath : `str` -  The hierarchy path of the object to wait for. 
 - fieldOrPropertyName : `str` -  The name of the field/property to wait for. 
 - value : `str` -  The value to wait for. 
 - timeout : `int` -  The number of seconds to wait for the object to exist 



#### Example


 ```python
 # Waits for the `Button` object to exist and have a value of `True` for the `isPressed` property
 await api.WaitForObject("//*[@name='Button']/fn:component('ButtonScript')", 'isPressed', True)
 ```
 