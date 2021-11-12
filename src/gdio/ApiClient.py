from .Client import Client
from . import ProtocolObjects, Messages, Exceptions, Enums

from functools import wraps

import os
import asyncio, socket
import time, datetime


AUTOPLAY_DEFAULT_PORT = 11002

def requireClientConnection(function):
    @wraps(function)
    async def inner(*args, **kwargs):
        if args[0].client == None:
            raise Exceptions.ClientNotConnectedError
        await function(*args, **kwargs)
    return inner

class ApiClient:
    def __init__(self):
        
        # Defined in self.Connect().
        self.client = None
        self.CurrentPlayDetails = None
        self.gameConnectionDetails = None

    @requireClientConnection
    async def AxisPress(self,
            axisId         : str,      # The name of the target input axis as defined in the Unity Input Manager.
            value          : float,    # The value of change on the target axis from -1.0 to +1.0.
            numberOfFrames : int,      # The number of frames to hold the input for.
            timeout        : int = 30  # The number of seconds to wait for the command to be recieved by the agent.
        ) -> bool:

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

        return (cmd_GenericResponse.RC == Enums.ResponseCode.OK)

    @requireClientConnection
    async def ButtonPress(self,
            buttonId       : str,      # The name of the target input button as defined in the Unity Input Manager.
            numberOfFrames : int,      # The number of frames to hold the input for.
            timeout        : int = 30  # The number of seconds to wait for the command to be recieved by the agent.
        ) -> bool:

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

        return (cmd_GenericResponse.RC == Enums.ResponseCode.OK)
    
    ## Void overload
    @requireClientConnection
    async def CallMethod_Void(self,
            hierarchyPath : str,         # The HierarchyPath for an object and the script attached to it.
            methodName    : str,         # The name of the method to call within the script.
            arguments     : list = None, # TODO: The list of arguments to pass into the method.
            timeout       : int = 30,    # The number of seconds to wait for the command to be recieved by the agent.
        ) -> None:

        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_CallMethodRequest(
                HierarchyPath = hierarchyPath,
                MethodName = methodName,
            )
        )

        # TODO: Set and serialize the method's arguments.
        if arguments:
            msg.GDIOMsg.SetArguments(arguments)

        requestInfo : ProtocolObjects.RequestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_GenericResponse : Messages.Cmd_GenericResponse = await self.client.GetResult(requestInfo.RequestId)

        # If the response is an error, warning, or information message,
        if cmd_GenericResponse.RC != 0:
            # throw an exception containing the response data.
            raise Exception(cmd_GenericResponse.ErrorMessage)

        # The message didn't timeout, and the response was OK; return
        return

    ## Return value overload
    @requireClientConnection
    async def CallMethod(self,
            t             : type,
            hierarchyPath : str,      # The HierarchyPath for an object and the script attached to it.
            methodName    : str,      # The name of the method to call within the script.
            arguments     : list,     # TODO: The list of arguments to pass into the method.
            timeout       : int = 30, # The number of seconds to wait for the command to be recieved by the agent.
        ) -> None:

        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_CallMethodRequest(
                HierarchyPath = hierarchyPath,
                MethodName = methodName,
            )
        )

        # TODO: Set and serialize the method's arguments.
        msg.GDIOMsg.SetArguments(arguments)

        requestInfo : ProtocolObjects.RequestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_GenericResponse : Messages.Cmd_GenericResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_GenericResponse.RC != Enums.ResponseCode.OK:
            raise Exception(cmd_GenericResponse.ErrorMessage)

        return cmd_GenericResponse.ReturnValues

    @requireClientConnection
    async def CaptureScreenshot(self,
            filename          : str,          # The path and filename of the screen capture.
            storeInGameFolder : bool = False, # TODO: Save the screenshot on the device the game is running on rather than returning it to the client.
            overwriteExisting : bool = False, # Overwrite if the file already exists.
            timeout           : int = 30,     # The number of seconds to wait for the command to be recieved by the agent.
        ) -> str:

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

        # TODO: Im not sure this works properly
        if storeInGameFolder:
            return cmd_CaptureScreenshotResponse.ImagePath

        if os.path.isfile(filename) and not overwriteExisting:
            raise OSError(f'Cannot save screenshot to {filename}, file already exists')
        
        # TODO: Relative paths
        with open(filename, 'wb') as f:
            f.write(cmd_CaptureScreenshotResponse.ImageData)

        return filename
        
    ## Float positions overload
    @requireClientConnection
    async def Click_XY(self,
            buttonId        : Enums.MouseButtons,
            x               : float,
            y               : float,
            clickFrameCount : int,
            timeout         : int = 30
        ) -> bool:

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
            raise Exceptions.ClickObjectError(cmd_GenericResponse.ErrorMessage)

        return cmd_GenericResponse.RC == Enums.ResponseCode.OK
    

    ## Vector2 positions overload
    # TODO: Can probably combine this with the XY overload
    @requireClientConnection
    async def Click_Vec2(self,
            buttonId        : Enums.MouseButtons,
            position        : ProtocolObjects.Vector2,
            clickFrameCount : int,
            timeout         : int = 30
        ) -> bool:
        return self.Click_XY(buttonId, position.x, position.y, clickFrameCount, timeout)

    ## Float positions overload
    @requireClientConnection
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
        ) -> bool:
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
            raise Exceptions.ClickObjectError(cmd_GenericResponse.ErrorMessage)

        return cmd_GenericResponse.RC == Enums.ResponseCode.OK

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
        ) -> bool:
        return self.ClickEx_XY(buttonId, position.x, position.y, clickFrameCount, keys, keysNumberOfFrames, modifiers, modifiersNumberOfFrames, delayAfterModifiersMsec, timeout)
    
    @requireClientConnection
    async def ClickObject(self,
            buttonId            : Enums.MouseButtons,
            hierarchyPath       : str,
            frameCount          : int,
            cameraHierarchyPath : str = None,
            timeout             : int = 30
        ) -> bool:
        
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
            raise Exceptions.ClickObjectError(cmd_GenericResponse.ErrorMessage)


        return cmd_GenericResponse.RC == Enums.ResponseCode.OK

    @requireClientConnection
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
        ) -> bool:

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
            raise Exceptions.ClickObjectError(cmd_GenericResponse.ErrorMessage)


        return cmd_GenericResponse.RC == Enums.ResponseCode.OK
            
    # TODO: autoplay
    async def Connect(self,
            hostname           : str = '127.0.0.1',    # The hostname of the device running the target game.
            port               : int = 19734,          # The port that the target Gamedriver agent is configured to use.
            autoplay           : bool = False,         # TODO: Start the game automatically within the Unity Editor.
            timeout            : int = 30,             # The number of seconds to wait for the command to be recieved by the agent.
            autoPortResolution : bool = True,# TODO: Automatically resolve the port a Gamedriver Agent is running on.

            reader : asyncio.StreamReader = None, # TEMP
            writer : asyncio.StreamWriter = None, # TEMP
        ) -> None:

        # Try to connect to the target game.
        try:
            if autoplay:
                raise NotImplementedError("Autoplay is not yet implemented.")
                # TODO: ManageAutoPlay()
                autoPlayDetails = self.ManageAutoPlay(hostname)
                if len(autoPlayDetails) == 0:
                    raise Exceptions.AutoPlayError("No compatible game found on the specified hostname.")
                gameConnectionDetails = autoPlayDetails[0].GCD
                self.CurrentPlayDetails = autoPlayDetails[0]

                # This uses the socket module becuase I don't know how to use the asyncio module for UDP.
                UdpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                endPoint = (autoPlayDetails[0].Addr, AUTOPLAY_DEFAULT_PORT)
                UdpClient.sendto(bytes('agent|startplay'), endPoint)
                UdpClient.close()


            self.client = Client(hostname, port, timeout)

            if not await self.client.Connect(internalComms=False, reader=reader, writer=writer):
                raise Exceptions.FailedGameConnectionError('Failed to connect to the game')

        # If any exception is thrown,
        except Exception as inner:
            # throw a wrapper exception and trace back to the inner exception.
            raise Exceptions.FailedClientConnectionError(f'Failed to connect to {hostname}:{port}') from inner

        # If no exception is thrown
        else:
            # and connection details havent been saved yet,
            if self.gameConnectionDetails == None:
                # save the connection details that the client recieved.
                self.gameConnectionDetails = self.client.GCD

        # No exceptions thrown; return
        return
    
    ## Regex overload
    '''
    async def Connect(self) -> None:
        raise NotImplementedError
        return
    '''

    @requireClientConnection
    async def DisableHooks(self, hookingObject, timeout : int = 30) -> bool:

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
            raise Exceptions.ClickObjectError(cmd_GenericResponse.ErrorMessage)


        return cmd_GenericResponse.RC == Enums.ResponseCode.OK

    @requireClientConnection
    async def DisableObjectCaching(self, timeout : int = 30) -> bool:
            
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_ChangeObjectResolverCacheStateRequest(
                STATE = False
            )
        )

        requestInfo : ProtocolObjects.RequestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_GenericResponse : Messages.Cmd_GenericResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_GenericResponse.RC != Enums.ResponseCode.OK:
            raise Exceptions.ClickObjectError(cmd_GenericResponse.ErrorMessage)


        return cmd_GenericResponse.RC == Enums.ResponseCode.OK

    async def Disconnect(self) -> None:
        # If the client isn't connected,
        if not self.client:
            # theres no need to disconnect.
            return

        ## TODO: CLEANUP
        self._cleanup()
        self.gameConnectionDetails = None

        await self.client.Disconnect()

    ## Float positions overload
    @requireClientConnection
    async def DoubleClick_XY(self,
            buttonId : Enums.MouseButtons,
            x : float,
            y : float,
            clickFrameCount : int,
            timeout : int = 30
        ) -> bool:

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
            raise Exceptions.ClickObjectError(cmd_GenericResponse.ErrorMessage)

        return cmd_GenericResponse.RC == Enums.ResponseCode.OK
    
    ## Vector2 positions overload
    async def DoubleClick_Vec2(self,
            buttonId : Enums.MouseButtons,
            position : ProtocolObjects.Vector2,
            clickFrameCount : int,
            timeout : int = 30
        ) -> bool:
        return self.DoubleClick(buttonId, position.x, position.y, clickFrameCount, timeout)

    ## Float positions overload
    @requireClientConnection
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
        ) -> bool:

        if (keys != None) or (modifiers != None):
            self.KeyPress(keys, keysNumberOfFrames, modifiers, modifiersNumberOfFrames, delayAfterModifiersMsec, timeout)

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
            raise Exceptions.ClickObjectError(cmd_GenericResponse.ErrorMessage)

        return cmd_GenericResponse.RC == Enums.ResponseCode.OK
    
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
        ) -> bool:
        return self.DoubleClickEx(buttonId, position.x, position.y, clickFrameCount, keys, keysNumberOfFrames, modifiers, modifiersNumberOfFrames, delayAfterModifiersMsec, timeout)

    ## Float positions overload
    @requireClientConnection
    async def DoubleClickObject(self,
            buttonId : Enums.MouseButtons,
            hierarchyPath : str,
            frameCount : int,
            timeout : int = 30
        ) -> bool:

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
            raise Exceptions.ClickObjectError(cmd_GenericResponse.ErrorMessage)

        return cmd_GenericResponse.RC == Enums.ResponseCode.OK

    @requireClientConnection
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
        ) -> bool:

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
            raise Exceptions.ClickObjectError(cmd_GenericResponse.ErrorMessage)

        return cmd_GenericResponse.RC == Enums.ResponseCode.OK

    @requireClientConnection
    async def EnableHooks(self, hookingObject, timeout : int = 30) -> bool:

        # TODO: Hooking objects
        # NOTE: ATM, enables all hooking
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
            raise Exceptions.ClickObjectError(cmd_GenericResponse.ErrorMessage)

        return cmd_GenericResponse.RC == Enums.ResponseCode.OK

    @requireClientConnection
    async def EnableObjectCaching(self, timeout : int = 30) -> bool:

        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_ChangeObjectResolverCacheStateRequest(
                STATE = True
            )
        )

        requestInfo : ProtocolObjects.RequestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_GenericResponse : Messages.Cmd_GenericResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_GenericResponse.RC != Enums.ResponseCode.OK:
            raise Exceptions.ClickObjectError(cmd_GenericResponse.ErrorMessage)

        return cmd_GenericResponse.RC == Enums.ResponseCode.OK
    
    @requireClientConnection
    async def FlushObjectLookupCache(self, timeout : int = 30) -> bool:
            
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_FlushCacheRequest()
        )

        requestInfo : ProtocolObjects.RequestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_GenericResponse : Messages.Cmd_GenericResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_GenericResponse.RC != Enums.ResponseCode.OK:
            raise Exceptions.ClickObjectError(cmd_GenericResponse.ErrorMessage)

        return cmd_GenericResponse.RC == Enums.ResponseCode.OK

    @requireClientConnection
    async def GetConnectedGameDetails(self) -> ProtocolObjects.GameConnectionDetails:
        return self.gameConnectionDetails

    @requireClientConnection
    async def GetLastFPS(self, timeout=30) -> float:
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
    async def GetNextCollisionEvent(self) -> ProtocolObjects.Collision:
        raise NotImplementedError

    @requireClientConnection
    async def GetObjectDistance(self,
            objectA_HierarchyPath : str,
            objectB_HierarchyPath : str,
            timeout : int = 30
        ) -> float:
        # TODO : weird deserialization thingy at the end
        raise NotImplementedError

        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_ObjectDistanceRequest(
                ObjectAHierarchyPath = objectA_HierarchyPath,
                ObjectBHierarchyPath = objectB_HierarchyPath
            )
        )
        requestInfo : ProtocolObjects.RequestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_GenericResponse : Messages.Cmd_GenericResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_GenericResponse.RC != Enums.ResponseCode.OK:
            return -1

        return cmd_GenericResponse

    @requireClientConnection
    async def GetObjectFieldValue(self,
            t : type,
            hierarchyPath : str,
            timeout : int = 30
        ):
        # TODO : weird deserialization thingy at the end
        raise NotImplementedError
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_GetObjectValueRequest(
                HierarchyPath = hierarchyPath,

                # This probably doesn't work like this
                Type = t.__class__
            )
        )
        requestInfo : ProtocolObjects.RequestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_GenericResponse : Messages.Cmd_GenericResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_GenericResponse.RC != Enums.ResponseCode.OK:
            return -1

        return cmd_GenericResponse

    @requireClientConnection
    async def GetObjectFieldValueByName(self,
            hierarchyPath : str,
            fieldName : str,
            timeout : int = 30
        ):
        # TODO : weird deserialization thingy at the end
        raise NotImplementedError
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_GetObjectValueRequest(
                HierarchyPath = hierarchyPath,
                FieldName = fieldName
            )
        )
        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        response = await self.client.GetResult(requestInfo.RequestId)

        if response.RC != Enums.ResponseCode.OK:
            return -1

        return response


    @requireClientConnection
    async def GetObjectList(self, timeout : int = 30) -> bool:
            
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_GetObjectListRequest()
        )

        requestInfo : ProtocolObjects.RequestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        cmd_GenericResponse : Messages.Cmd_GenericResponse = await self.client.GetResult(requestInfo.RequestId)

        if cmd_GenericResponse.RC != Enums.ResponseCode.OK:
            raise Exceptions.ClickObjectError(cmd_GenericResponse.ErrorMessage)

        return cmd_GenericResponse.Objects

    @requireClientConnection
    async def GetObjectPosition(self,
            hierarchyPath : str,
            coordSpace : Enums.CoordinateConversion = Enums.CoordinateConversion.NONE,
            cameraHierarchyPath : str = None,
            timeout : int = 30
        ) -> ProtocolObjects.Vector3:
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_GetObjectPositionRequest(
                HierarchyPath = hierarchyPath,
                CameraHierarchyPath=cameraHierarchyPath,
                CoordSpace = coordSpace
            )
        )
        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        response = await self.client.GetResult(requestInfo.RequestId)
        if response.Value3 == None or response.RC != Enums.ResponseCode.INFORMATION:
            raise Exceptions.ObjectPositionError(response.ErrorMessage)

        return response.Value3

    @requireClientConnection
    async def GetSceneName(self, timeout : int = 30) -> bool:
            
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_GetSceneNameRequest()
        )

        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        response = await self.client.GetResult(requestInfo.RequestId)

        if response.RC != Enums.ResponseCode.INFORMATION:
            raise Exceptions.SceneNameError(response.ErrorMessage)

        return response.InformationMessage

    def GetVersionString(self) -> str:
        raise NotImplementedError
        return

    @requireClientConnection
    async def KeyPress(self,
            keys : list,
            numberOfFrames : int,
            modifiers : list = None,
            modifiersNumberOfFrames : int = 3,
            delayAfterModifiersMsec : int = 500,
            timeout : int = 30
        ) -> bool:

        if modifiers != None:
            modifiersMessage = ProtocolObjects.ProtocolMessage(
                ClientUID = self.client.ClientUID,
                GDIOMsg = Messages.Cmd_KeyPressRequest(
                    KeysCodes = [int(key) for key in modifiers],
                    NumberOfFrames = numberOfFrames + modifiersNumberOfFrames,
                )
            )
            modifiersRequestInfo = await asyncio.wait_for(self.client.SendMessage(modifiersMessage), timeout)
            self.Wait(delayAfterModifiersMsec)

        keysMessage = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_KeyPressRequest(
                KeyCodes = [int(key) for key in keys],
                NumberOfFrames = numberOfFrames,
            )
        )
        keysRequestInfo = await asyncio.wait_for(self.client.SendMessage(keysMessage), timeout)

        # No exceptions thrown; return True
        return True

    def Launch(self, filename : str, arguments : str = None):
        ## Not sure what this one does yet
        raise NotImplementedError

    @requireClientConnection
    async def LoadScene(self, sceneName : str, timeout : int = 30) -> bool:
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_LoadSceneRequest(
                SceneName = sceneName
            )
        )

        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        response = await self.client.GetResult(requestInfo.RequestId)
        
        return True

    def ManageAutoPlay(self, hostname : str) -> list:
        raise NotImplementedError

    @requireClientConnection
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
            raise Exceptions.InputRequestError(response.ErrorMessage)

        return True

    @requireClientConnection
    async def MouseMoveToObject(self,
            objectHierarchyPath : str,
            frameCount : float,
            waitForObject : bool = True,
            waitForEmptyInput : bool = True,
            timeout : int = 60
        ):
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
            raise Exceptions.InputRequestError(response.ErrorMessage)

        return True

    @requireClientConnection
    async def MouseMoveToPoint(self,
            dx : float,
            dy : float,
            frameCount : float,
            ox : float = None,
            oy : float = None,
            waitForEmptyInput : bool = True,
            timeout : int = 30
        ):
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
            raise Exceptions.InputRequestError(response.ErrorMessage)

        return True

    @requireClientConnection
    async def NavAgentMoveToPoint(self,
            navAgent_HierarchyPath : str,
            dx : float,
            dy : float,
            waitForMoveToComplete : bool = True,
            timeout : int = 30
        ):
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
            raise Exceptions.InputRequestError(response.ErrorMessage)

        return True

    @requireClientConnection
    async def Raycast(self,
            raycastPoint : ProtocolObjects.Vector3,
            cameraHierarchyPath : str,
            timeout : int = 30
        ) -> list:

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
            raise Exceptions.InputRequestError(response.ErrorMessage)

        return response.RaycastResults

    @requireClientConnection
    async def RegisterCollisionMonitor(self,
            HierarchyPath : str,
            timeout : int = 30    
        ):
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Messages.Cmd_RegisterCollisionMonitorRequest(
                HierarchyPath = HierarchyPath
            )
        )
        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        response = await self.client.GetResult(requestInfo.RequestId)
        if response.RC != Enums.ResponseCode.OK:
            raise Exception(response.ErrorMessage)

        return str(response.ReturnedValues['Id'])

    @requireClientConnection
    async def RotateObject_Quaternion(self,
            hierarchyPath : str,
            quaternion : ProtocolObjects.Vector4,
            waitForObject : bool = True,
            timeout : int = 30
        ):
        request = Messages.Cmd_RotateRequest(
                HierarchyPath = hierarchyPath,
                Quant = quaternion,
                Timeout = timeout,
                WaitForObject = waitForObject
        )
        return await self._RotateObject(hierarchyPath, request, waitForObject, timeout)

    @requireClientConnection
    async def RotateObject_Euler(self,
            hierarchyPath : str,
            euler : ProtocolObjects.Vector3,
            relativeTo : Enums.Space = Enums.Space.Self,
            waitForObject : bool = True,
            timeout : int = 30
        ):
        request = Messages.Cmd_RotateRequest(
            HierarchyPath = hierarchyPath,
            Euler = euler,
            RelativeTo = relativeTo,
            Timeout = timeout,
            WaitForObject = waitForObject
        )

        return await self._RotateObject(hierarchyPath, request, waitForObject, timeout)

    @requireClientConnection
    async def RotateObject_AxisAngle(self,
            hierarchyPath : str,
            xAngle : float,
            yAngle : float,
            zAngle : float,
            relativeTo : Enums.Space = Enums.Space.Self,
            waitForObject : bool = True,
            timeout : int = 30
        ):
        request = Messages.Cmd_RotateRequest(
            HierarchyPath = hierarchyPath,
            XAngle = xAngle,
            YAngle = yAngle,
            ZAngle = zAngle,
            RelativeTo = relativeTo,
            Timeout = timeout,
            WaitForObject = waitForObject
        )
        return await self._RotateObject(hierarchyPath, request, waitForObject, timeout)

    @requireClientConnection
    async def _RotateObject(self,
            HierarchyPath : str,
            request : Messages.Cmd_RotateRequest,
            waitForObject : bool = True,
            timeout : int = 30
        ):
        msg = ProtocolObjects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = request
        )

        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)
        response = await self.client.GetResult(requestInfo.RequestId)
        if response.RC != Enums.ResponseCode.OK:
            raise Exceptions.InputRequestError(response.ErrorMessage)

        return True

    @requireClientConnection
    async def SetInputFieldText(self,
            hierarchyPath : str,
            text : str,
            waitForObject : bool = True,
            timeout : int = 30
        ):
        request = Messages.Cmd_SetInputFieldTextRequest(
            HierarchyPath = hierarchyPath,
            Text = text,
            Timeout = timeout,
            WaitForObject = waitForObject
        )
        requestInfo = await asyncio.wait_for(self.client.SendMessage(request), timeout)
        response = await self.client.GetResult(requestInfo.RequestId)
        if response.RC != Enums.ResponseCode.OK:
            raise Exception(response.ErrorMessage)

        return True

    @requireClientConnection
    async def SetObjectFieldValue() -> bool:
        # TODO: Big one
        raise NotImplementedError

    @requireClientConnection
    async def Tap_XY(self,
            x : float,
            y : float,
            tapCount : int = 1,
            frameCount : int = 5,
            timeout : int = 30
        ) -> bool:
        request = Messages.Cmd_TapRequest(
            X = x,
            Y = y,
            FrameCount = frameCount,
            TapCount = tapCount
        )
        requestInfo = await asyncio.wait_for(self.client.SendMessage(request), timeout)
        response = await self.client.GetResult(requestInfo.RequestId)
        if response.RC != Enums.ResponseCode.OK:
            raise Exception(response.ErrorMessage)

        return True

    @requireClientConnection
    async def Tap_Vec2(self,
            position : ProtocolObjects.Vector2,
            tapCount : int = 1,
            frameCount : int = 5,
            timeout : int = 30
        ) -> bool:
        return await self.Tap_XY(position.X, position.Y, tapCount, frameCount, timeout)

    @requireClientConnection
    async def TapObject(self,
            hierarchyPath : str,
            tapCount : int = 1,
            frameCount : int = 5,
            cameraHierarchyPath : str = None,
            timeout : int = 30
        ) -> bool:
        request = Messages.Cmd_TapRequest(
            HierarchyPath = hierarchyPath,
            FrameCount = frameCount,
            TapCount = tapCount,
            CameraHierarchyPath = cameraHierarchyPath
        )
        requestInfo = await asyncio.wait_for(self.client.SendMessage(request), timeout)
        response = await self.client.GetResult(requestInfo.RequestId)
        if response.RC != Enums.ResponseCode.OK:
            raise Exception(response.ErrorMessage)

        return True

    @requireClientConnection
    async def TerminateGame(self):
        raise NotImplementedError

    @requireClientConnection
    async def ToggleEditorPause(self):
        raise NotImplementedError

    @requireClientConnection
    async def ToggleEditorPlay(self):
        raise NotImplementedError

    @requireClientConnection
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
        ) -> bool:
        request = Messages.Cmd_TouchEventRequest(
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
        requestInfo = await asyncio.wait_for(self.client.SendMessage(request), timeout)
        response = await self.client.GetResult(requestInfo.RequestId)
        if waitForEmptyInput:
            self.WaitForEmptyInput(timeout)
        if response.RC != Enums.ResponseCode.OK:
            raise Exception(response.ErrorMessage)

        return True

    
    @requireClientConnection
    async def UnregisterCollisionMonitor(self,
            hierarchyPath : str,
            timeout : int = 30
        ) -> bool:
        request = Messages.Cmd_UnregisterCollisionMonitorRequest(
            HierarchyPath = hierarchyPath,
        )
        requestInfo = await asyncio.wait_for(self.client.SendMessage(request), timeout)
        response = await self.client.GetResult(requestInfo.RequestId)
        if response.RC != Enums.ResponseCode.OK:
            raise Exception(response.ErrorMessage)

        return True

    async def Wait(self, miliseconds : int) -> None:
        time.sleep(miliseconds * 0.001)

    @requireClientConnection
    async def WaitForEmptyInput(self, timeout : int = 30) -> bool:
        await asyncio.wait_for(self.client.WaitForEmptyInput(datetime.datetime.now().timestamp()), timeout)

    @requireClientConnection
    async def WaitForCollisionEvent(self,
            eventId : str,
            timeout : int = 30
        ) -> ProtocolObjects.Collision:
        raise NotImplementedError

    def waitForObject(self,
            hierarchyPath : str,
            timeout : int = 30
        ) -> bool:
        raise NotImplementedError

    def waitForObjectValue(self,
            hierarchyPath : str,
            timeout : int = 30
        ) -> bool:
        raise NotImplementedError

    def _cleanup(self):
        pass