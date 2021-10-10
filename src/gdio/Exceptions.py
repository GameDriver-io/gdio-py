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