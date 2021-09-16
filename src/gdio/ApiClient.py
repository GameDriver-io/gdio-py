from .Client import Client
from . import Objects, Requests, Responses, Exceptions

import os
import asyncio
import time


class ApiClient:
    def __init__(self):
        
        # Declare client. Defined in self.Connect().
        self.client = None

        # Declare gameConnectionDetails. Defined in self.Connect().
        self.gameConnectionDetails = None

        return

    async def AxisPress(self,
            axisId         : str,      # The name of the target input axis as defined in the Unity Input Manager.
            value          : float,    # The value of change on the target axis from -1.0 to +1.0.
            numberOfFrames : int,      # The number of frames to hold the input for.
            timeout        : int = 30  # The number of seconds to wait for the command to be recieved by the agent.
        ) -> bool:

        # This command cannot be run without an agent connection.
        if not self.client:
            raise Exceptions.ClientNotConnectedError

        msg = Objects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Requests.InputManagerStateRequest(
                IdName = axisId,
                NumberOfFrames = numberOfFrames,
                InputType = 1,
                ChangeValue = value
                )
        )

        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)

        # Mitigates response mixups. Still happens sometimes.
        # Also means commands are input dependent
        await self.client.Recieve()

        # The message didn't timeout and was sent successfully; return True.
        return True

    async def ButtonPress(self,
            buttonId       : str,      # The name of the target input button as defined in the Unity Input Manager.
            numberOfFrames : int,      # The number of frames to hold the input for.
            timeout        : int = 30  # The number of seconds to wait for the command to be recieved by the agent.
        ) -> bool:

        # This command cannot be run without an agent connection.
        if self.client == None:
            raise Exceptions.ClientNotConnectedError

        msg = Objects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Requests.InputManagerStateRequest(
                IdName = buttonId,
                NumberOfFrames = numberOfFrames,
                InputType = 0,
                ChangeValue = 0
            ),
        )
        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)

        # Mitigates response mixups. Still happens sometimes.
        # Also means commands are input dependent
        await self.client.Recieve()

        # The message didn't timeout and was sent successfully; return True.
        return True
    
    ## Void overload
    async def CallMethod(self,
            hierarchyPath   : str,      # The HierarchyPath for an object and the script attached to it.
            methodName      : str,      # The name of the method to call within the script.
            arguments       : list,     # TODO: The list of arguments to pass into the method.
            timeout         : int = 30, # The number of seconds to wait for the command to be recieved by the agent.
        ) -> None:

        # This command cannot be run without an agent connection.
        if self.client == None:
            raise Exceptions.ClientNotConnectedError

        msg = Objects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Requests.CallMethodRequest(
                HierarchyPath = hierarchyPath,
                MethodName = methodName,
            )
        )

        # TODO: Set and serialize the method's arguments.
        msg.GDIOMsg.SetArguments(arguments)

        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)

        # Recieve the response message and save its contained GDIOMsg.
        response = Responses.GetObjectValueResponse(**Objects.getGDIOMsgData(await self.client.Recieve()))

        # If the response is an error, warning, or information message,
        if response.RC != 0:
            # throw an exception containing the response data.
            raise Exceptions.CallMethodError(response.ErrorMessage)

        # The message didn't timeout, and the response was OK; return
        return

    ## Return value overload
    '''
    async def CallMethod(self) -> type:
        raise NotImplementedError
        return
    '''

    async def CaptureScreenshot(self,
            filename          : str,          # The path and filename of the screen capture.
            storeInGameFolder : bool = False, # TODO: Save the screenshot on the device the game is running on rather than returning it to the client.
            overwriteExisting : bool = False, # Overwrite if the file already exists.
            timeout           : int = 60,     # The number of seconds to wait for the command to be recieved by the agent.
        ) -> str:

        # This command cannot be run without an agent connection.
        if self.client == None:
            raise Exceptions.ClientNotConnectedError

        msg = Objects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Requests.CaptureScreenshotRequest(
                StoreInGameFolder = storeInGameFolder,
                Filename = filename,
            ),
        )

        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)

        # Recieve the response message and save its contained GDIOMsg.
        response = Responses.CaptureScreenshotResponse(**Objects.getGDIOMsgData(await self.client.Recieve()))
        
        # If the response is an Error,
        if response.RC == 2:
            # throw an exception containing the response data.
            raise Exceptions.CaptureScreenshotError(response.ErrorMessage)

        # TODO: Im not sure this works properly
        # If the client does not save the image localy,
        if storeInGameFolder:
            # Return the image's location relative to the game.
            return response.ImagePath

        # If the file already exists,
        # and `overwriteExisting` is not True,
        if os.path.isfile(filename) and not overwriteExisting:
            # throw and exception that the image can't be saved.
            raise OSError(f'Cannot save screenshot to {filename}, file already exists')
        
        # TODO: Relative paths
        with open(filename, 'wb') as f:
            f.write(response.ImageData)

        # No exceptions thrown; return image's location.
        return filename
        
    ## Float positions overload
    async def Click(self,
            buttonId : Objects.MouseButtons,
            x : float,
            y : float,
            clickFrameCount : int,
            timeout : int = 30
        ) -> bool:
        raise NotImplementedError

    ## Vector2 positions overload
    '''
    async def Click(self,
            buttonId : MouseButtons,
            position : Vector2,
            clickFrameCount : int,
            timeout : int = 30
        ) -> bool:
        return self.Click(buttonId, position.x, position.y, clickFrameCount, timeout)
    '''

    ## Float positions overload
    async def ClickEx(self,
            buttonId : Objects.MouseButtons,
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
        raise NotImplementedError

    ## Vector2 positions overload
    '''
    async def ClickEx(self,
            buttonId : MouseButtons,
            position : Vector2,
            clickFrameCount : int,
            keys : list = None,
            keysNumberOfFrames : int = 5,
            modifiers : list = None,
            modifiersNumberOfFrames : int = 3,
            delayAfterModifiersMsec : int = 500,
            timeout : int = 30
        ) -> bool:
        return ClickEx(buttonId, position.x, position.y, clickFrameCount, keys, keysNumberOfFrames, modifiers, modifiersNumberOfFrames, delayAfterModifiersMsec, timeout)
    '''
    
    async def ClickObject(self) -> bool:
        raise NotImplementedError

    async def ClickObjectEx(self) -> bool:
        raise NotImplementedError

    async def Connect(self,
            hostname : str = '127.0.0.1',    # The hostname of the device running the target game.
            port     : int = 19734,          # The port that the target Gamedriver agent is configured to use.
            autoplay : bool = False,         # TODO: Start the game automatically within the Unity Editor.
            timeout  : int = 30,             # The number of seconds to wait for the command to be recieved by the agent.
            autoPortResolution : bool = True # TODO: Automatically resolve the port a Gamedriver Agent is running on.
        ) -> None:

        # Try to connect to the target game.
        try:
            self.client = Client(hostname, port, timeout)

            if not await self.client.Connect():
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

    async def DisableHooks(self, timeout : int = 30) -> bool:

        # This command cannot be run without an agent connection.
        if not self.client:
            raise Exceptions.ClientNotConnectedError

        # TODO: Hooking objects
        # NOTE: ATM, disables all hooking
        msg = Objects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Requests.ChangeHookStatusRequest(
                KeyboardHooksStatus = False,
                MouseHooksStatus = False,
                TouchHooksStatus = False,
                GamepadHooksStatus = False,
                BitChanged = 0xF
            ),
        )

        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)

        # Mitigates response mixups. Still happens sometimes.
        # Also means commands are input dependent
        await self.client.Recieve()

        # No exceptions thrown; return True
        return True

    async def DisableObjectCaching(self, timeout : int = 30) -> bool:

        # This command cannot be run without an agent connection.
        if not self.client:
            raise Exceptions.ClientNotConnectedError
            
        msg = Objects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Requests.ChangeObjectResolverCacheStateRequest(
                STATE = False
            )
        )

        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)

        # Mitigates response mixups. Still happens sometimes.
        # Also means commands are input dependent
        await self.client.Recieve()

        # No exceptions thrown; return True
        return True

    async def Disconnect(self) -> None:
        # If the client isn't connected,
        if not self.client:
            # theres no need to disconnect.
            return

        ## TODO: CLEANUP
        self.gameConnectionDetails = None

        await self.client.Disconnect()

    ## Float positions overload
    async def DoubleClick(self) -> bool:
        raise NotImplementedError
    
    ## Vector2 positions overload
    '''
    async def DoubleClick(self) -> bool:
        return self.DoubleClick()
    '''

    ## Float positions overload
    async def DoubleClickEx(self) -> bool:
        raise NotImplementedError
    
    ## Vector2 positions overload
    '''
    async def DoubleClickEx(self) -> bool:
        return self.DoubleClickEx()
    '''

    ## Float positions overload
    async def DoubleClickObject(self) -> bool:
        raise NotImplementedError
    
    ## Vector2 positions overload
    '''
    async def DoubleClickObject(self) -> bool:
        return self.DoubleClickObject()
    '''

    async def EnableHooks(self, timeout : int = 30) -> bool:

        # This command cannot be run without an agent connection.
        if not self.client:
            raise Exceptions.ClientNotConnectedError

        # TODO: Hooking objects
        # NOTE: ATM, enables all hooking
        msg = Objects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Requests.ChangeHookStatusRequest(
                KeyboardHooksStatus = True,
                MouseHooksStatus = True,
                TouchHooksStatus = True,
                GamepadHooksStatus = True,
                BitChanged = 0xF
            ),
        )

        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)

        # Mitigates response mixups. Still happens sometimes.
        # Also means commands are input dependent
        await self.client.Recieve()

        # No exceptions thrown; return True
        return True


    async def EnableObjectCaching(self, timeout : int = 30) -> bool:

        # This command cannot be run without an agent connection.
        if not self.client:
            raise Exceptions.ClientNotConnectedError

        msg = Objects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Requests.ChangeObjectResolverCacheStateRequest(
                STATE = True
            )
        )

        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)

        # Mitigates response mixups. Still happens sometimes.
        # Also means commands are input dependent
        await self.client.Recieve()

        # No exceptions thrown; return True
        return True
    
    async def FlushObjectLookupCache(self, timeout : int = 30) -> bool:

        # This command cannot be run without an agent connection.
        if not self.client:
            raise Exceptions.ClientNotConnectedError
            
        msg = Objects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Requests.FlushCacheRequest()
        )

        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)

        # Mitigates response mixups. Still happens sometimes.
        # Also means commands are input dependent
        await self.client.Recieve()

        # No exceptions thrown; return True
        return True

    async def GetConnectedGameDetails(self) -> Objects.GameConnectionDetails:
        # Can't retrieve details about a game the client isn't connected to.
        if not self.client:
            raise Exceptions.ClientNotConnectedError

        return self.gameConnectionDetails

    async def GetLastFPS(self) -> float:
        raise NotImplementedError

    async def GetNextCollisionEvent(self) -> Objects.Collision:
        raise NotImplementedError


########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################

    async def GetObjectList(self, timeout : int = 30) -> bool:

        # This command cannot be run without an agent connection.
        if not self.client:
            raise Exceptions.ClientNotConnectedError
            
        msg = Objects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Requests.GetObjectListRequest()
        )

        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)

        # Mitigates response mixups. Still happens sometimes.
        # Also means commands are input dependent
        await self.client.Recieve()

        # TODO: return object list if RC==OK
        return True

    async def GetSceneName(self, timeout : int = 30) -> bool:
        
        # This command cannot be run without an agent connection.
        if not self.client:
            raise Exceptions.ClientNotConnectedError
            
        msg = Objects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Requests.GetSceneNameRequest()
        )

        requestInfo = await asyncio.wait_for(self.client.SendMessage(msg), timeout)

        # Mitigates response mixups. Still happens sometimes.
        # Also means commands are input dependent.
        await self.client.Recieve()

        # TODO: return scene name if RC==OK
        return True

    

    async def Wait(self, miliseconds : int) -> None:
        time.sleep(miliseconds * 0.001)