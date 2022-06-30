from re import M
from .Client import Client
from . import ProtocolObjects, Messages, Enums
from _gdio import Serializers

from functools import wraps

import msgpack
import os
import asyncio, socket
import time, datetime
import subprocess

import logging

from .constants import *

def requireClientConnectionAsync(function):
    @wraps(function)
    async def inner(*args, **kwargs):
        if args[0].client == None:
            raise Exception("This method requires a client connection")
        return await function(*args, **kwargs)
    return inner

def requireClientConnection(function):
    @wraps(function)
    def inner(*args, **kwargs):
        if args[0].client == None:
            raise Exception("This method requires a client connection")
        return function(*args, **kwargs)
    return inner


def UDPsend(hostname, port, data):
    UdpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UdpClient.sendto(bytes(data, 'utf-8'), (hostname, port))
    UdpClient.close()


class ApiClient:
    '''
    GameDriver.io Unity API Client class.
    '''
    def __init__(self,

            hostname           : str = '127.0.0.1', # The hostname of the device running the target game.
            port               : int = 19734,       # The port that the target Gamedriver agent is configured to use.
            autoplay           : bool = False,      # Start the game automatically within the Unity Editor.
            connectionTimeout  : int = 30,          # The number of seconds to wait for the command to be processed by the agent.
            autoPortResolution : bool = True,       # TODO: Automatically resolve the port a Gamedriver Agent is running on.

            debug : bool = False,
            customSerializer : Serializers.CustomSerializer = None
        ):

        self.hostname = hostname
        self.port = port
        self.autoplay = autoplay
        self.connectionTimeout = connectionTimeout
        self.autoPortResolution = autoPortResolution
    
        
        # Defined in self.Connect()
        self.client = None
        self.CurrentPlayDetails = None
        self.gameConnectionDetails = None

        if debug:
            log_file_path = f'logs/{datetime.datetime.now().date().strftime("%Y-%m-%d")}.log'
            i = 1
            while os.path.exists(log_file_path):
                log_file_path = f'logs/{datetime.datetime.now().date().strftime(f"%Y-%m-%d-{i}")}.log'
                i += 1

            logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', filename=log_file_path, filemode='w')

        self.CustomSerializer = customSerializer

    @requireClientConnectionAsync
    async def AxisPress(self,
            axisId         : str,      # The name of the target input axis as defined in the Unity Input Manager.
            value          : float,    # The value of change on the target axis from -1.0 to +1.0.
            numberOfFrames : int,      # The number of frames to hold the input for.
            timeout        : int = 30  # The number of seconds to wait for the command to be processed by the agent.
        ):
        '''
        <summary> Send arbitrary axis states to the game. Defaults to LEFT ALT/CTRL/SHIFT/WINDOWS(COMMAND) </summary>
        <param name="axisId" type="str"> The name of the target input axis as defined in the Unity Input Manager (Old). </param>
        <param name="value" type="float"> The value of change on the target axis from -1.0 to +1.0. </param>
        <param name="numberOfFrames" type="int"> The number of frames to hold the input for. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        # Move the horizontal axis to the right for 100 frames.
        await api.AxisPress(axisId="Horizontal", value=1.0, numberOfFrames=100)
        ```
        </example>
        '''

        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_InputManagerStateRequest(
                IdName = axisId,
                NumberOfFrames = numberOfFrames,
                InputType = 1,
                ChangeValue = value
                )
        )

        requestInfo : ProtocolObjects.RequestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_GenericResponse : Messages.Cmd_GenericResponse = await self.client.GetResult(requestInfo.RequestId)
        
        if cmd_GenericResponse.RC == Enums.ResponseCode.ERROR:
            raise Exception(cmd_GenericResponse.ErrorMessage)

    @requireClientConnectionAsync
    async def ButtonPress(self,
            buttonId       : str,
            numberOfFrames : int,
            timeout        : int = 30
        ):
        '''
        <summary> Send arbitrary button states to the game. Defaults to LEFT ALT/CTRL/SHIFT/WINDOWS(COMMAND) </summary>

        <param name="buttonId" type="str"> The name of the target input button as defined in the Unity Input Manager (Old). </param>
        <param name="numberOfFrames" type="int"> The number of frames to hold the input for. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        # Press the Jump button for 100 frames.
        await api.ButtonPress(buttonId="Jump", numberOfFrames=100)
        ```
        </example>
        '''

        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_InputManagerStateRequest(
                IdName = buttonId,
                NumberOfFrames = numberOfFrames,
                InputType = 0,
                ChangeValue = 0
            ),
        )
        requestInfo : ProtocolObjects.RequestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_GenericResponse : Messages.Cmd_GenericResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_GenericResponse.RC == Enums.ResponseCode.ERROR:
            raise Exception(cmd_GenericResponse.ErrorMessage)

    ## Return value overload
    @requireClientConnectionAsync
    async def CallMethod(self,
            hierarchyPath : str,
            methodName    : str,
            arguments     : list = None,
            timeout       : int = 30,
        ) -> type:
        '''
        <summary> Execute a method on an object </summary>

        <param name="hierarchyPath" type="str"> The HierarchyPath for a script attached to an object where the target method is defined. </param>
        <param name="methodName" type="str"> The name of the method to call. </param>
        <param name="arguments" type="list[any]"> The list of arguments to pass into the method. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <returns value="bool"> The return value of the method. </returns>

        <example>
        ```python
        # Set the color of the `Player` object to red using its method `SetColor`.
        await api.CallMethod(hierarchyPath="//*[@name='Player']/fn:component('Box')", methodName="SetColor", arguments=[255, 0, 0])
        ```
        </example>
        '''
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_CallMethodRequest(
                HierarchyPath = hierarchyPath,
                MethodName = methodName,
            )
        )

        if arguments:

            if not Serializers.IsBuiltin(arguments):
                raise NotImplementedError("Custom serializers are not yet supported for method calls.")
            msg.GDIOMsg.SetArguments(arguments, self.CustomSerializer)

        requestInfo : ProtocolObjects.RequestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_GetObjectValueResponse : Messages.Cmd_GetObjectValueResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_GetObjectValueResponse.RC != Enums.ResponseCode.OK:
            raise Exception(cmd_GetObjectValueResponse.ErrorMessage)

        if cmd_GetObjectValueResponse.Value is not None:
            return msgpack.unpackb(cmd_GetObjectValueResponse.Value)
        else:
            return None

    @requireClientConnectionAsync
    async def CaptureScreenshot(self,
            filename          : str,
            storeInGameFolder : bool = False,
            overwriteExisting : bool = False,
            timeout           : int = 30,
        ) -> str:
        '''
        <summary> Capture a screenshot of the currently running game. </summary>

        <param name="filename" type="str"> The absolute path and filename of the screen capture. </param>
        <param name="storeInGameFolder" type="bool"> Save the screenshot on the device the game is running on rather than returning it to the client. </param>
        <param name="overwriteExisting" type="bool"> Overwrite if the file already exists. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <returns value="str"> The path and filename of the screen capture. </returns>

        <example>
        ```python
        await api.CaptureScreenshot(filename="/path/to/file/screenshot.png")
        ```
        </example>
        '''
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_CaptureScreenshotRequest(
                StoreInGameFolder = storeInGameFolder,
                Filename = filename,
            )
        )

        requestInfo : ProtocolObjects.RequestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_CaptureScreenshotResponse : Messages.Cmd_CaptureScreenshotResponse = await asyncio.wait_for(self.client.GetResult(requestInfo.RequestId), timeout)
        
        if cmd_CaptureScreenshotResponse.RC == Enums.ResponseCode.ERROR:
            raise Exception(cmd_CaptureScreenshotResponse.ErrorMessage)

        # TODO: Im not sure if this works properly
        if storeInGameFolder:
            return cmd_CaptureScreenshotResponse.ImagePath

        if os.path.isfile(filename) and not overwriteExisting:
            raise OSError(f'Cannot save screenshot to {filename}, file already exists')
        
        # TODO: Relative paths
        with open(filename, 'wb') as f:
            f.write(cmd_CaptureScreenshotResponse.ImageData)

        return filename
        
    ## Float positions overload
    @requireClientConnectionAsync
    async def Click_XY(self,
            buttonId        : Enums.MouseButtons,
            x               : float,
            y               : float,
            clickFrameCount : int,
            timeout         : int = 30
        ):
        '''
        <summary> Clicks a mouse button at the target coordinates. </summary>

        <param name="buttonId" type="MouseButtons"> The button to click. </param>
        <param name="x" type="float"> The x position in screen coordinates at which to click. </param>
        <param name="y" type="float"> The y position in screen coordinates at which to click. </param>
        <param name="clickFrameCount" type="int"> The number of frames to click for. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        # Left click the screen at (100, 100) for 5 frames.
        await api.Click_XY(ButtonId=MouseButtons.Left, x=100, y=100, clickFrameCount=5)
        ```
        </example>
        '''
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_ClickRequest(
                MouseButtonId = int(buttonId),
                X = x,
                Y = y,
                FrameCount=clickFrameCount,
            ),
        )
        requestInfo : ProtocolObjects.RequestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_GenericResponse : Messages.Cmd_GenericResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_GenericResponse.RC != Enums.ResponseCode.OK:
            raise Exception(cmd_GenericResponse.ErrorMessage)
    

    ## Vector2 positions overload
    # TODO: Can probably combine this with the XY overload
    @requireClientConnectionAsync
    async def Click_Vec2(self,
            buttonId        : Enums.MouseButtons,
            position        : ProtocolObjects.Vector2,
            clickFrameCount : int,
            timeout         : int = 30
        ):
        '''
        <summary> Clicks a mouse button at the target coordinates. </summary>

        <param name="buttonId" type="MouseButtons"> The button to click. </param>
        <param name="position" type="Vector2"> The position in screen coordinates at which to click. </param>
        <param name="clickFrameCount" type="int"> The number of frames to click for. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        # Left click the screen at (100, 100) for 5 frames.
        await api.Click_XY(ButtonId=MouseButtons.Left, position=(100, 100), clickFrameCount=5)
        ```
        </example>
        '''
        await self.Click_XY(buttonId, position.x, position.y, clickFrameCount, timeout)

    ## Float positions overload
    @requireClientConnectionAsync
    async def ClickEx_XY(self,
            buttonId                : Enums.MouseButtons,
            x                       : float,
            y                       : float,
            clickFrameCount         : int,
            keys                    : list = None,
            keysNumberOfFrames      : int = 5,
            modifiers               : list = None,
            modifiersNumberOfFrames : int = 3,
            delayAfterModifiersMsec : int = 500,
            timeout                 : int = 30
        ):
        '''
        <summary> Clicks a mouse button at the target coordinates along with keypresses. </summary>

        <param name="buttonId" type="MouseButtons"> The button to click. </param>
        <param name="x" type="float"> The x position in screen coordinates at which to click. </param>
        <param name="y" type="float"> The y position in screen coordinates at which to click. </param>
        <param name="clickFrameCount" type="int"> The number of frames to click for. </param>
        <param name="keys" type="list[KeyCode]"> The list of keys to press while clicking. </param>
        <param name="keysNumberOfFrames" type="int"> The number of frames to hold the keys for. </param>
        <param name="modifiers" type="list[KeyCode]"> The list of modifier keys to press while clicking. </param>
        <param name="modifiersNumberOfFrames" type="int"> The number of frames to hold the modifier keys for. </param>
        <param name="delayAfterModifiersMsec" type="int"> The number of milliseconds to wait after pressing the modifiers before clicking the keys. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        # Shift+Left click the screen at (100, 100) for 5 frames.
        await api.ClickEx_XY(buttonId=MouseButtons.Left, x=100, y=100, clickFrameCount=5, keys=[KeyCode.LShift], keysNumberOfFrames=5)
        ```
        </example>
        '''
        if keys != None or modifiers != None:
            await self.KeyPress(
                keys,
                keysNumberOfFrames + clickFrameCount,
                modifiers,
                modifiersNumberOfFrames + clickFrameCount,
                delayAfterModifiersMsec,
                timeout
            )
            msg = ProtocolObjects.ProtocolMessage(
                ClientUID = self.client.ClientUID,
                GDIOMsg = Messages.Cmd_ClickRequest(
                    MouseButtonId = int(buttonId),
                    X = x,
                    Y = y,
                    FrameCount = clickFrameCount,
                ),
            )
            requestInfo : ProtocolObjects.RequestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_GenericResponse : Messages.Cmd_GenericResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_GenericResponse.RC != Enums.ResponseCode.OK:
            raise Exception(cmd_GenericResponse.ErrorMessage)

    ## Vector2 positions overload
    async def ClickEx_Vec2(self,
            buttonId                : Enums.MouseButtons,
            position                : ProtocolObjects.Vector2,
            clickFrameCount         : int,
            keys                    : list = None,
            keysNumberOfFrames      : int = 5,
            modifiers               : list = None,
            modifiersNumberOfFrames : int = 3,
            delayAfterModifiersMsec : int = 500,
            timeout                 : int = 30
        ):
        '''
        <summary> Clicks a mouse button at the target coordinates along with keypresses. </summary>

        <param name="buttonId" type="MouseButtons"> The button to click. </param>
        <param name="position" type="Vector2"> The position in screen coordinates at which to click. </param>
        <param name="clickFrameCount" type="int"> The number of frames to click for. </param>
        <param name="keys" type="list[KeyCode]"> The list of keys to press while clicking. </param>
        <param name="keysNumberOfFrames" type="int"> The number of frames to hold the keys for. </param>
        <param name="modifiers" type="list[KeyCode]"> The list of modifier keys to press while clicking. </param>
        <param name="modifiersNumberOfFrames" type="int"> The number of frames to hold the modifier keys for. </param>
        <param name="delayAfterModifiersMsec" type="int"> The number of milliseconds to wait after pressing the modifiers before clicking the keys. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        # Shift+Left click the screen at (100, 100) for 5 frames.
        await api.ClickEx_XY(buttonId=MouseButtons.Left, position=(100, 100), clickFrameCount=5, keys=[KeyCode.LShift], keysNumberOfFrames=5)
        ```
        </example>
        '''
        await self.ClickEx_XY(buttonId, position.x, position.y, clickFrameCount, keys, keysNumberOfFrames, modifiers, modifiersNumberOfFrames, delayAfterModifiersMsec, timeout)
    
    @requireClientConnectionAsync
    async def ClickObject(self,
            buttonId            : Enums.MouseButtons,
            hierarchyPath       : str,
            frameCount          : int,
            cameraHierarchyPath : str = None,
            timeout             : int = 30
        ):
        '''
        <summary> Clicks a mouse button at the position of the target object. </summary>

        <param name="buttonId" type="MouseButtons"> The button to click. </param>
        <param name="hierarchyPath" type="str"> The hierarchy path of the object to click. </param>
        <param name="frameCount" type="int"> The number of frames to click for. </param>
        <param name="cameraHierarchyPath" type="str"> The hierarchy path of the camera to use to find the object. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        # Left click the screen at the position of the `Player` object for 5 frames.
        await api.ClickObject(buttonId=MouseButtons.Left, hierarchyPath="//*[@name='Player']", frameCount=5)
        ```
        </example>
        '''
        
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_ClickObjectRequest(
                MouseButtonId = int(buttonId),
                HierarchyPath = hierarchyPath,
                FrameCount = frameCount,
                CameraHierarchyPath = cameraHierarchyPath,
            )
        )
        requestInfo : ProtocolObjects.RequestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_GenericResponse : Messages.Cmd_GenericResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_GenericResponse.RC != Enums.ResponseCode.OK:
            raise Exception(cmd_GenericResponse.ErrorMessage)

    @requireClientConnectionAsync
    async def ClickObjectEx(self,
            buttonId                : Enums.MouseButtons,
            hierarchyPath           : str,
            frameCount              : int,
            cameraHierarchyPath     : str = None,
            keys                    : list = None,
            keysNumberOfFrames      : int = 5,
            modifiers               : list = None,
            modifiersNumberOfFrames : int = 3,
            delayAfterModifiersMsec : int = 500,
            timeout                 : int = 30
        ):
        '''
        <summary> Clicks a mouse button at the position of the target object along with keypresses. </summary>

        <param name="buttonId" type="MouseButtons"> The button to click. </param>
        <param name="hierarchyPath" type="str"> The hierarchy path of the object to click. </param>
        <param name="frameCount" type="int"> The number of frames to click for. </param>
        <param name="cameraHierarchyPath" type="str"> The hierarchy path of the camera to use to find the object. </param>
        <param name="keys" type="list"> The keys to press. </param>
        <param name="keysNumberOfFrames" type="int"> The number of frames to hold the keys for. </param>
        <param name="modifiers" type="list"> The modifiers to press. </param>
        <param name="modifiersNumberOfFrames" type="int"> The number of frames to hold the modifiers for. </param>
        <param name="delayAfterModifiersMsec" type="int"> The number of milliseconds to wait after pressing the modifiers. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        # Shift+Left click the screen at the position of the `Player` object for 5 frames.
        await api.ClickObjectEx(buttonId=MouseButtons.Left, hierarchyPath="//*[@name='Player']", frameCount=5, keys=[KeyCode.LShift], keysNumberOfFrames=5)
        ```
        </example>
        '''
        if keys != None or modifiers != None:
            await self.KeyPress(keys, keysNumberOfFrames + frameCount, modifiers, modifiersNumberOfFrames + frameCount, delayAfterModifiersMsec, timeout)
        
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_ClickObjectRequest(
                MouseButtonId = int(buttonId),
                HierarchyPath = hierarchyPath,
                FrameCount = frameCount,
                CameraHierarchyPath = cameraHierarchyPath,
            )
        )
        requestInfo : ProtocolObjects.RequestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_GenericResponse : Messages.Cmd_GenericResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_GenericResponse.RC != Enums.ResponseCode.OK:
            raise Exception(cmd_GenericResponse.ErrorMessage)
            
    async def Connect(self,
            hostname           : str = '127.0.0.1', # The hostname of the device running the target game.
            port               : int = 19734,       # The port that the target Gamedriver agent is configured to use.
            autoplay           : bool = False,      # Start the game automatically within the Unity Editor.
            timeout            : int = 30,          # The number of seconds to wait for the command to be processed by the agent.

            _reader : asyncio.StreamReader = None, # TEMP
            _writer : asyncio.StreamWriter = None, # TEMP
        ) -> bool:
        '''
        <summary> Connects to an agent at the target hostname and port. </summary>

        <param name="hostname" type="str"> The hostname of the device running the target game. </param>
        <param name="port" type="int"> The port that the target Gamedriver agent is configured to listen on. </param>
        <param name="autoplay" type="bool"> Start the game automatically within the Unity Editor. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <returns value="bool"> True if nothing went wrong while trying to connect; Otherwise an exception is thown </returns>

        <example>
        ```python
        api = ApiClient()
        if await api.Connect(hostname="localhost", port=19734):
            print("Connected!")
        ```
        </example>
        '''
        # Try to connect to the target game.
        try:
            if autoplay:
                logging.debug("Looking for an editor to use for autoplay..")
                islistening = self._VerifyEditorInstance(hostname, timeout)
                if len(islistening) == 0:
                    raise Exception("No compatible game found on the specified hostname.")

                logging.debug(f"Autoplaying on the editor instance at {hostname}:{AUTOPLAY_DEFAULT_PORT}")

                # This uses the socket module becuase I don't know how to use the asyncio module for UDP.
                UDPsend(hostname, AUTOPLAY_DEFAULT_PORT, 'agent|startplay')

            self.client = Client(hostname, port, timeout)
            connected = await (self.client.Connect(internalComms=False, reader=_reader, writer=_writer))
            if not connected:
                raise Exception('Failed to connect to the game')

        # If any exception is thrown,
        except Exception as inner:
            # throw a wrapper exception and trace back to the inner exception.
            raise Exception(f'Failed to connect to {hostname}:{port}') from inner

        # If no exception is thrown
        else:
            # and connection details haven't been saved yet,
            if not self.gameConnectionDetails:
                
                # save the connection details that the client recieved.
                await asyncio.wait_for(self._WaitForConnectionDetails(), timeout)

        # No exceptions thrown; return success.
        return True

    async def _WaitForConnectionDetails(self):
        logging.debug("Waiting for connection details...")

        while self.client.GCD == None:
            await asyncio.sleep(0)

        logging.debug(f"Saving connection details {self.client.GCD}")
        self.gameConnectionDetails = self.client.GCD
    
    ## Regex overload
    '''
    async def Connect(self) -> None:
        raise NotImplementedError
        return
    '''

    @requireClientConnectionAsync
    async def DisableHooks(self, hookingObject : Enums.HookingObject = Enums.HookingObject.ALL, timeout : int = 30):
        '''
        <summary> Disables the ability to preform the target input type from the ApiClient. </summary>

        <param name="HookingObject" type="str"> The input type to disable. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        
        # Disable Mouse Hooks
        await api.DisableHooks(hookingObject=HookingObject.MOUSE)

        # Disable Gamepad Hooks
        await api.DisableHooks(hookingObject=HookingObject.GAMEPAD)

        # or just disable everything at once
        await api.DisableHooks(hookingObject=HookingObject.ALL)
        ```
        </example>
        '''
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_ChangeHookStatusRequest(
                KeyboardHooksStatus = True if (hookingObject & Enums.HookingObject.KEYBOARD) <= 0 else False,
                MouseHooksStatus = True if (hookingObject & Enums.HookingObject.MOUSE) <= 0 else False,
                TouchHooksStatus = True if (hookingObject & Enums.HookingObject.TOUCHINPUT) <= 0 else False,
                GamepadHooksStatus = True if (hookingObject & Enums.HookingObject.GAMEPAD) <= 0 else False,
                BitChanged = int(hookingObject)
            ),
        )

        requestInfo : ProtocolObjects.RequestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_GenericResponse : Messages.Cmd_GenericResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_GenericResponse.RC != Enums.ResponseCode.OK:
            raise Exception(cmd_GenericResponse.ErrorMessage)

    @requireClientConnectionAsync
    async def DisableObjectCaching(self, timeout : int = 30):
        '''
        <summary> Disables object caching of objects for HierarchyPath resolution. </summary>

        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        await api.DisableObjectCaching()
        ```
        </example>
        '''
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_ChangeObjectResolverCacheStateRequest(
                STATE = False
            )
        )

        requestInfo : ProtocolObjects.RequestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_GenericResponse : Messages.Cmd_GenericResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_GenericResponse.RC != Enums.ResponseCode.OK:
            raise Exception(cmd_GenericResponse.ErrorMessage)

    async def Disconnect(self):
        '''
        <summary> Disconnects from the agent. </summary>

        <example>
        ```python
        await api.Disconnect()
        ```
        </example>
        '''
        # If the client isn't connected,
        if not self.client:
            # theres no need to disconnect.
            return

        ## TODO: CLEANUP
        self.gameConnectionDetails = None

        await self.client.Disconnect()

    ## Float positions overload
    @requireClientConnectionAsync
    async def DoubleClick_XY(self,
            buttonId : Enums.MouseButtons,
            x : float,
            y : float,
            clickFrameCount : int,
            timeout : int = 30
        ):
        '''
        <summary> Double-clicks a mouse button at the target coordinates. </summary>

        <param name="buttonId" type="MouseButtons"> The button to click. </param>
        <param name="x" type="float"> The x position to click at. </param>
        <param name="y" type="float"> The y position to click at. </param>
        <param name="clickFrameCount" type="int"> The number of frames to click for. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        # Double-click the left mouse button at (500, 500)
        await api.DoubleClick_XY(buttonId=MouseButtons.LEFT, x=500, y=500, clickFrameCount=5)
        ```
        </example>
        '''
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_ClickRequest(
                MouseButtonId = int(buttonId),
                X = x,
                Y = y,
                FrameCount = clickFrameCount,
                IsDoubleClick = True
            )
        )

        requestInfo : ProtocolObjects.RequestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_GenericResponse : Messages.Cmd_GenericResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_GenericResponse.RC != Enums.ResponseCode.OK:
            raise Exception(cmd_GenericResponse.ErrorMessage)
    
    ## Vector2 positions overload
    async def DoubleClick_Vec2(self,
            buttonId : Enums.MouseButtons,
            position : ProtocolObjects.Vector2,
            clickFrameCount : int,
            timeout : int = 30
        ):
        '''
        <summary> Double-clicks a mouse button at the target coordinates. </summary>

        <param name="buttonId" type="MouseButtons"> The button to click. </param>
        <param name="position" type="Vector2"> The position to click at. </param>
        <param name="clickFrameCount" type="int"> The number of frames to click for. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        # Double-click the left mouse button at (500, 500)
        await api.DoubleClick_XY(buttonId=MouseButtons.LEFT, position=(500, 500), clickFrameCount=5)
        ```
        </example>
        '''
        await self.DoubleClick_XY(buttonId, position.x, position.y, clickFrameCount, timeout)

    ## Float positions overload
    @requireClientConnectionAsync
    async def DoubleClickEx_XY(self,
            buttonId : Enums.MouseButtons,
            x : float,
            y : float,
            clickFrameCount : int,
            keys : list = None,
            keysNumberOfFrames : int = 5,
            modifiers : list = None,
            modifiersNumberOfFrames : int = 3,
            delayAfterModifiersMsec : int = 500,
            timeout : int = 30
        ):
        '''
        <summary> Double-clicks the mouse at the target coordinates. </summary>

        <param name="buttonId" type="MouseButtons"> The button to click. </param>
        <param name="x" type="float"> The x position to click at. </param>
        <param name="y" type="float"> The y position to click at. </param>
        <param name="clickFrameCount" type="int"> The number of frames to click. </param>
        <param name="keys" type="list"> The list of keys to press. </param>
        <param name="keysNumberOfFrames" type="int"> The number of frames to press the keys. </param>
        <param name="modifiers" type="list"> The list of modifiers to press. </param>
        <param name="modifiersNumberOfFrames" type="int"> The number of frames to press the modifiers. </param>
        <param name="delayAfterModifiersMsec" type="int"> The number of milliseconds to wait after pressing the modifiers. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        # Double-click the left mouse button at (500, 500) while pressing Shift and Control
        await api.DoubleClickEx_XY(buttonId=MouseButtons.LEFT, x=500, y=500, clickFrameCount=5, keys=[KeyCode.SHIFT, KeyCode.CONTROL], keysNumberOfFrames=5)
        ```
        </example>
        '''
        if (keys != None) or (modifiers != None):
            await self.KeyPress(keys, keysNumberOfFrames, modifiers, modifiersNumberOfFrames, delayAfterModifiersMsec, timeout)

        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_ClickRequest(
                MouseButtonId = int(buttonId),
                X = x,
                Y = y,
                FrameCount = clickFrameCount,
                IsDoubleClick = True
            )
        )

        requestInfo : ProtocolObjects.RequestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_GenericResponse : Messages.Cmd_GenericResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_GenericResponse.RC != Enums.ResponseCode.OK:
            raise Exception(cmd_GenericResponse.ErrorMessage)
    
    ## Vector2 positions overload
    async def DoubleClickEx_Vec2(self,
            buttonId : Enums.MouseButtons,
            position : ProtocolObjects.Vector2,
            clickFrameCount : int,
            keys : list = None,
            keysNumberOfFrames : int = 5,
            modifiers : list = None,
            modifiersNumberOfFrames : int = 3,
            delayAfterModifiersMsec : int = 500,
            timeout : int = 30
        ):
        '''
        <summary> Double-clicks the mouse at the target coordinates. </summary>

        <param name="buttonId" type="MouseButtons"> The button to click. </param>
        <param name="position" type="Vector2"> The position to click at. </param>
        <param name="clickFrameCount" type="int"> The number of frames to click. </param>
        <param name="keys" type="list"> The list of keys to press. </param>
        <param name="keysNumberOfFrames" type="int"> The number of frames to press the keys. </param>
        <param name="modifiers" type="list"> The list of modifiers to press. </param>
        <param name="modifiersNumberOfFrames" type="int"> The number of frames to press the modifiers. </param>
        <param name="delayAfterModifiersMsec" type="int"> The number of milliseconds to wait after pressing the modifiers. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        # Double-click the left mouse button at (500, 500) while pressing Shift and Control
        await api.DoubleClickEx_Vec2(buttonId=MouseButtons.LEFT, position=Vector2(500, 500), clickFrameCount=5, keys=[KeyCode.SHIFT, KeyCode.CONTROL], keysNumberOfFrames=5)
        ```
        </example>
        '''
        await self.DoubleClickEx_XY(buttonId, position.x, position.y, clickFrameCount, keys, keysNumberOfFrames, modifiers, modifiersNumberOfFrames, delayAfterModifiersMsec, timeout)

    ## Float positions overload
    @requireClientConnectionAsync
    async def DoubleClickObject(self,
            buttonId : Enums.MouseButtons,
            hierarchyPath : str,
            frameCount : int,
            timeout : int = 30
        ):
        '''
        <summary> Double-clicks the mouse at the target coordinates. </summary>

        <param name="buttonId" type="MouseButtons"> The button to click. </param>
        <param name="hierarchyPath" type="str"> The hierarchy path of the object to click. </param>
        <param name="frameCount" type="int"> The number of frames to click. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        # Double-click the position of the `Player` object
        await api.DoubleClickObject(buttonId=MouseButtons.LEFT, hierarchyPath="//*[@name='Player']", 5)
        ```
        </example>
        '''
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_ClickObjectRequest(
                MouseButtonId = int(buttonId),
                HierarchyPath = hierarchyPath,
                FrameCount = frameCount,
                IsDoubleClick = True
            )
        )

        requestInfo : ProtocolObjects.RequestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_GenericResponse : Messages.Cmd_GenericResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_GenericResponse.RC != Enums.ResponseCode.OK:
            raise Exception(cmd_GenericResponse.ErrorMessage)

    @requireClientConnectionAsync
    async def DoubleClickObjectEx(self,
            buttonId : Enums.MouseButtons,
            hierarchyPath : str,
            clickFrameCount : int,
            keys : list = None,
            keysNumberOfFrames : int = 5,
            modifiers : list = None,
            modifiersNumberOfFrames : int = 3,
            delayAfterModifiersMsec : int = 500,
            timeout : int = 30
        ):
        '''
        <summary> Double-clicks the mouse at the target coordinates. </summary>

        <param name="buttonId" type="MouseButtons"> The button to click. </param>
        <param name="hierarchyPath" type="str"> The hierarchy path of the object to click. </param>
        <param name="clickFrameCount" type="int"> The number of frames to click. </param>
        <param name="keys" type="list"> The list of keys to press. </param>
        <param name="keysNumberOfFrames" type="int"> The number of frames to press the keys. </param>
        <param name="modifiers" type="list"> The list of modifiers to press. </param>
        <param name="modifiersNumberOfFrames" type="int"> The number of frames to press the modifiers. </param>
        <param name="delayAfterModifiersMsec" type="int"> The number of milliseconds to wait after pressing the modifiers. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        # Double-click the position of the `Player` object while pressing Shift and Control
        await api.DoubleClickObjectEx(buttonId=MouseButtons.LEFT, hierarchyPath="//*[@name='Player']", clickFrameCount=5, keys=[KeyCode.SHIFT, KeyCode.CONTROL], keysNumberOfFrames=5)
        ```
        </example>
        '''
        if keys != None or modifiers != None:
            await self.KeyPress(keys, keysNumberOfFrames + clickFrameCount, modifiers, modifiersNumberOfFrames + clickFrameCount, delayAfterModifiersMsec, timeout)
        
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_ClickObjectRequest(
                MouseButtonId = int(buttonId),
                HierarchyPath = hierarchyPath,
                FrameCount = clickFrameCount,
                IsDoubleClick = True
            )
        )
        requestInfo : ProtocolObjects.RequestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_GenericResponse : Messages.Cmd_GenericResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_GenericResponse.RC != Enums.ResponseCode.OK:
            raise Exception(cmd_GenericResponse.ErrorMessage)

    @requireClientConnectionAsync
    async def EnableHooks(self, hookingObject : Enums.HookingObject = Enums.HookingObject.ALL, timeout : int = 30):
        '''
        <summary> Enables the given hooking object. </summary>

        <param name="hookingObject" type="HookingObject"> The hooking object to enable. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        api = ApiClient()
        await api.Connect()
        
        # Enable Mouse Hooks
        await api.EnableHooks(hookingObject=HookingObject.MOUSE)

        # Enable Gamepad Hooks
        await api.EnableHooks(hookingObject=HookingObject.GAMEPAD)

        # or just enable everything at once
        await api.EnableHooks(hookingObject=HookingObject.ALL)
        ```
        </example>
        '''
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_ChangeHookStatusRequest(
                KeyboardHooksStatus = (hookingObject & Enums.HookingObject.KEYBOARD) > 0,
                MouseHooksStatus = (hookingObject & Enums.HookingObject.MOUSE) > 0,
                TouchHooksStatus = (hookingObject & Enums.HookingObject.TOUCHINPUT) > 0,
                GamepadHooksStatus = (hookingObject & Enums.HookingObject.GAMEPAD) > 0,
                BitChanged = int(hookingObject)
            ),
        )

        requestInfo : ProtocolObjects.RequestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_GenericResponse : Messages.Cmd_GenericResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_GenericResponse.RC != Enums.ResponseCode.OK:
            raise Exception(cmd_GenericResponse.ErrorMessage)

    @requireClientConnectionAsync
    async def EnableObjectCaching(self, timeout : int = 30):
        '''
        <summary> Enables caching of objects for hierarchyPath resolution. </summary>

        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        await api.EnableObjectCaching()
        ```
        </example>
        '''
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_ChangeObjectResolverCacheStateRequest(
                STATE = True
            )
        )

        requestInfo : ProtocolObjects.RequestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_GenericResponse : Messages.Cmd_GenericResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_GenericResponse.RC != Enums.ResponseCode.OK:
            raise Exception(cmd_GenericResponse.ErrorMessage)
    
    @requireClientConnectionAsync
    async def FlushObjectLookupCache(self, timeout : int = 30):
        '''
        <summary> Flushes the object lookup cache. </summary>

        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        await api.FlushObjectLookupCache()
        ```
        </example>
        '''
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_FlushCacheRequest()
        )

        requestInfo : ProtocolObjects.RequestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_GenericResponse : Messages.Cmd_GenericResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_GenericResponse.RC != Enums.ResponseCode.OK:
            raise Exception(cmd_GenericResponse.ErrorMessage)

    @requireClientConnection
    def GetConnectedGameDetails(self) -> ProtocolObjects.GameConnectionDetails:
        '''
        <summary> Gets the details of the connected game. </summary>

        <returns value="GameConnectionDetails"> The details of the connected game. </returns>

        <example>
        ```python
        details = await api.GetConnectedGameDetails()
        print(details.GameName)
        ```
        </example>
        '''
        return self.gameConnectionDetails

    @requireClientConnectionAsync
    async def GetLastFPS(self, timeout = 30) -> float:
        '''
        <summary> Gets the last reported FPS value. </summary>

        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <returns value="float"> The last FPS value. </returns>

        <example>
        ```python
        fps = await api.GetLastFPS()
        print(fps)
        ```
        </example>
        '''
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_GetStatisticsRequest()
        )

        requestInfo : ProtocolObjects.RequestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_GenericResponse : Messages.Cmd_GenericResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_GenericResponse.RC != Enums.ResponseCode.OK:
            return -1

        return cmd_GenericResponse.ReturnedValues['FPS']
        

    @requireClientConnection
    def GetNextCollisionEvent(self, eventId) -> ProtocolObjects.Collision:
        '''
        <summary> Gets the next collision event. </summary>

        <returns value="Collision"> The next collision event. </returns>

        <example>
        ```python
        # Begin recieving collision events that occur on the `Player` object
        monitorid = await api.RegisterCollisionMonitor(hierarchyPath="//*[@name='Player']")

        # Get the next collision event that occurs on the `Player` object
        collision = await api.GetNextCollisionEvent(eventId=monitorid)

        # Stop recieving collision events on the `Player` object
        await api.UnregisterCollisionMonitor(hierarchyPath="//*[@name='Player']")
        ```
        </example>
        '''
        nextEvent = self.client.GetNextEvent(eventId)
        if nextEvent is None:
            return None
        return nextEvent

    @requireClientConnectionAsync
    async def GetObjectDistance(self,
            objectA_HierarchyPath : str,
            objectB_HierarchyPath : str,
            timeout : int = 30
        ) -> float:
        '''
        <summary> Gets the distance between two objects. </summary>

        <param name="objectA_HierarchyPath" type="str"> The hierarchy path of the first object. </param>
        <param name="objectB_HierarchyPath" type="str"> The hierarchy path of the second object. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <returns value="float"> The distance between the objects. </returns>

        <example>
        ```python
        distance = await api.GetObjectDistance(objectA_HierarchyPath="//*[@name='ObjectA']", objectB_HierarchyPath="//*[@name='ObjectB']")
        print(distance)
        ```
        </example>
        '''

        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_ObjectDistanceRequest(
                ObjectA_HierarchyPath = objectA_HierarchyPath,
                ObjectB_HierarchyPath = objectB_HierarchyPath
            )
        )
        requestInfo : ProtocolObjects.RequestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_GetObjectValueResponse : Messages.Cmd_GetObjectValueResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_GetObjectValueResponse.RC != Enums.ResponseCode.OK:
            raise Exception('Failed getting object distance')

        if cmd_GetObjectValueResponse.Value is not None:
            return msgpack.unpackb(cmd_GetObjectValueResponse.Value)
        else:
            # TODO: More pedantic return value; something like float-min
            return None

    @requireClientConnectionAsync
    async def GetObjectFieldValue(self,
            hierarchyPath : str,
            timeout : int = 30
        ):
        '''
        <summary> Gets the value of a field on an object. </summary>

        <param name="t" type="type"> The type of the field. </param>
        <param name="hierarchyPath" type="str"> The hierarchy path of the target field. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <returns value="t"> The value of the field. </returns>

        <example>
        ```python
        # Check to see if the `Player` object is active in the scene
        value = await api.GetObjectFieldValue(t=bool, hierachyPath="//Player[@name='Player']/@active")
        print(value)
        ```
        </example>
        '''

        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_GetObjectValueRequest(
                HierarchyPath = hierarchyPath,

                # This probably doesn't work like this
                #TypeFullName = Enums.CSTypeFullName[t.__name__]
            )
        )
        requestInfo : ProtocolObjects.RequestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_GetObjectValueResponse : Messages.Cmd_GetObjectValueResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_GetObjectValueResponse.RC != Enums.ResponseCode.INFORMATION:
            return None

        if cmd_GetObjectValueResponse.Value is not None:
            return msgpack.unpackb(cmd_GetObjectValueResponse.Value)

        return cmd_GetObjectValueResponse.directObject

    @requireClientConnectionAsync
    async def GetObjectFieldValueByName(self,
            hierarchyPath : str,
            fieldName : str,
            timeout : int = 30
        ):
        '''
        <summary> Gets the value of a field on an object by field name. </summary>

        <param name="hierarchyPath" type="str"> The hierarchy path of the object. </param>
        <param name="fieldName" type="str"> The name of the field. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <returns value="t"> The value of the field. </returns>

        <example>
        ```python
        # Check to see if the `Player` object is active in the scene
        value = await api.GetObjectFieldValueByName(hierarchyPath="//*[@name='Player']", fieldName="active")
        print(value)
        ```
        </example>
        '''
        
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_GetObjectValueRequest(
                HierarchyPath = hierarchyPath,
                ObjectFieldOrPropertyName = fieldName
            )
        )
        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_GetObjectValueResponse : Messages.Cmd_GetObjectValueResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_GetObjectValueResponse.RC != Enums.ResponseCode.INFORMATION:
            return None

        if cmd_GetObjectValueResponse.Value is not None:
            return msgpack.unpackb(cmd_GetObjectValueResponse.Value)

        return cmd_GetObjectValueResponse.directObject


    @requireClientConnectionAsync
    async def GetObjectList(self, timeout : int = 30) -> list:
        '''
        <summary> Gets the list of objects in the scene. </summary>

        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <returns value="list"> The list of objects in the scene. </returns>

        <example>
        ```python
        objects = await api.GetObjectList()
        print(objects)
        ```
        </example>
        '''
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_GetObjectListRequest()
        )

        requestInfo : ProtocolObjects.RequestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_GenericResponse : Messages.Cmd_GenericResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_GenericResponse.RC != Enums.ResponseCode.INFORMATION:
            raise Exception(cmd_GenericResponse.ErrorMessage)

        return cmd_GenericResponse.Objects


    async def GetObject(self,
            hierarchyPath : str,
            timeout : int = 30
        ) -> object:

        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_GetGameObjectRequest(
                HierarchyPath = hierarchyPath,
            )
        )
        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_GetObjectListResponse : Messages.Cmd_GetObjectListResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_GetObjectListResponse.RC != Enums.ResponseCode.INFORMATION:
            raise Exception(cmd_GetObjectListResponse.ErrorMessage)

        return cmd_GetObjectListResponse.Objects[0]

    @requireClientConnectionAsync
    async def GetObjectPosition(self,
            hierarchyPath : str,
            coordSpace : Enums.CoordinateConversion = Enums.CoordinateConversion.NONE,
            cameraHierarchyPath : str = None,
            timeout : int = 30
        ) -> ProtocolObjects.Vector3:
        '''
        <summary> Gets the position of an object. </summary>

        <param name="hierarchyPath" type="str"> The hierarchy path of the object. </param>
        <param name="coordSpace" type="CoordinateConversion"> The coordinate space to use. </param>
        <param name="cameraHierarchyPath" type="str"> The hierarchy path of the camera to use. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <returns value="Vector3"> The position of the object. </returns>

        <example>
        ```python
        # Get the position of the `Player` object in screen space
        position = await api.GetObjectPosition(hierarchyPath="//*[@name='Player']", coordSpace=CoordinateConversion.SCREEN_SPACE)
        print(position)
        ```
        </example>
        '''

        cameraHierarchyPath = '' if cameraHierarchyPath is None else cameraHierarchyPath

        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_GetObjectPositionRequest(
                ObjectHierarchyPath = hierarchyPath,
                CameraHierarchyPath = cameraHierarchyPath,
                SpaceConversion = coordSpace
            )
        )
        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_VectorResponse : Messages.Cmd_VectorResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_VectorResponse.RC != Enums.ResponseCode.INFORMATION:
            raise Exception(cmd_VectorResponse.ErrorMessage)

        return cmd_VectorResponse.Value3

    @requireClientConnectionAsync
    async def GetSceneName(self, timeout : int = 30) -> str:
        '''
        <summary> Gets the name of the active scene. </summary>

        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <returns value="str"> The name of the active scene. </returns>

        <example>
        ```python
        sceneName = await api.GetSceneName()
        print(sceneName)
        ```
        </example>
        '''
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_GetSceneNameRequest()
        )

        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        response = await self.client.GetResult(requestInfo.RequestId)

        if response.RC != Enums.ResponseCode.INFORMATION:
            raise Exception(response.ErrorMessage)

        return response.InformationMessage

    """
    def GetVersionString(self) -> str:
        '''
        <summary> (**Not Implemented**) Gets the version string of the agent. </summary>

        <returns value="str"> The version string of the agent. </returns>

        <example>
        ```python
        api = ApiClient()
        print(api.GetVersionString())
        ```
        </example>
        '''
        raise NotImplementedError
    """

    @requireClientConnectionAsync
    async def KeyPress(self,
            keys : list,
            numberOfFrames : int,
            modifiers : list = None,
            modifiersNumberOfFrames : int = 3,
            delayAfterModifiersMsec : int = 500,
            timeout : int = 30
        ):
        '''
        <summary> Presses a key. </summary>

        <param name="keys" type="list"> The keys to press. </param>
        <param name="numberOfFrames" type="int"> The number of frames to press the keys. </param>
        <param name="modifiers" type="list"> The modifiers to press. </param>
        <param name="modifiersNumberOfFrames" type="int"> The number of frames to press the modifiers. </param>
        <param name="delayAfterModifiersMsec" type="int"> The delay after pressing the modifiers. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        await api.KeyPress(keys=[KeyCode.A, KeyCode.B, KeyCode.C], numberOfFrames=10)
        ```
        </example>
        '''
        if modifiers != None:
            modifiersMessage = ProtocolObjects.ProtocolMessage(
                ClientUID = self.client.ClientUID,
                GDIOMsg = Messages.Cmd_KeyPressRequest(
                    KeyCodes = [int(key) for key in modifiers],
                    NumberOfFrames = numberOfFrames + modifiersNumberOfFrames,
                )
            )
            modifiersRequestInfo = await asyncio.wait_for(self.client.SendMessage(modifiersMessage), timeout)
            await self.Wait(delayAfterModifiersMsec)

        keysMessage = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_KeyPressRequest(
                KeyCodes = [int(key) for key in keys],
                NumberOfFrames = numberOfFrames,
            )
        )
        keysRequestInfo = await asyncio.wait_for(self.client.SendMessage(keysMessage), timeout)

    def Launch(self, filepath : str, arguments : str = None):
        '''
        <summary> Launches an executable. </summary>

        <param name="filename" type="str"> The filename of the process to launch. </param>
        <param name="arguments" type="str"> The arguments to launch the process with. </param>

        <returns value="bool"> The process object. </returns>

        <example>
        ```python
        game_process = api.Launch(filepath="/path/to/executable.exe", arguments="arg1 arg2")

        api.TerminateGame(game_process)
        ```
        </example>
        '''
        
        args = arguments if arguments else ''
        path = os.path.abspath(filepath)
        proc = subprocess.Popen([path, args])

        return proc

    @requireClientConnectionAsync
    async def LoadScene(self, sceneName : str, timeout : int = 30):
        '''
        <summary> Loads a scene by name. </summary>

        <param name="sceneName" type="str"> The name of the scene to load. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        await api.LoadScene(sceneName="SceneA")
        ```
        </example>
        '''
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_LoadSceneRequest(
                SceneName = sceneName
            )
        )

        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        #response = await self.client.GetResult(requestInfo.RequestId)
        
    def _VerifyEditorInstance(self, hostname : str, timeout = 30) -> list:
        '''

        '''
        ReceiveClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ReceiveClient.bind(('', AUTOPLAY_RECEIVE_PORT))
        ReceiveClient.settimeout(timeout)

        SendClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        SendClient.connect((hostname, AUTOPLAY_DEFAULT_PORT))
        payload = bytes(f'agent|getgameinfo|{AUTOPLAY_RECEIVE_PORT}', 'utf-8')
        SendClient.send(payload)
        SendClient.close()

        data, addr = ReceiveClient.recvfrom(1024)
        ReceiveClient.close()

        return data

    @requireClientConnectionAsync
    async def MouseDrag(self,
            button : Enums.MouseButtons,
            dx : float,
            dy : float,
            frameCount : float,
            ox : float = None,
            oy : float = None,
            waitForEmptyInput : bool = True,
            timeout : int = 30
        ):
        '''
        <summary> Drags the mouse. </summary>

        <param name="button" type="MouseButtons"> The button to drag with. </param>
        <param name="dx" type="float"> The amount to drag the mouse in the X direction. </param>
        <param name="dy" type="float"> The amount to drag the mouse in the Y direction. </param>
        <param name="frameCount" type="float"> The number of frames to drag the mouse. </param>
        <param name="ox" type="float"> The offset X of the mouse. </param>
        <param name="oy" type="float"> The offset Y of the mouse. </param>
        <param name="waitForEmptyInput" type="bool"> Whether or not to wait for the mouse to be empty before continuing. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        # Drag the mouse to (10, 10) over the next 100 frames
        await api.MouseDrag(button=MouseButtons.Left, dx=10, dy=10, frameCount=100)
        ```
        </example>
        '''
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_MouseDragRequest(
                Destination = ProtocolObjects.Vector2(dx, dy),
                Origin = ProtocolObjects.Vector2(ox, oy),
                FrameCount = frameCount,
                ButtonId = button
            )
        )
        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        response = await self.client.GetResult(requestInfo.RequestId)
        if waitForEmptyInput:
            self.WaitForEmptyInput(timeout)
        if response.RC != Enums.ResponseCode.OK:
            raise Exception(response.ErrorMessage)

    @requireClientConnectionAsync
    async def MouseMoveToObject(self,
            objectHierarchyPath : str,
            frameCount : float,
            waitForObject : bool = True,
            waitForEmptyInput : bool = True,
            timeout : int = 60
        ):
        '''
        <summary> Moves the mouse to an object. </summary>

        <param name="objectHierarchyPath" type="str"> The object hierarchy path of the object to move to. </param>
        <param name="frameCount" type="float"> The number of frames to move the mouse. </param>
        <param name="waitForObject" type="bool"> Whether or not to wait for the object to be found. </param>
        <param name="waitForEmptyInput" type="bool"> Whether or not to wait for the mouse to be empty before continuing. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        # Move the mouse to the object 'Box' over the next 100 frames
        await api.MouseMoveToObject(objectHierarchyPath="//*[@name='Box']", frameCount=100)
        ```
        </example>
        '''
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_MouseMoveToObjectRequest(
                ObjectHierarchyPath = objectHierarchyPath,
                Timeout = timeout,
                FrameCount = frameCount,
                WaitForObject = waitForObject
            )
        )
        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        response = await self.client.GetResult(requestInfo.RequestId)
        if waitForEmptyInput:
            self.WaitForEmptyInput(timeout)
        if response.RC != Enums.ResponseCode.OK:
            raise Exception(response.ErrorMessage)

    @requireClientConnectionAsync
    async def MouseMoveToPoint(self,
            dx : float,
            dy : float,
            frameCount : float,
            ox : float = None,
            oy : float = None,
            waitForEmptyInput : bool = True,
            timeout : int = 30
        ):
        '''
        <summary> Moves the mouse to an absolute point on screen. </summary>

        <param name="dx" type="float"> The amount to move the mouse in the X direction. </param>
        <param name="dy" type="float"> The amount to move the mouse in the Y direction. </param>
        <param name="frameCount" type="float"> The number of frames to move the mouse. </param>
        <param name="ox" type="float"> The offset X of the mouse. </param>
        <param name="oy" type="float"> The offset Y of the mouse. </param>
        <param name="waitForEmptyInput" type="bool"> Whether or not to wait for the mouse to be empty before continuing. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        # Move the mouse to (10, 10) over the next 100 frames
        await api.MouseMoveToPoint(dx=10, dy=10, frameCount=100)
        ```
        </example>
        '''
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_MouseMoveRequest(
                Destination = ProtocolObjects.Vector2(dx, dy),
                Origin = ProtocolObjects.Vector2(ox, oy),
                FrameCount = frameCount
            )
        )
        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        response = await self.client.GetResult(requestInfo.RequestId)
        if waitForEmptyInput:
            self.WaitForEmptyInput(timeout)
        if response.RC != Enums.ResponseCode.OK:
            raise Exception(response.ErrorMessage)

    @requireClientConnectionAsync
    async def NavAgentMoveToPoint(self,
            navAgent_HierarchyPath : str,
            dx : float,
            dy : float,
            waitForMoveToComplete : bool = True,
            timeout : int = 30
        ):
        '''
        <summary> Moves the nav agent to a point. </summary>

        <param name="navAgent_HierarchyPath" type="str"> The object hierarchy path of the nav agent to move. </param>
        <param name="dx" type="float"> The amount to move the nav agent in the X direction. </param>
        <param name="dy" type="float"> The amount to move the nav agent in the Y direction. </param>
        <param name="waitForMoveToComplete" type="bool"> Whether or not to wait for the nav agent to reach the destination. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <returns value="bool"> True if successful, False otherwise. </returns>

        <example>
        ```python
        # Move the nav agent to (100, 100)
        await api.NavAgentMoveToPoint(navAgent_HierarchyPath="//*[@name='Agent']", dx=100, dy=100)
        ```
        </example>
        '''
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_NavAgentMoveToPointRequest(
                NavAgentHierarchyPath = navAgent_HierarchyPath,
                Point = ProtocolObjects.Vector2(dx, dy),
            )
        )
        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        response = await self.client.GetResult(requestInfo.RequestId)

        if response.RC != Enums.ResponseCode.OK:
            raise Exception(response.ErrorMessage)

        return True

    @requireClientConnectionAsync
    async def Raycast(self,
            raycastPoint : ProtocolObjects.Vector3,
            cameraHierarchyPath : str = None,
            timeout : int = 30
        ) -> list:
        '''
        <summary> Perform a Raycast to a point to find out what is in that position. </summary>

        <param name="raycastPoint" type="Vector3"> The raycast point. </param>
        <param name="cameraHierarchyPath" type="str"> The hierarchy path of the camera to use for the raycast. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <returns value="list"> The raycast results. </returns>

        <example>
        ```python
        point = Vector3(100, 100, 100)
        raycastResults = await api.Raycast(raycastPoint=point)
        ```
        </example>
        '''
        cameraHierarchyPath = '' if cameraHierarchyPath is None else cameraHierarchyPath

        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_RaycastRequest(
                CameraHierarchyPath = cameraHierarchyPath,
                RaycastPoint = raycastPoint
            )
        )
        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        response = await self.client.GetResult(requestInfo.RequestId)
        if response.RC != Enums.ResponseCode.OK:
            raise Exception(response.ErrorMessage)

        return response.RaycastResults

    @requireClientConnectionAsync
    async def RegisterCollisionMonitor(self,
            hierarchyPath : str,
            timeout : int = 30    
        ) -> str:
        '''
        <summary> Registers a collision monitor to recieve collision events on an object. </summary>

        <param name="hierarchyPath" type="str"> The hierarchy path of the object to monitor. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <returns value="str"> The Id of the collision monitor </returns>

        <example>
        ```python
        # Begin recieving collision events that occur on the `Player` object
        monitorid = await api.RegisterCollisionMonitor(hierarchyPath="//*[@name='Player']")

        # Wait for a collision event
        collision = await api.WaitForCollisionEvent(eventId=monitorid)

        # Stop recieving collision events on the `Player` object
        await api.UnregisterCollisionMonitor(hierarchyPath="//*[@name='Player']")
        ```
        </example>
        '''
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_RegisterCollisionMonitorRequest(
                HierarchyPath = hierarchyPath
            )
        )
        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        response = await self.client.GetResult(requestInfo.RequestId)
        if response.RC != Enums.ResponseCode.OK:
            raise Exception(response.ErrorMessage)

        return str(response.ReturnedValues['Id'])

    @requireClientConnectionAsync
    async def RotateObject_Quaternion(self,
            hierarchyPath : str,
            quaternion : ProtocolObjects.Vector4,
            waitForObject : bool = True,
            timeout : int = 30
        ):
        '''
        <summary> Rotates an object using a quaternion. </summary>

        <param name="hierarchyPath" type="str"> The hierarchy path of the object to rotate. </param>
        <param name="quaternion" type="Vector4"> The quaternion to rotate the object by. </param>
        <param name="waitForObject" type="bool"> Whether or not to wait for the object to rotate. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        # Rotate the `box` object by a quaternion of (0, 0, 0, 1)
        await api.RotateObject_Quaternion(hierarchyPath="//*[@name='Box']", quaternion=Vector4(0, 0, 0, 1))
        ```
        </example>
        '''
        request = Messages.Cmd_RotateRequest(
                HierarchyPath = hierarchyPath,
                Quant = quaternion,
                Timeout = timeout,
                WaitForObject = waitForObject
        )
        await self._RotateObject(hierarchyPath, request, waitForObject, timeout)

    @requireClientConnectionAsync
    async def RotateObject_Euler(self,
            hierarchyPath : str,
            euler : ProtocolObjects.Vector3,
            relativeTo : Enums.Space = Enums.Space.Self,
            waitForObject : bool = True,
            timeout : int = 30
        ):
        '''
        <summary> Rotates an object using euler angles. </summary>

        <param name="hierarchyPath" type="str"> The hierarchy path of the object to rotate. </param>
        <param name="euler" type="Vector3"> The Euler angles to rotate the object by. </param>
        <param name="relativeTo" type="Space"> The space to rotate the object in. </param>
        <param name="waitForObject" type="bool"> Whether or not to wait for the object to rotate. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        # Rotate the `box` object by 10 degrees around the X axis
        # then rotate it by 20 degrees around the new relative Y axis
        # then rotate it by 30 degrees around the new relative Z axis
        await api.RotateObject_Euler(hierarchyPath="//*[@name='Box']", euler=Vector3(10, 20, 30))
        ```
        </example>
        '''
        request = Messages.Cmd_RotateRequest(
            HierarchyPath = hierarchyPath,
            Euler = euler,
            RelativeTo = relativeTo,
            Timeout = timeout,
            WaitForObject = waitForObject
        )

        await self._RotateObject(hierarchyPath, request, waitForObject, timeout)

    @requireClientConnectionAsync
    async def RotateObject_AxisAngle(self,
            hierarchyPath : str,
            xAngle : float,
            yAngle : float,
            zAngle : float,
            relativeTo : Enums.Space = Enums.Space.Self,
            waitForObject : bool = True,
            timeout : int = 30
        ):
        '''
        <summary> Rotates an object using absolute axis angles. </summary>

        <param name="hierarchyPath" type="str"> The hierarchy path of the object to rotate. </param>
        <param name="xAngle" type="float"> The X angle to rotate the object by. </param>
        <param name="yAngle" type="float"> The Y angle to rotate the object by. </param>
        <param name="zAngle" type="float"> The Z angle to rotate the object by. </param>
        <param name="relativeTo" type="Space"> The space to rotate the object in. </param>
        <param name="waitForObject" type="bool"> Whether or not to wait for the object to rotate. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        # Rotate the `box` object by 10 degrees around the X axis, 20 degrees around the Y axis, and 30 degrees around the Z axis
        await api.RotateObject_AxisAngle(hierarchyPath="//*[@name='Box']", xAngle=10, yAngle=20, zAngle=30)
        ```
        </example>
        '''
        request = Messages.Cmd_RotateRequest(
            HierarchyPath = hierarchyPath,
            XAngle = xAngle,
            YAngle = yAngle,
            ZAngle = zAngle,
            RelativeTo = relativeTo,
            Timeout = timeout,
            WaitForObject = waitForObject
        )
        await self._RotateObject(hierarchyPath, request, waitForObject, timeout)

    @requireClientConnectionAsync
    async def _RotateObject(self,
            HierarchyPath : str,
            request : Messages.Cmd_RotateRequest,
            waitForObject : bool = True,
            timeout : int = 30
        ):
        '''

        '''
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = request
        )

        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        response = await self.client.GetResult(requestInfo.RequestId)
        if response.RC != Enums.ResponseCode.OK:
            raise Exception(response.ErrorMessage)

    @requireClientConnectionAsync
    async def SetInputFieldText(self,
            hierarchyPath : str,
            text : str,
            waitForObject : bool = True,
            timeout : int = 30
        ):
        '''
        <summary> Sets the text of an InputField or TMP_InputField. </summary>

        <param name="hierarchyPath" type="str"> The hierarchy path of the input field. </param>
        <param name="text" type="str"> The text to set the input field to. </param>
        <param name="waitForObject" type="bool"> Whether or not to wait for the object to be set. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        # Set the text of the `InputField` object to `Hello World`
        await api.SetInputFieldText(hierarchyPath="//FilterInputTxt[@name='TextMeshPro InputField']", text="Hello World")
        ```
        </example>
        '''
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_SetInputFieldTextRequest(
                HierarchyPath = hierarchyPath,
                Text = text,
                Timeout = timeout,
                WaitForObject = waitForObject
            )
        )
        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        response = await self.client.GetResult(requestInfo.RequestId)
        if response.RC != Enums.ResponseCode.OK:
            raise Exception(response.ErrorMessage)

    @requireClientConnectionAsync
    async def SetObjectFieldValue(
            self,
            hierarchyPath : str,
            fieldName : str,
            value : object,
            waitForObject : bool = True,
            timeout : int = 30
        ):
        '''
        <summary> Set the field or property of an object. </summary>

        <param name="hierarchyPath" type="str"> The hierarchy path of the object. </param>
        <param name="fieldName" type="str"> The name of the field or property to set. </param>
        <param name="value" type="object"> The value to set the field or property to. </param>
        <param name="waitForObject" type="bool"> If True, wait for the object to exist if it doesn't. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        # Set the `Text` field of the `TextMeshPro` object to `Hello World`
        await api.SetObjectFieldValue(hierarchyPath="/Untagged[@name='Canvas']/FilterInputTxt[@name='TextMeshPro InputField']/fn:component('TMPro.TMP_InputField')", fieldName="text", value="string:Hello World")
        ```
        '''

        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_SetObjectValueRequest(
                HierarchyPath = hierarchyPath,
                ObjectFieldOrPropertyName = fieldName,
                WaitForObject = waitForObject,
                Timeout = timeout,
            )
        )

        if Serializers.IsBuiltin(value):
            msg.GDIOMsg.SerializedObjectType = type (value)
            msg.GDIOMsg.Value = msgpack.pack(value)
            msg.GDIOMsg.CustomSerialization = False
            
        else:
            msg.GDIOMsg.SerializedObjectType = type (value)
            msg.GDIOMsg.Value = self.CustomSerializer.Pack(value)
            msg.GDIOMsg.CustomSerialization = True

        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        response = await self.client.GetResult(requestInfo.RequestId)

        if response.RC != Enums.ResponseCode.OK:
            raise Exception(response.ErrorMessage)


    @requireClientConnectionAsync
    async def Tap_XY(self,
            x : float,
            y : float,
            tapCount : int = 1,
            frameCount : int = 5,
            timeout : int = 30
        ):
        '''
        <summary> Tap the handheld device at the target position. </summary>

        <param name="x" type="float"> The X coordinate to tap. </param>
        <param name="y" type="float"> The Y coordinate to tap. </param>
        <param name="tapCount" type="int"> The number of times to tap the object. </param>
        <param name="frameCount" type="int"> The number of frames to tap the object. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        # Tap the screen once at (100, 100)
        await api.Tap_XY(x=100, y=100)
        ```
        </example>
        '''
        
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_TapRequest(
                X = x,
                Y = y,
                FrameCount = frameCount,
                TapCount = tapCount
            )
        )
        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        response = await self.client.GetResult(requestInfo.RequestId)
        
        if response.RC != Enums.ResponseCode.OK:
            raise Exception(response.ErrorMessage)

    @requireClientConnectionAsync
    async def Tap_Vec2(self,
            position : ProtocolObjects.Vector2,
            tapCount : int = 1,
            frameCount : int = 5,
            timeout : int = 30
        ):
        '''
        <summary> Tap the handheld device at the target position. </summary>

        <param name="position" type="Vector2"> The position to tap. </param>
        <param name="tapCount" type="int"> The number of times to tap the object. </param>
        <param name="frameCount" type="int"> The number of frames to tap the object. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <returns value="bool"> True if successful, False otherwise. </returns>

        <example>
        ```python
        # Tap the screen once at (100, 100)
        await api.Tap_Vec2(position=Vector2(100, 100))
        ```
        </example>
        '''
        await self.Tap_XY(position.X, position.Y, tapCount, frameCount, timeout)

    @requireClientConnectionAsync
    async def TapObject(self,
            hierarchyPath : str,
            tapCount : int = 1,
            frameCount : int = 5,
            cameraHierarchyPath : str = None,
            timeout : int = 30
        ):
        '''
        <summary> Tap the handheld device at the target position. </summary>

        <param name="hierarchyPath" type="str"> The hierarchy path of the object to tap. </param>
        <param name="tapCount" type="int"> The number of times to tap the object. </param>
        <param name="frameCount" type="int"> The number of frames to tap the object. </param>
        <param name="cameraHierarchyPath" type="str"> The hierarchy path of the camera to use when tapping. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        # Tap the screen once at the position of the `TextMeshPro InputField` object
        await api.TapObject(hierarchyPath="//FilterInputTxt[@name='TextMeshPro InputField']")
        ```
        </example>
        '''

        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_TapRequest(
                HierarchyPath = hierarchyPath,
                FrameCount = frameCount,
                TapCount = tapCount,
                CameraHierarchyPath = cameraHierarchyPath
            )
        )

        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        response = await self.client.GetResult(requestInfo.RequestId)
        if response.RC != Enums.ResponseCode.OK:
            raise Exception(response.ErrorMessage)

    @requireClientConnectionAsync
    async def TerminateGame(self, process):
        '''
        <summary> Terminates the game. </summary>

        <example>
        ```python
        game_process = api.Launch("/path/to/executable.exe", "arg1 arg2")

        api.TerminateGame(process=game_process)
        ```
        </example>
        '''
        process.kill()

    def StopEditorPlay(self):
        '''
        <summary> Stops Play Mode in the Unity Editor. </summary>

        <example>
        ```python
        api.StopEditorPlay()
        ```
        </example>
        '''
        hostname = '127.0.0.1'
        if self.CurrentPlayDetails is not None:
            hostname = self.CurrentPlayDetails.Addr
        logging.debug(f'Stopping editor play on {hostname}')
        UDPsend(hostname, AUTOPLAY_DEFAULT_PORT, 'agent|stopplay')

    def ToggleEditorPause(self):
        '''
        <summary> Toggles Pause in the Unity Editor while Play Mode is active. </summary>

        <returns value="bool"> True if successful, False otherwise. </returns>

        <example>
        ```python
        api.ToggleEditorPause()
        ```
        </example>
        '''
        hostname = '127.0.0.1'
        if self.CurrentPlayDetails is not None:
            hostname = self.CurrentPlayDetails.Addr
        logging.debug(f'Toggling editor pause on {hostname}')
        UDPsend(hostname, AUTOPLAY_DEFAULT_PORT, 'agent|togglepause')

    def ToggleEditorPlay(self):
        '''
        <summary> Toggles Play Mode in the Unity Editor. </summary>

        <returns value="bool"> True if successful, False otherwise. </returns>

        <example>
        ```python
        api.ToggleEditorPlay()
        ```
        </example>
        '''
        hostname = '127.0.0.1'
        if self.CurrentPlayDetails is not None:
            hostname = self.CurrentPlayDetails.Addr
        logging.debug(f'Toggling editor play on {hostname}')
        UDPsend(hostname, AUTOPLAY_DEFAULT_PORT, 'agent|toggleplay')

    @requireClientConnectionAsync
    async def TouchInput(self,
            x1 : float,
            y1 : float,
            x2 : float,
            y2 : float,
            fingerId : int,
            tapCount : int = 1,
            frameCount : int = 5,
            waitForEmptyInput : bool = True,
            radius : float = 20,
            pressure : float = 1,
            altitudeAngle : float = 0,
            azmulthAngle : float = 0,
            maximumPossiblePressure : float = 1,
            timeout : int = 30
        ):
        '''
        <summary> Touches an object. </summary>

        <param name="x1" type="float"> The X coordinate of the first touch point. </param>
        <param name="y1" type="float"> The Y coordinate of the first touch point. </param>
        <param name="x2" type="float"> The X coordinate of the second touch point. </param>
        <param name="y2" type="float"> The Y coordinate of the second touch point. </param>
        <param name="fingerId" type="int"> The finger ID. </param>
        <param name="tapCount" type="int"> The number of times to tap the object. </param>
        <param name="frameCount" type="int"> The number of frames to tap the object. </param>
        <param name="waitForEmptyInput" type="bool"> Whether to wait for an empty input. </param>
        <param name="radius" type="float"> The radius of the touch. </param>
        <param name="pressure" type="float"> The pressure of the touch. </param>
        <param name="altitudeAngle" type="float"> The altitude angle of the touch. </param>
        <param name="azmulthAngle" type="float"> The azmulth angle of the touch. </param>
        <param name="maximumPossiblePressure" type="float"> The maximum possible pressure of the touch. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        # Performs a single touch input from 0,0 to 100, 100 with a single "finger" over a duration of 50 frames
        await api.TouchInput(x1=0, y1=0, x2=100, y2=100, fingerId=0, tapCount=1, frameCount=50)
        ```
        </example>
        '''
        request = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_TouchEventRequest(
                StartPosition=ProtocolObjects.Vector2(X=x1, Y=y1),
                DestinationPosition=ProtocolObjects.Vector2(X=x2, Y=y2),
                FrameCount = frameCount,
                TapCount = tapCount,
                Radius = radius,
                Pressure = pressure,
                AltitudeAngle = altitudeAngle,
                AzmulthAngle = azmulthAngle,
                FingerId = fingerId,            
                MaximumPossiblePressure = maximumPossiblePressure
            )
        )
        requestInfo = await asyncio.wait_for(self.client.SendMessage(request), timeout)
        response = await self.client.GetResult(requestInfo.RequestId)
        if waitForEmptyInput:
            self.WaitForEmptyInput(timeout)
        if response.RC != Enums.ResponseCode.OK:
            raise Exception(response.ErrorMessage)

    
    @requireClientConnectionAsync
    async def UnregisterCollisionMonitor(self,
            hierarchyPath : str,
            timeout : int = 30
        ):
        '''
        <summary> Unregisters a collision monitor to stop recieving collision events on an object. </summary>

        <param name="hierarchyPath" type="str"> The hierarchy path of the object to monitor. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the command to be processed by the agent. </param>

        <example>
        ```python
        # Begin recieving collision events that occur on the `Player` object
        monitorid = await api.RegisterCollisionMonitor(hierarchyPath="//*[@name='Player']")

        # Wait for a collision event
        collision = await api.WaitForCollisionEvent(eventId=monitorid)

        # Stop recieving collision events on the `Player` object
        await api.UnregisterCollisionMonitor(hierarchyPath="//*[@name='Player']")
        ```
        </example>
        '''
        request = Messages.Cmd_UnregisterCollisionMonitorRequest(
            HierarchyPath = hierarchyPath,
        )
        requestInfo = await asyncio.wait_for(self.client.SendMessage(request), timeout)
        response = await self.client.GetResult(requestInfo.RequestId)
        if response.RC != Enums.ResponseCode.OK:
            raise Exception(response.ErrorMessage)

    async def Wait(self, miliseconds : int) -> None:
        '''
        <summary> Waits for a specified number of miliseconds. </summary>

        <param name="miliseconds" type="int"> The number of miliseconds to wait. </param>

        <example>
        ```python
        # Waits for 1 second
        await api.Wait(miliseconds=1000)
        ```
        </example>
        '''
        time.sleep(miliseconds * 0.001)

    @requireClientConnectionAsync
    async def WaitForEmptyInput(self, timeout : int = 30):
        '''
        <summary> Waits for an empty input event. </summary>

        <param name="timeout" type="int"> The number of seconds to wait for the event to be processed </param>

        <example>
        ```python
        await api.WaitForEmptyInput()
        ```
        </example>
        '''
        await asyncio.wait_for(self.client.WaitForEmptyInput(), timeout)

    @requireClientConnectionAsync
    async def WaitForCollisionEvent(self,
            eventId : str,
            timeout : int = 30
        ) -> ProtocolObjects.Collision:
        '''
        <summary> Waits for a new collision event. </summary>

        <param name="eventId" type="str"> The Id of the collision monitor to wait for an event from. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the event to be processed </param>

        <returns value="Collision"> The collision event. </returns>

        <example>
        ```python
        # Begin recieving collision events that occur on the `Player` object
        monitorid = await api.RegisterCollisionMonitor(hierarchyPath="//*[@name='Player']")

        # Wait for a collision event
        await api.WaitForCollisionEvent(eventId=monitorid)

        # Stop recieving collision events on the `Player` object
        await api.UnregisterCollisionMonitor(hierarchyPath="//*[@name='Player']")
        ```
        </example>
        '''
        nextEvent =  await asyncio.wait_for(self.client.WaitForNextEvent(eventId), timeout)
        if nextEvent is None:
            return None
        return nextEvent

    @requireClientConnectionAsync
    async def WaitForObject(self,
            hierarchyPath : str,
            timeout : int = 30
        ) -> bool:
        '''
        <summary> Waits for an object to exist. </summary>

        <param name="hierarchyPath" type="str"> The hierarchy path of the object to wait for. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the object to exist. </param>

        <returns value="bool"> True if the object is found, False otherwise. </returns>

        <example>
        ```python
        # Waits for the `Key` object to exist
        await api.WaitForObject(hierarchyPath="//*[@name='Key']")
        ```
        </example>
        '''
        
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_WaitForObjectRequest(
                HierarchyPath = hierarchyPath,
                Timeout = timeout
            )
        )

        requestInfo : Messages.RequestInfo = await self.client.SendMessage(msg)
        cmd_WaitForObjectResponse : Messages.Cmd_WaitForObjectResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_WaitForObjectResponse.RC == Enums.ResponseCode.OK and cmd_WaitForObjectResponse.ObjectResolutionResult == Enums.OBJECT_RESOLUTION.OBJECT_FOUND:
            return True

        return False

    @requireClientConnectionAsync
    async def waitForObjectValue(self,
            hierarchyPath : str,
            fieldOrPropertyName : str,
            #waitForObject : bool = True,
            value = None,
            timeout : int = 30
        ) -> bool:
        '''
        <summary> Wait for an object to exist and have a specific value for a specified field/property. </summary>

        <param name="hierarchyPath" type="str"> The hierarchy path of the object to wait for. </param>
        <param name="fieldOrPropertyName" type="str"> The name of the field/property to wait for. </param>
        <param name="value" type="str"> The value to wait for. </param>
        <param name="timeout" type="int"> The number of seconds to wait for the object to exist </param>

        <returns value="bool"> True if the object is found and has the specified value, False otherwise. </returns>

        <example>
        ```python
        # Waits for the `Button` object to exist and have a value of `True` for the `isPressed` property
        await api.WaitForObject(hierarchyPath="//*[@name='Button']/fn:component('ButtonScript')", fieldOrPropertyName="isPressed", value=True)
        ```
        </example>
        '''

        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_WaitForObjectValueRequest(
                HierarchyPath = hierarchyPath,
                FieldOrPropertyName = fieldOrPropertyName,
                Timeout = timeout,
            )
        )

        # This series of conditionals doesnt really make sense yet
        if Serializers.IsBuiltin(value):
            msg.GDIOMsg.SerializedObjectType = value.__class__
            msg.GDIOMsg.Value = msgpack.packb(value)
            msg.GDIOMsg.CustomSerialization = False

        else:
            msg.GDIOMsg.SerializedObjectType = value.__class__
            msg.GDIOMsg.Value = self.CustomSerializer.Pack(value)
            msg.GDIOMsg.CustomSerialization = True

        requestInfo : Messages.RequestInfo = await self.client.SendMessage(msg)
        cmd_WaitForObjectValueResponse : Messages.Cmd_WaitForObjectValueResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_WaitForObjectValueResponse.RC == Enums.ResponseCode.OK and cmd_WaitForObjectValueResponse.ObjectResolutionResult == Enums.OBJECT_RESOLUTION.OBJECT_FOUND:
            return True

        return False