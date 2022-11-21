from enum import Enum
from sys import platform


class OSName(Enum):
    LINUX = "linux"
    MAC = "mac"
    WINDOWS = "windows"
    UNKNOWN = "unknown"

    @staticmethod
    def by_current_platform():
        if platform == "linux" or platform == "linux2":
            return OSName.LINUX
        if platform == "darwin":
            return OSName.MAC
        if platform == "win32":
            return OSName.WINDOWS
        return OSName.UNKNOWN

    @staticmethod
    def by_name(name):
        for os in OSName:
            if os.value == name:
                return os
        return OSName.UNKNOWN

