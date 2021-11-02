class ClientNotConnectedError(Exception):
    def __init__(self):
        super().__init__('This client is not connected to a GDIOAgent. Use ApiClient.Connect()')

class FailedClientConnectionError(Exception):
    pass

class FailedGameConnectionError(Exception):
    pass

class CallMethodError(Exception):
    pass

class CaptureScreenshotError(Exception):
    pass

class CorruptedHandshakeError(Exception):
    pass

class UnmatchedEventError(Exception):
    pass

class HooksStatusError(Exception):
    def __init__(self, message=None):
        self.message = '' if message == None else message
        super.__init__(f'Failied to change hook status: {self.message}')

class ClickObjectError(Exception):
    def __init__(self, message=None):
        self.message = '' if message == None else message
        super.__init__(f'Failied to click object: {self.message}')

class ObjectListError(Exception):
    def __init__(self, message=None):
        self.message = '' if message == None else message
        super.__init__(f'Failied to get object list: {self.message}')

class ObjectPositionError(Exception):
    def __init__(self, message=None):
        self.message = '' if message == None else message
        super.__init__(f'Failied to get object position: {self.message}')

class SceneNameError(Exception):
    def __init__(self, message=None):
        self.message = '' if message == None else message
        super.__init__(f'Failied to get scene name: {self.message}')

class InputRequestError(Exception):
    def __init__(self, message=None):
        self.message = '' if message == None else message
        super.__init__(f'Failied to execute input request: {self.message}')