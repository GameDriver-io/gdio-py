# TODO: clean up wildcards
from Client import Client
from Objects import *
from Requests import *
from Exceptions import *
from Responses import *

import socket, time, os

def getGDIOMsgData(message : ProtocolMessage):
    # TODO: collect CmdIDs somewhere to rebuild MSGs into classes
    return message['GDIOMsg'][1]


class ApiClient:
    def __init__(self):

        self.client = None
        self.gameConnectionDetails = None

    def Connect(self,
            hostname : str = '127.0.0.1',
            port : int = 19734,
            autoplay : bool = False,    # TODO
            timeout : int = 30,
            autoPortResolution = True   # TODO
        ):
        try:
            self.client = Client(hostname, port, timeout)

            if not self.client.Connect():
                raise FailedGameConnectionError('Failed to connect to the game')
        
        except Exception as inner:
            raise FailedClientConnectionError(f'Failed to connect to {hostname}:{port}') from inner

        else:
            if self.gameConnectionDetails == None:
                self.gameConnectionDetails = self.client.GCD

        return True

    def AxisPress(self,
            axisId,
            value,
            numberOfFrames,
            timeout : int = 30
        ):

        if not self.client:
            raise ClientNotConnectedError

        msg = ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = InputManagerStateRequest(
                IdName = axisId,
                NumberOfFrames = numberOfFrames,
                InputType = 1,
                ChangeValue = value
                ),
        )
        requestInfo = self.client.SendMessage(msg)
        self.client.Wait(requestInfo, timeout)
        return True

    def ButtonPress(self,
            buttonId : str,
            numberOfFrames : int,
            timeout : int = 30
        ):

        if self.client == None:
            raise ClientNotConnectedError

        msg = ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = InputManagerStateRequest(
                IdName = buttonId,
                NumberOfFrames = numberOfFrames,
                InputType = 0,
                ChangeValue = 0
            ),
        )
        requestInfo = self.client.SendMessage(msg)
        self.client.Wait(requestInfo, timeout)
        return True
    
    def CallMethod(self,
            hierarchyPath,
            methodName,
            arguments,
            timeout = 30,
        ):
        if self.client == None:
            raise ClientNotConnectedError

        msg = ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = CallMethodRequest(
                HierarchyPath = hierarchyPath,
                MethodName = methodName,
            ),
        )

        # TODO: Argument serializing
        msg.GDIOMsg.SetArguments(arguments)

        requestInfo = self.client.SendMessage(msg)
        self.client.Wait(requestInfo, timeout)

        response = GetObjectValueResponse(**getGDIOMsgData(self.client.Recieve()))
        if response.RC != 0:
            raise CallMethodError(response.ErrorMessage)

        return True

    def CaptureScreenshot(self,
            filename,
            storeInGameFolder = False,
            overwriteExisting = False,
            timeout = 60,
            ):

        if self.client == None:
            raise ClientNotConnectedError

        msg = ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = CaptureScreenshotRequest(
                StoreInGameFolder = storeInGameFolder,
                Filename = filename,
            ),
        )

        requestInfo = self.client.SendMessage(msg)
        self.client.Wait(requestInfo, timeout)
        
        response = CaptureScreenshotResponse(**getGDIOMsgData(self.client.Recieve()))

        if response.RC == 2:
            raise CaptureScreenshotError(response.ErrorMessage)

        if storeInGameFolder:
            # TODO: Im not sure this works properly
            return response.ImagePath

        if os.path.isfile(filename) and not overwriteExisting:
            raise OSError(f'Cannot save screenshot to {filename}, file already exists')
        
        # TODO: Relative paths
        with open(filename, 'wb') as f:
            f.write(response.ImageData)
        return filename    



    # TODO: Hooking objects
    def EnableHooks(self, timeout = 30):

        if not self.client:
            raise ClientNotConnectedError

        # NOTE: ATM, enables all hooking
        msg = ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = ChangeHookStatusRequest(
                KeyboardHooksStatus = True,
                MouseHooksStatus = True,
                TouchHooksStatus = True,
                GamepadHooksStatus = True,
                BitChanged = 0xF
            ),
        )
        requestInfo = self.client.SendMessage(msg)
        self.client.Wait(requestInfo, timeout)
        return self.client.Recieve()

    # TODO: Hooking objects
    def DisableHooks(self, timeout = 30):
    
        if not self.client:
            raise ClientNotConnectedError

        # NOTE: ATM, disables all hooking 
        msg = ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = ChangeHookStatusRequest(
                KeyboardHooksStatus = False,
                MouseHooksStatus = False,
                TouchHooksStatus = False,
                GamepadHooksStatus = False,
                BitChanged = 0xF
            ),
        )
        requestInfo = self.client.SendMessage(msg)
        self.client.Wait(requestInfo, timeout)
        return self.client.Recieve()

    def EnableObjectCaching(self, timeout = 30):

        msg = ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = ChangeObjectResolverCacheStateRequest(
                STATE = True
            )
        )
        requestInfo = self.client.SendMessage(msg)
        self.client.Wait(requestInfo, timeout)
        return self.client.Recieve()

    def DisableObjectCaching(self, timeout = 30):

        msg = ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = ChangeObjectResolverCacheStateRequest(
                STATE = False
            )
        )
        requestInfo = self.client.SendMessage(msg)
        self.client.Wait(requestInfo, timeout)
        return self.client.Recieve()
    
    def FlushObjectLookupCache(self, timeout = 30):

        msg = ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = FlushCacheRequest()
        )
        requestInfo = self.client.SendMessage(msg)
        self.client.Wait(requestInfo, timeout)
        return self.client.Recieve()

    def GetObjectList(self, timeout = 30):

        msg = ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = GetObjectListRequest()
        )
        requestInfo = self.client.SendMessage(msg)
        self.client.Wait(requestInfo, timeout)

        # TODO: return object list if RC==OK
        return self.client.Recieve()

    def GetSceneName(self, timeout = 30):
        
        msg = ProtocolMessage(
            ClientUID = self.client.ClientUID,
            GDIOMsg = GetSceneNameRequest()
        )
        requestInfo = self.client.SendMessage(msg)
        self.client.Wait(requestInfo, timeout)

        # TODO: return scene name if RC==OK
        return self.client.Recieve()

    def GetConnectedGameDetails(self):
        return self.gameConnectionDetails

    def Disconnect(self):
        self.client.Disconnect()

    def Wait(self, miliseconds):
        time.sleep(miliseconds * 0.001)