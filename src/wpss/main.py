from .core import Screenshot, WhatsApp
from argpi import Arguments, ArgumentDescription, FetchType
from time import sleep as pause
from os import getcwd
import sys

class Screenshotter:
    def __init__(self, arguments: Arguments) -> None:
        self.arguments = arguments
        self.sleep_time = 10
        self.location = getcwd()

        if self.arguments.__there__('--delay'):
            self.sleep_time = int(self.arguments.__fetch__('--delay', FetchType.SINGULAR))
        
        if self.arguments.__there__('--location'):
            self.location = self.arguments.__fetch__('--location', FetchType.SINGULAR)

        if self.arguments.__there__('--start'):
            try:
                self.start
            except KeyboardInterrupt:
                sys.exit(1)

    @property
    def start(self) -> None:
        while True:
            if WhatsApp().open:
                Screenshot(getcwd()).take
            pause(self.sleep_time)
    
def main():
    arguments = Arguments().__capture__()
    arguments.__add__('--delay', ArgumentDescription().shorthand('-d'))
    arguments.__add__('--location', ArgumentDescription().shorthand('-loc'))
    arguments.__add__('--start', ArgumentDescription().shorthand('-s'))
    arguments.__analyse__()

    Screenshotter(arguments)