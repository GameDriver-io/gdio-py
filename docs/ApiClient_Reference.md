# `class` ApiClient

GameDriver.io Unity API Client class.

## Methods

| Name | Summary |
| ---- | ---- |
| AxisPress -> `bool` |  Presses the target axis for the specified number of frames.  |
| ButtonPress -> `bool` |  Presses the target button for the specified number of frames.  |
| CallMethod -> `bool` |  Calls a method on the target object.  |
| CallMethod_Void -> `bool` |  Calls a void method on the target object.  |
| CaptureScreenshot -> `str` |  Captures a screenshot of the currently connected app.  |
| ClickEx_Vec2 -> `bool` |  Clicks a mouse button at the target coordinates with modifier keys.  |
| ClickEx_XY -> `bool` |  Clicks a mouse button at the target coordinates with modifier keys.  |
| ClickObject -> `bool` |  Clicks a mouse button at the position of the target object.  |
| ClickObjectEx -> `bool` |  Clicks a mouse button at the position of the target object with modifier keys.  |
| Click_Vec2 -> `bool` |  Clicks a mouse button at the target coordinates.  |
| Click_XY -> `bool` |  Clicks a mouse button at the target coordinates.  |
| Connect -> `bool` |  Connects to an agent at the target hostname and port.  |
| DisableHooks -> `bool` |  Disables the ability to preform the target input type from the ApiClient.  |
| DisableObjectCaching -> `bool` |  Disables object caching for HierarchyPath resolution.  |
| Disconnect -> `None` |  Disconnects from the agent.  |
| DoubleClickEx_Vec2 -> `bool` |  Clicks the mouse at the given coordinates.  |
| DoubleClickEx_XY -> `bool` |  Clicks the mouse at the given coordinates.  |
| DoubleClickObject -> `bool` |  Clicks the mouse at the given coordinates.  |
| DoubleClickObjectEx -> `bool` |  Clicks the mouse at the given coordinates.  |
| DoubleClick_Vec2 -> `bool` |  Clicks the mouse at the given coordinates.  |
| DoubleClick_XY -> `bool` |  Clicks the mouse at the given coordinates.  |
| EnableHooks -> `bool` |  Enables the given hooking object.  |
| EnableObjectCaching -> `bool` |  Enables object caching.  |
| FlushObjectLookupCache -> `bool` |  Flushes the object lookup cache.  |
| GetConnectedGameDetails -> `ProtocolObjects.GameConnectionDetails` |  Gets the details of the connected game.  |
| GetLastFPS -> `float` |  Gets the last FPS value.  |
| GetNextCollisionEvent -> `ProtocolObjects.Collision` |  **Not Implemented** Gets the next collision event.  |
| GetObjectDistance -> `float` |  **Not Implemented** Gets the distance between two objects.  |
| GetObjectFieldValue -> `t` |  **Not Implemented** Gets the value of a field on an object.  |
| GetObjectFieldValueByName -> `t` |  **Not Implemented** Gets the value of a field on an object.  |
| GetObjectList -> `bool` |  Gets the list of objects.  |
| GetObjectPosition -> `ProtocolObjects.Vector3` |  Gets the position of an object.  |
| GetSceneName -> `bool` |  Gets the name of the scene.  |
| GetVersionString -> `str` |  **Not Implemented** Gets the version string of the agent.  |
| KeyPress -> `bool` |  Presses a key.  |
| Launch -> `None` |  **Not Implemented** Launches a process.  |
| LoadScene -> `bool` |  Loads a scene.  |
| MouseDrag -> `bool` |  Drags the mouse.  |
| MouseMoveToObject -> `bool` |  Moves the mouse to an object.  |
| MouseMoveToPoint -> `bool` |  Moves the mouse to a point.  |
| NavAgentMoveToPoint -> `bool` |  Moves the nav agent to a point.  |
| Raycast -> `list` |  Performs a raycast.  |
| RegisterCollisionMonitor -> `bool` |  Registers a collision monitor.  |
| RotateObject_AxisAngle -> `bool` |  Rotates an object.  |
| RotateObject_Euler -> `bool` |  Rotates an object.  |
| RotateObject_Quaternion -> `bool` |  Rotates an object.  |
| SetInputFieldText -> `bool` |  Sets the text of an input field.  |
| SetObjectFieldValue -> `bool` |  **Not Implemented** Sets the value of an object field.  |
| TapObject -> `bool` |  Taps an object.  |
| Tap_Vec2 -> `bool` |  Taps an object.  |
| Tap_XY -> `bool` |  Taps an object.  |
| TerminateGame -> `bool` |  **Not Implemented** Terminates the game.  |
| ToggleEditorPause -> `bool` |  **Not Implemented** Toggles the editor pause.  |
| ToggleEditorPlay -> `bool` |  **Not Implemented** Toggles the editor play.  |
| TouchInput -> `bool` |  Touches an object.  |
| UnregisterCollisionMonitor -> `bool` |  Unregisters a collision monitor.  |
| Wait -> `None` |  Waits for a specified number of miliseconds.  |
| WaitForCollisionEvent -> `ProtocolObjects.Collision` |  **Not Implemented** Waits for a collision event.  |
| WaitForEmptyInput -> `bool` |  Waits for an empty input event.  |
| waitForObject -> `bool` |  **Not Implemented** Waits for an object.  |
| waitForObjectValue -> `bool` |  **Not Implemented** Waits for an object value.  |
### `bool` AxisPress(axisId : `str`, value : `float`, numberOfFrames : `int`, timeout : `int`)

 Presses the target axis for the specified number of frames. 

#### Returns

 `True` if the command was sent successfully, `False` otherwise. 

#### Parameters








#### Example


 ```python
 api = ApiClient()
 await api.Connect()

 # Move the horizontal axis to the right for 100 frames.
 await api.AxisPress(axisId='Horizontal', value=1.0, numberOfFrames=100)
 ```
 ### `bool` ButtonPress(buttonId : `str`, numberOfFrames : `int`, timeout : `int`)

 Presses the target button for the specified number of frames. 

#### Returns

 `True` if the command was sent successfully, `False` otherwise. 

#### Parameters







#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 # Press the Jump button for 100 frames.
 await api.ButtonPress(buttonId='Jump', numberOfFrames=100)
 ```
 ### `bool` CallMethod(t : `type`, hierarchyPath : `str`, methodName : `str`, arguments : `list[any]`, timeout : `int`)

 Calls a method on the target object. 

#### Returns

 The return value of the target method of type `t`. 

#### Parameters









#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.CallMethod(t=int, hierarchyPath="//*[@name='Player']/fn:component('PlayerController')", methodName="Jump")
 ```
 ### `bool` CallMethod_Void(hierarchyPath : `str`, methodName : `str`, arguments : `list[any]`, timeout : `int`)

 Calls a void method on the target object. 

#### Returns

 `True` if the command was sent successfully, `False` otherwise. 

#### Parameters








#### Example


 ```python
 api = ApiClient()
 await api.Connect()

 # Call the `Jump` method on the `Player` object at the scene root.
 await api.CallMethod("//*[@name='Player']/fn:component('PlayerController')", "Jump")
 ```
 ### `str` CaptureScreenshot(filename : `str`, storeInGameFolder : `bool`, overwriteExisting : `bool`, timeout : `int`)

 Captures a screenshot of the currently connected app. 

#### Returns

 The path and filename of the screen capture. 

#### Parameters








#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.CaptureScreenshot(filename='/path/to/file')
 ```
 ### `bool` ClickEx_Vec2(buttonId : `Enums.MouseButtons`, position : `ProtocolObjects.Vector2`, clickFrameCount : `int`, keys : `list[Enums.KeyCode]`, keysNumberOfFrames : `int`, modifiers : `list[Enums.KeyCode]`, modifiersNumberOfFrames : `int`, delayAfterModifiersMsec : `int`, timeout : `int`)

 Clicks a mouse button at the target coordinates with modifier keys. 

#### Returns

 `True` if the command was sent successfully, `False` otherwise. 

#### Parameters













#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 # Shift+Left click the screen at (100, 100) for 5 frames.
 await api.ClickEx_XY(buttonId=Enums.MouseButtons.Left, position=(100, 100), clickFrameCount=5, keys=[Enums.KeyCode.LShift], keysNumberOfFrames=5)
 ```
 ### `bool` ClickEx_XY(buttonId : `Enums.MouseButtons`, x : `float`, y : `float`, clickFrameCount : `int`, keys : `list[Enums.KeyCode]`, keysNumberOfFrames : `int`, modifiers : `list[Enums.KeyCode]`, modifiersNumberOfFrames : `int`, delayAfterModifiersMsec : `int`, timeout : `int`)

 Clicks a mouse button at the target coordinates with modifier keys. 

#### Returns

 `True` if the command was sent successfully, `False` otherwise. 

#### Parameters














#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 # Shift+Left click the screen at (100, 100) for 5 frames.
 await api.ClickEx_XY(buttonId=Enums.MouseButtons.Left, x=100, y=100, clickFrameCount=5, keys=[Enums.KeyCode.LShift], keysNumberOfFrames=5)
 ```
 ### `bool` ClickObject(buttonId : `Enums.MouseButtons`, hierarchyPath : `str`, frameCount : `int`, cameraHierarchyPath : `str`, timeout : `int`)

 Clicks a mouse button at the position of the target object. 

#### Returns

 `True` if the command was sent successfully, `False` otherwise. 

#### Parameters









#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 # Left click the screen at the position of the `Player` object for 5 frames.
 await api.ClickObject(buttonId=Enums.MouseButtons.Left, hierarchyPath="//*[@name='Player']", frameCount=5)
 ```
 ### `bool` ClickObjectEx(buttonId : `Enums.MouseButtons`, hierarchyPath : `str`, frameCount : `int`, cameraHierarchyPath : `str`, keys : `list`, keysNumberOfFrames : `int`, modifiers : `list`, modifiersNumberOfFrames : `int`, delayAfterModifiersMsec : `int`, timeout : `int`)

 Clicks a mouse button at the position of the target object with modifier keys. 

#### Returns

 True if the command was sent successfully, False otherwise. 

#### Parameters














#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 # Shift+Left click the screen at the position of the `Player` object for 5 frames.
 await api.ClickObjectEx(buttonId=Enums.MouseButtons.Left, hierarchyPath="//*[@name='Player']", frameCount=5, keys=[Enums.KeyCode.LShift], keysNumberOfFrames=5)
 ```
 ### `bool` Click_Vec2(buttonId : `Enums.MouseButtons`, position : `ProtocolObjects.Vector2`, clickFrameCount : `int`, timeout : `int`)

 Clicks a mouse button at the target coordinates. 

#### Returns

 `True` if the command was sent successfully, `False` otherwise. 

#### Parameters








#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 # Left click the screen at (100, 100) for 5 frames.
 await api.Click_XY(ButtonId=Enums.MouseButtons.Left, position=(100, 100), clickFrameCount=5)
 ```
 ### `bool` Click_XY(buttonId : `Enums.MouseButtons`, x : `float`, y : `float`, clickFrameCount : `int`, timeout : `int`)

 Clicks a mouse button at the target coordinates. 

#### Returns

 `True` if the command was sent successfully, `False` otherwise. 

#### Parameters









#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 # Left click the screen at (100, 100) for 5 frames.
 await api.Click_XY(ButtonId=Enums.MouseButtons.Left, x=100, y=100, clickFrameCount=5)
 ```
 ### `bool` Connect(hostname : `str`, port : `int`, autoplay : `bool`, timeout : `int`, autoPortResolution : `bool`)

 Connects to an agent at the target hostname and port. 

#### Returns

 True if nothing went wrong while trying to connect; None otherwise 

#### Parameters









#### Example


 ```python
 api = ApiClient()
 if await api.Connect(hostname='localhost', port=19734):
 print("Connected!")
 ```
 ### `bool` DisableHooks(Enums.HookingObject : `str`, timeout : `int`)

 Disables the ability to preform the target input type from the ApiClient. 

#### Returns

 True if the command was sent successfully, False otherwise. 

#### Parameters






#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 # Disable Keyboard, Mouse, Touch and Controller hooks globally.
 await api.DisableHooks(hookingObject=Enums.HookingObject.All)
 ```
 ### `bool` DisableObjectCaching(timeout : `int`)

 Disables object caching for HierarchyPath resolution. 

#### Returns

 `True` if the command was sent successfully, `False` otherwise. 

#### Parameters





#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.DisableObjectCaching()
 ```
 ### `None` Disconnect()

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
 ### `bool` DoubleClickEx_Vec2(buttonId : `Enums.MouseButtons`, position : `ProtocolObjects.Vector2`, clickFrameCount : `int`, keys : `list`, keysNumberOfFrames : `int`, modifiers : `list`, modifiersNumberOfFrames : `int`, delayAfterModifiersMsec : `int`, timeout : `int`)

 Clicks the mouse at the given coordinates. 

#### Returns

 True if the command was sent successfully, False otherwise. 

#### Parameters













#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.DoubleClickEx_Vec2(Enums.MouseButtons.LEFT, ProtocolObjects.Vector2(500, 500), 5, [Enums.Keys.SHIFT, Enums.Keys.CONTROL], 5, [Enums.Modifiers.SHIFT, Enums.Modifiers.CONTROL], 3, 500)
 ```
 ### `bool` DoubleClickEx_XY(buttonId : `Enums.MouseButtons`, x : `float`, y : `float`, clickFrameCount : `int`, keys : `list`, keysNumberOfFrames : `int`, modifiers : `list`, modifiersNumberOfFrames : `int`, delayAfterModifiersMsec : `int`, timeout : `int`)

 Clicks the mouse at the given coordinates. 

#### Returns

 True if the command was sent successfully, False otherwise. 

#### Parameters














#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.DoubleClickEx_XY(Enums.MouseButtons.LEFT, 500, 500, 5, [Enums.Keys.SHIFT, Enums.Keys.CONTROL], 5, [Enums.Modifiers.SHIFT, Enums.Modifiers.CONTROL], 3, 500)
 ```
 ### `bool` DoubleClickObject(buttonId : `Enums.MouseButtons`, hierarchyPath : `str`, frameCount : `int`, timeout : `int`)

 Clicks the mouse at the given coordinates. 

#### Returns

 True if the command was sent successfully, False otherwise. 

#### Parameters








#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.DoubleClickObject(Enums.MouseButtons.LEFT, "HierarchyPath", 5)
 ```
 ### `bool` DoubleClickObjectEx(buttonId : `Enums.MouseButtons`, hierarchyPath : `str`, clickFrameCount : `int`, keys : `list`, keysNumberOfFrames : `int`, modifiers : `list`, modifiersNumberOfFrames : `int`, delayAfterModifiersMsec : `int`, timeout : `int`)

 Clicks the mouse at the given coordinates. 

#### Returns

 True if the command was sent successfully, False otherwise. 

#### Parameters













#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.DoubleClickObjectEx(Enums.MouseButtons.LEFT, "HierarchyPath", 5, [Enums.Keys.SHIFT, Enums.Keys.CONTROL], 5, [Enums.Modifiers.SHIFT, Enums.Modifiers.CONTROL], 3, 500)
 ```
 ### `bool` DoubleClick_Vec2(buttonId : `Enums.MouseButtons`, position : `ProtocolObjects.Vector2`, clickFrameCount : `int`, timeout : `int`)

 Clicks the mouse at the given coordinates. 

#### Returns

 True if the command was sent successfully, False otherwise. 

#### Parameters








#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.DoubleClick_Vec2(Enums.MouseButtons.LEFT, ProtocolObjects.Vector2(500, 500), 5)
 ```
 ### `bool` DoubleClick_XY(buttonId : `Enums.MouseButtons`, x : `float`, y : `float`, clickFrameCount : `int`, timeout : `int`)

 Clicks the mouse at the given coordinates. 

#### Returns

 `True` if the command was sent successfully, `False` otherwise. 

#### Parameters









#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.DoubleClick_XY(Enums.MouseButtons.LEFT, 500, 500, 5)
 ```
 ### `bool` EnableHooks(hookingObject : `Enums.HookingObject`, timeout : `int`)

 Enables the given hooking object. 

#### Returns

 True if the command was sent successfully, False otherwise. 

#### Parameters






#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.EnableHooks(Enums.HookingObject.MOUSE)
 ```
 ### `bool` EnableObjectCaching(timeout : `int`)

 Enables object caching. 

#### Returns

 True if the command was sent successfully, False otherwise. 

#### Parameters





#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.EnableObjectCaching()
 ```
 ### `bool` FlushObjectLookupCache(timeout : `int`)

 Flushes the object lookup cache. 

#### Returns

 True if the command was sent successfully, False otherwise. 

#### Parameters





#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.FlushObjectLookupCache()
 ```
 ### `ProtocolObjects.GameConnectionDetails` GetConnectedGameDetails()

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
 ### `float` GetLastFPS(timeout : `int`)

 Gets the last FPS value. 

#### Returns

 The last FPS value. 

#### Parameters





#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 fps = await api.GetLastFPS()
 print(fps)
 ```
 ### `ProtocolObjects.Collision` GetNextCollisionEvent()

 **Not Implemented** Gets the next collision event. 

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
 ### `float` GetObjectDistance(objectA_HierarchyPath : `str`, objectB_HierarchyPath : `str`, timeout : `int`)

 **Not Implemented** Gets the distance between two objects. 

#### Returns

 The distance between the objects. 

#### Parameters







#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 distance = await api.GetObjectDistance('ObjectA', 'ObjectB')
 print(distance)
 ```
 ### `t` GetObjectFieldValue(t : `type`, hierarchyPath : `str`, timeout : `int`)

 **Not Implemented** Gets the value of a field on an object. 

#### Returns

 The value of the field. 

#### Parameters







#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 value = await api.GetObjectFieldValue(type(int), 'ObjectA')
 print(value)
 ```
 ### `t` GetObjectFieldValueByName(hierarchyPath : `str`, fieldName : `str`, timeout : `int`)

 **Not Implemented** Gets the value of a field on an object. 

#### Returns

 The value of the field. 

#### Parameters







#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 value = await api.GetObjectFieldValueByName('ObjectA', 'Position')
 print(value)
 ```
 ### `bool` GetObjectList(timeout : `int`)

 Gets the list of objects. 

#### Returns

 True if successful, false otherwise. 

#### Parameters





#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 objects = await api.GetObjectList()
 print(objects)
 ```
 ### `ProtocolObjects.Vector3` GetObjectPosition(hierarchyPath : `str`, coordSpace : `Enums.CoordinateConversion`, cameraHierarchyPath : `str`, timeout : `int`)

 Gets the position of an object. 

#### Returns

 The position of the object. 

#### Parameters








#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 position = await api.GetObjectPosition('ObjectA')
 print(position)
 ```
 ### `bool` GetSceneName(timeout : `int`)

 Gets the name of the scene. 

#### Returns

 True if successful, false otherwise. 

#### Parameters





#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 sceneName = await api.GetSceneName()
 print(sceneName)
 ```
 ### `str` GetVersionString()

 **Not Implemented** Gets the version string of the agent. 

#### Returns

 The version string of the agent. 

#### Parameters




#### Example


 ```python
 api = ApiClient()
 print(api.GetVersionString())
 ```
 ### `bool` KeyPress(keys : `list`, numberOfFrames : `int`, modifiers : `list`, modifiersNumberOfFrames : `int`, delayAfterModifiersMsec : `int`, timeout : `int`)

 Presses a key. 

#### Returns

 True if successful, false otherwise. 

#### Parameters










#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.KeyPress(['A', 'B'], 10)
 ```
 ### `None` Launch(filename : `str`, arguments : `str`)

 **Not Implemented** Launches a process. 

#### Returns



#### Parameters






#### Example


 ```python
 # TODO
 ```
 ### `bool` LoadScene(sceneName : `str`, timeout : `int`)

 Loads a scene. 

#### Returns

 True if successful, false otherwise. 

#### Parameters






#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.LoadScene('SceneA')
 ```
 ### `bool` MouseDrag(button : `Enums.MouseButtons`, dx : `float`, dy : `float`, frameCount : `float`, ox : `float`, oy : `float`, waitForEmptyInput : `bool`, timeout : `int`)

 Drags the mouse. 

#### Returns

 True if successful, false otherwise. 

#### Parameters












#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.MouseDrag(Enums.MouseButtons.Left, 10, 10, 10)
 ```
 ### `bool` MouseMoveToObject(objectHierarchyPath : `str`, frameCount : `float`, waitForObject : `bool`, waitForEmptyInput : `bool`, timeout : `int`)

 Moves the mouse to an object. 

#### Returns

 True if successful, false otherwise. 

#### Parameters









#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.MouseMoveToObject('/root/SceneA/UI/ButtonA', 10)
 ```
 ### `bool` MouseMoveToPoint(dx : `float`, dy : `float`, frameCount : `float`, ox : `float`, oy : `float`, waitForEmptyInput : `bool`, timeout : `int`)

 Moves the mouse to a point. 

#### Returns

 True if successful, false otherwise. 

#### Parameters











#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.MouseMoveToPoint(10, 10, 10)
 ```
 ### `bool` NavAgentMoveToPoint(navAgent_HierarchyPath : `str`, dx : `float`, dy : `float`, waitForMoveToComplete : `bool`, timeout : `int`)

 Moves the nav agent to a point. 

#### Returns

 True if successful, false otherwise. 

#### Parameters









#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.NavAgentMoveToPoint('/root/SceneA/NavAgentA', 10, 10)
 ```
 ### `list` Raycast(raycastPoint : `ProtocolObjects.Vector3`, cameraHierarchyPath : `str`, timeout : `int`)

 Performs a raycast. 

#### Returns

 The raycast results. 

#### Parameters







#### Example


 ```python
 api = ApiClient()
 await api.Connect()

 raycastPoint = ProtocolObjects.Vector3(10, 10, 10)
 cameraHierarchyPath = '/root/SceneA/CameraA'
 raycastResults = await api.Raycast(raycastPoint, cameraHierarchyPath)
 ```
 ### `bool` RegisterCollisionMonitor(HierarchyPath : `str`, timeout : `int`)

 Registers a collision monitor. 

#### Returns

 True if successful, false otherwise. 

#### Parameters






#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.RegisterCollisionMonitor('/root/SceneA/ObjectA')
 ```
 ### `bool` RotateObject_AxisAngle(hierarchyPath : `str`, xAngle : `float`, yAngle : `float`, zAngle : `float`, relativeTo : `Enums.Space`, waitForObject : `bool`, timeout : `int`)

 Rotates an object. 

#### Returns

 True if successful, false otherwise. 

#### Parameters











#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.RotateObject_AxisAngle('/root/SceneA/ObjectA', 1, 1, 1)
 ```
 ### `bool` RotateObject_Euler(hierarchyPath : `str`, euler : `ProtocolObjects.Vector3`, relativeTo : `Enums.Space`, waitForObject : `bool`, timeout : `int`)

 Rotates an object. 

#### Returns

 True if successful, false otherwise. 

#### Parameters









#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.RotateObject_Euler('/root/SceneA/ObjectA', ProtocolObjects.Vector3(1, 1, 1))
 ```
 ### `bool` RotateObject_Quaternion(hierarchyPath : `str`, quaternion : `ProtocolObjects.Vector4`, waitForObject : `bool`, timeout : `int`)

 Rotates an object. 

#### Returns

 True if successful, false otherwise. 

#### Parameters








#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.RotateObject_Quaternion('/root/SceneA/ObjectA', ProtocolObjects.Vector4(1, 1, 1, 1))
 ```
 ### `bool` SetInputFieldText(hierarchyPath : `str`, text : `str`, waitForObject : `bool`, timeout : `int`)

 Sets the text of an input field. 

#### Returns

 True if successful, false otherwise. 

#### Parameters








#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.SetInputFieldText('/root/SceneA/ObjectA', 'Hello World')
 ```
 ### `bool` SetObjectFieldValue()

 **Not Implemented** Sets the value of an object field. 

#### Returns

 True if successful, false otherwise. 

#### Parameters




#### Example

### `bool` TapObject(hierarchyPath : `str`, tapCount : `int`, frameCount : `int`, cameraHierarchyPath : `str`, timeout : `int`)

 Taps an object. 

#### Returns

 True if successful, false otherwise. 

#### Parameters









#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.TapObject('/root/SceneA/ObjectA')
 ```
 ### `bool` Tap_Vec2(position : `ProtocolObjects.Vector2`, tapCount : `int`, frameCount : `int`, timeout : `int`)

 Taps an object. 

#### Returns

 True if successful, false otherwise. 

#### Parameters








#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.Tap_Vec2(ProtocolObjects.Vector2(1, 1))
 ```
 ### `bool` Tap_XY(x : `float`, y : `float`, tapCount : `int`, frameCount : `int`, timeout : `int`)

 Taps an object. 

#### Returns

 True if successful, false otherwise. 

#### Parameters









#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.Tap_XY(1, 1)
 ```
 ### `bool` TerminateGame()

 **Not Implemented** Terminates the game. 

#### Returns

 True if successful, false otherwise. 

#### Parameters




#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.TerminateGame()
 ```
 ### `bool` ToggleEditorPause()

 **Not Implemented** Toggles the editor pause. 

#### Returns

 True if successful, false otherwise. 

#### Parameters




#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.ToggleEditorPause()
 ```
 ### `bool` ToggleEditorPlay()

 **Not Implemented** Toggles the editor play. 

#### Returns

 True if successful, false otherwise. 

#### Parameters




#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.ToggleEditorPlay()
 ```
 ### `bool` TouchInput(x1 : `float`, y1 : `float`, x2 : `float`, y2 : `float`, fingerId : `int`, tapCount : `int`, frameCount : `int`, waitForEmptyInput : `bool`, radius : `float`, pressure : `float`, altitudeAngle : `float`, azmulthAngle : `float`, maximumPossiblePressure : `float`, timeout : `int`)

 Touches an object. 

#### Returns

 True if successful, false otherwise. 

#### Parameters


















#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.TouchInput(1, 1, 1, 1, 1)
 ```
 ### `bool` UnregisterCollisionMonitor(hierarchyPath : `str`, timeout : `int`)

 Unregisters a collision monitor. 

#### Returns

 True if successful, false otherwise. 

#### Parameters






#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.UnregisterCollisionMonitor('/root/SceneA/ObjectA')
 ```
 ### `None` Wait(miliseconds : `int`)

 Waits for a specified number of miliseconds. 

#### Returns



#### Parameters





#### Example


 ```python
 api = ApiClient()
 
 await api.Wait(1000)
 ```
 ### `ProtocolObjects.Collision` WaitForCollisionEvent(eventId : `str`, timeout : `int`)

 **Not Implemented** Waits for a collision event. 

#### Returns

 The collision event message. 

#### Parameters






#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.WaitForCollisionEvent('123')
 ```
 ### `bool` WaitForEmptyInput(timeout : `int`)

 Waits for an empty input event. 

#### Returns

 `True` if the event was recieved in time, `False` otherwise. 

#### Parameters





#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.WaitForEmptyInput()
 ```
 ### `bool` waitForObject(hierarchyPath : `str`, timeout : `int`)

 **Not Implemented** Waits for an object. 

#### Returns

 True if successful, false otherwise. 

#### Parameters






#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.WaitForObject('/root/SceneA/ObjectA')
 ```
 ### `bool` waitForObjectValue(hierarchyPath : `str`, timeout : `int`)

 **Not Implemented** Waits for an object value. 

#### Returns

 True if successful, false otherwise. 

#### Parameters






#### Example


 ```python
 api = ApiClient()
 await api.Connect()
 
 await api.WaitForObjectValue('/root/SceneA/ObjectA')
 ```
 