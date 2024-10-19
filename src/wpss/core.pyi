from pyautogui import screenshot
from datetime import datetime
from os.path import expanduser, expandvars, join, isdir
from os import getcwd
import psutil, pygetwindow as gw
from typing import Union, Literal
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import toml
import smtplib

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
    
    @property
    def saved_to(self) -> str:
        """`Returns the saved location full path`
        
        Use after `take`
        """
        ...

class WhatsApp:
    """`WhatsApp Class`
    
    Responsible for checking if any window is open with instance of whatsapp or whatsapp web in it.
    """
    def __init__(self, keywords: list[str], browsers: list[str]) -> None:
        """`Create a WhatsApp Object.`"""
        ...
    
    @staticmethod
    def check_in_pname(name: str, keywords: list[str]) -> bool:
        """`Checks a list of browser names against the parameter (name)`"""
        ...
    
    @staticmethod
    def check_keywords(keywords: list[str], target: str) -> bool:
        """`Checks if any of the keywords is in target.`"""
        ...
    
    @property
    def open(self) -> bool:
        """`Returns True if any instance is open of whatsapp or whatsapp web (either window or browser tab), else false`"""
        ...

class ConfigManager:
    """`Congiguration Manager`"""
    def __init__(self, filedire: str = '~', filename: str = '.ss-config.toml') -> None:
        """`Create a Configuration Manager Object in the given directory`"""
        ...
    
    def load_config(self) -> None:
        """`Load the config from the path/.ss-config.toml`"""
        ...
    
    def save_config(self) -> None:
        """`Save the Configurations to the file.`"""
        ...
    
    def add(self, root: str, value: str) -> None:
        """"`Add a value.`"""
        ...
    
    def remove(self, key: str) -> None:
        """`Remove a key`"""
        ...
    
    def fetch(self, key: str):
        """`Get a key value.`"""
    
class Email:
    """`Email Sender Class`"""
    def __init__(
            self,
            Application_Specific_Password: str,
            sender: str,
            receiver: str,
            subject: str,
            body: Union[str, None] = None,
            attachment: Union[str, None] = None,
            server: str = 'smtp.zoho.in',
            port: Literal[456, 587] = 587
    ) -> None:
        """`Create an email object.`"""
        ...
    
    @property
    def send(self) -> Literal[True]:
        """`Send the Email.`"""
        ...

class ZipAll:
    """`Zipper for Bulk`"""
    def __init__(self, directory: str, outfile_name: str = 'output.zip') -> None:
        """`Create a ZipAll object for a directory`"""
        ...
    
    @staticmethod
    def check_contents(dir: str) -> bool:
        """`returns true if the dir is non-empty`"""
        ...
    
    @property
    def make(self) -> None:
        """`create the zip file and delete all the contents`"""
        ...
    
    @property
    def get_path(self) -> str:
        """`Returns the zip filename with path.`"""
        ...