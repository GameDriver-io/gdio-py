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