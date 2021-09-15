from .Client import Client
from . import Objects, Requests, Responses, Exceptions

import os
import asyncio, socket
import time


class ApiClient:
    def __init__(self):
        
        # Declare client. Defined in self.Connect().
        self.client = None

        # Declare gameConnectionDetails. Defined in self.Connect().
        self.gameConnectionDetails = None

        return

    def AxisPress(self,
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
        # Send the message, and save its Client, RequestID, and Timestamp.
        requestInfo = self.client.SendMessage(msg)

        # Wait until either:
        #   the message is acknowleged
        #   or the request times out and throws and exception.
        self.client.Wait(requestInfo, timeout)

        # The message didn't timeout and was sent successfully; return True.
        return True

    def ButtonPress(self,
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
        # Send the message, and save its Client, RequestID, and Timestamp.
        requestInfo = self.client.SendMessage(msg)

        # Wait until either:
        #   the message is acknowleged
        #   or the request times out and throws and exception.
        self.client.Wait(requestInfo, timeout)

        # The message didn't timeout and was sent successfully; return True.
        return True
    
    ## Void overload
    def CallMethod(self,
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

        # Send the message, and save its Client, RequestID, and Timestamp.
        requestInfo = self.client.SendMessage(msg)

        # Wait until either:
        #   the message is acknowleged
        #   or the request times out and throws and exception.
        self.client.Wait(requestInfo, timeout)

        # Recieve the response message and save its contained GDIOMsg.
        response = Responses.GetObjectValueResponse(**Objects.getGDIOMsgData(self.client.Recieve()))

        # If the response is an error, warning, or information message,
        if response.RC != 0:
            # throw an exception containing the response data.
            raise Exceptions.CallMethodError(response.ErrorMessage)

        # The message didn't timeout, and the response was OK; return
        return

    ## Return value overload
    '''
    def CallMethod(self) -> type:
        raise NotImplementedError
        return
    '''

    def CaptureScreenshot(self,
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

        # Send the message, and save its Client, RequestID, and Timestamp.
        requestInfo = self.client.SendMessage(msg)

        # Wait until either:
        #   the message is acknowleged
        #   or the request times out and throws and exception.
        self.client.Wait(requestInfo, timeout)

        # Recieve the response message and save its contained GDIOMsg.
        response = Responses.CaptureScreenshotResponse(**Objects.getGDIOMsgData(self.client.Recieve()))
        
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
    def Click(self,
            buttonId : Objects.MouseButtons,
            x : float,
            y : float,
            clickFrameCount : int,
            timeout : int = 30
        ) -> bool:
        raise NotImplementedError

    ## Vector2 positions overload
    '''
    def Click(self,
            buttonId : MouseButtons,
            position : Vector2,
            clickFrameCount : int,
            timeout : int = 30
        ) -> bool:
        return self.Click(buttonId, position.x, position.y, clickFrameCount, timeout)
    '''

    ## Float positions overload
    def ClickEx(self,
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
    def ClickEx(self,
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
    
    def ClickObject(self) -> bool:
        raise NotImplementedError

    def ClickObjectEx(self) -> bool:
        raise NotImplementedError

    def Connect(self,
            hostname : str = '127.0.0.1',    # The hostname of the device running the target game.
            port     : int = 19734,          # The port that the target Gamedriver agent is configured to use.
            autoplay : bool = False,         # TODO: Start the game automatically within the Unity Editor.
            timeout  : int = 30,             # The number of seconds to wait for the command to be recieved by the agent.
            autoPortResolution : bool = True # TODO: Automatically resolve the port a Gamedriver Agent is running on.
        ) -> None:

        # Try to connect to the target game.
        try:
            self.client = Client(hostname, port, timeout)

            if not self.client.Connect():
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
    def Connect(self) -> None:
        raise NotImplementedError
        return
    '''

    def DisableHooks(self, timeout : int = 30) -> bool:

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

        # Send the message, and save its Client, RequestID, and Timestamp.
        requestInfo = self.client.SendMessage(msg)

        # Wait until either:
        #   the message is acknowleged
        #   or the request times out and throws and exception.
        self.client.Wait(requestInfo, timeout)

        # No exceptions thrown; return True
        return True

    def DisableObjectCaching(self, timeout : int = 30) -> bool:

        # This command cannot be run without an agent connection.
        if not self.client:
            raise Exceptions.ClientNotConnectedError
            
        msg = Objects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Requests.ChangeObjectResolverCacheStateRequest(
                STATE = False
            )
        )

        # Send the message, and save its Client, RequestID, and Timestamp.
        requestInfo = self.client.SendMessage(msg)

        # Wait until either:
        #   the message is acknowleged
        #   or the request times out and throws and exception.
        self.client.Wait(requestInfo, timeout)

        # No exceptions thrown; return True
        return True

    def Disconnect(self) -> None:
        # If the client isn't connected,
        if not self.client:
            # theres no need to disconnect.
            return

        ## TODO: CLEANUP
        self.gameConnectionDetails = None

        self.client.Disconnect()

    ## Float positions overload
    def DoubleClick(self) -> bool:
        raise NotImplementedError
    
    ## Vector2 positions overload
    '''
    def DoubleClick(self) -> bool:
        return self.DoubleClick()
    '''

    ## Float positions overload
    def DoubleClickEx(self) -> bool:
        raise NotImplementedError
    
    ## Vector2 positions overload
    '''
    def DoubleClickEx(self) -> bool:
        return self.DoubleClickEx()
    '''

    ## Float positions overload
    def DoubleClickObject(self) -> bool:
        raise NotImplementedError
    
    ## Vector2 positions overload
    '''
    def DoubleClickObject(self) -> bool:
        return self.DoubleClickObject()
    '''

    def EnableHooks(self, timeout : int = 30) -> bool:

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

        # Send the message, and save its Client, RequestID, and Timestamp.
        requestInfo = self.client.SendMessage(msg)

        # Wait until either:
        #   the message is acknowleged
        #   or the request times out and throws and exception.
        self.client.Wait(requestInfo, timeout)

        # No exceptions thrown; return True
        return True


    def EnableObjectCaching(self, timeout : int = 30) -> bool:

        # This command cannot be run without an agent connection.
        if not self.client:
            raise Exceptions.ClientNotConnectedError

        msg = Objects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Requests.ChangeObjectResolverCacheStateRequest(
                STATE = True
            )
        )

        # Send the message, and save its Client, RequestID, and Timestamp.
        requestInfo = self.client.SendMessage(msg)

        # Wait until either:
        #   the message is acknowleged
        #   or the request times out and throws and exception.
        self.client.Wait(requestInfo, timeout)

        # No exceptions thrown; return True
        return True
    
    def FlushObjectLookupCache(self, timeout : int = 30) -> bool:

        # This command cannot be run without an agent connection.
        if not self.client:
            raise Exceptions.ClientNotConnectedError
            
        msg = Objects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Requests.FlushCacheRequest()
        )

        # Send the message, and save its Client, RequestID, and Timestamp.
        requestInfo = self.client.SendMessage(msg)

        # Wait until either:
        #   the message is acknowleged
        #   or the request times out and throws and exception.
        self.client.Wait(requestInfo, timeout)

        # No exceptions thrown; return True
        return True

    def GetConnectedGameDetails(self) -> Objects.GameConnectionDetails:
        # Can't retrieve details about a game the client isn't connected to.
        if not self.client:
            raise Exceptions.ClientNotConnectedError

        return self.gameConnectionDetails

    def GetLastFPS(self) -> float:
        raise NotImplementedError

    def GetNextCollisionEvent(self) -> Objects.Collision:
        raise NotImplementedError


########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################

    def GetObjectList(self, timeout : int = 30) -> bool:

        # This command cannot be run without an agent connection.
        if not self.client:
            raise Exceptions.ClientNotConnectedError
            
        msg = Objects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Requests.GetObjectListRequest()
        )
        # Send the message, and save its Client, RequestID, and Timestamp.
        requestInfo = self.client.SendMessage(msg)

        # Wait until either:
        #   the message is acknowleged
        #   or the request times out and throws and exception.
        self.client.Wait(requestInfo, timeout)

        # TODO: return object list if RC==OK
        return True

    def GetSceneName(self, timeout : int = 30) -> bool:
        
        # This command cannot be run without an agent connection.
        if not self.client:
            raise Exceptions.ClientNotConnectedError
            
        msg = Objects.ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = Requests.GetSceneNameRequest()
        )
        # Send the message, and save its Client, RequestID, and Timestamp.
        requestInfo = self.client.SendMessage(msg)

        # Wait until either:
        #   the message is acknowleged
        #   or the request times out and throws and exception.
        self.client.Wait(requestInfo, timeout)

        # TODO: return scene name if RC==OK
        return True

    

    def Wait(self, miliseconds : int) -> None:
        time.sleep(miliseconds * 0.001)