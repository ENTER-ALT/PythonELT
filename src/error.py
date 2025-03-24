from enum import Enum

class Error:
    def __init__(self, message, severity):
        self.message = message
        self.severity = severity

    def __str__(self):
        return f"{self.severity}: {self.message}"

    def __repr__(self):
        return self.__str__()

class ErrorSeverity(Enum):
    SEVERE = 0
    SAFE = 1

    def __str__(self):
        return self.name