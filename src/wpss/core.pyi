from pyautogui import screenshot
from datetime import datetime
from os.path import expanduser, expandvars, join, isdir
from os import getcwd
import psutil, pygetwindow as gw

class Screenshot:
    """`Screenshot Class`
    
    Responsible for all operations related to taking Screenshot of the screen.
    """
    def __init__(self, location: str) -> None:
        """`Create a Screenshot Object.`
        
        #### Parameters
        - **location**: The directory (to store the screenshots)
        """
        ...
    
    @property
    def take(self) -> None:
        """`Take Screenshot.`"""
        ...

class WhatsApp:
    """`WhatsApp Class`
    
    Responsible for checking if any window is open with instance of whatsapp or whatsapp web in it.
    """
    def __init__(self) -> None:
        """`Create a WhatsApp Object.`"""
        ...
    
    @staticmethod
    def check_name(name: str) -> bool:
        """`Checks a list of browser names against the parameter (name)`"""
        ...
    
    @property
    def open(self) -> bool:
        """`Returns True if any instance is open of whatsapp or whatsapp web (either window or browser tab), else false`"""
        ...