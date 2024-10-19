from pyautogui import screenshot
from datetime import datetime
from os.path import expanduser, expandvars, join, isdir, exists, basename, isfile
from os import getcwd, listdir, unlink
import psutil, pygetwindow as gw
from typing import Union, Literal
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import toml
import smtplib
import zipfile

class Screenshot:
    def __init__(self, location: str) -> None:
        self.location = expanduser(expandvars(location))
        if self.location.startswith('./'):
            self.location = join(getcwd(), self.location[2:])
        
        if not isdir(self.location):
            raise NotADirectoryError("Location should be a directory.")

    @property
    def take(self) -> None:
        ss = screenshot()
        self.loc = join(self.location, f"screenshot_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png")
        ss.save(self.loc)
    
    @property
    def saved_to(self) -> str:
        return self.loc

class WhatsApp:
    def __init__(self, keywords: list[str], browsers: list[str]) -> None:
        self.windows = gw.getAllTitles()
        self.keywords = keywords
        self.browsers = browsers
    
    @staticmethod
    def check_in_pname(name: str, keywords: list[str]) -> bool:
        to_check = keywords
        for n in to_check:
            if n in name:
                return True
        
        return False

    @staticmethod
    def check_keywords(keywords: list[str], target: str) -> bool:
        for x in keywords:
            if x in target:
                return True
        return False

    @property
    def open(self) -> bool:
        for window in self.windows:
            if 'WhatsApp' in window or 'whatsapp' in window:
                return True
        
        for proc in psutil.process_iter(['name']):
            try:
                if WhatsApp.check_in_pname(proc.info['name'], self.browsers):
                    for window in self.windows:
                        if WhatsApp.check_keywords(self.keywords, window):
                            return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        return False

class ConfigManager:
    def __init__(self, filedire: str = '~', filename: str = '.ss-config.toml') -> None:
        self.filepath = expanduser(expandvars(filedire))
        self.filename = filename
        self.config_data = {}
        self.load_config()
    
    def load_config(self) -> None:
        if exists(self.filepath) and isdir(self.filepath) and exists(join(self.filepath, self.filename)):
            with open(join(self.filepath, self.filename), 'r+') as ref:
                self.config_data = toml.load(ref)
        else:
            self.config_data = {}
    
    def save_config(self):
        with open(join(self.filepath, self.filename), 'w+') as ref:
            toml.dump(self.config_data, ref)
    
    def add(self, root: str, value: str) -> None:
        keys = root.split('.')
        d = self.config_data

        # Traverse the keys except the last one, ensuring nested dictionaries are created
        for k in keys[:-1]:
            d = d.setdefault(k, {})

        # Set the value for the last key directly
        d[keys[-1]] = value

        # Save the updated configuration
        self.save_config()
    
    def remove(self, key: str) -> None:
        keys = key.split('.')
        d = self.config_data
        try:
            for k in keys[:-1]:
                d = d[k]
            del d[keys[-1]]
            self.save_config()
        except KeyError:
            print(f"Key \'{key}\' not found.")
    
    def fetch(self, key: str):
        keys = key.split('.')
        d = self.config_data
        try:
            for k in keys:
                d = d[k]
            return d
        except KeyError:
            print(f"Key \'{key}\' not found.")
            return None

class Email:
    def __init__(self, Application_Specific_Password: str, sender: str, receiver: str, subject: str, body: Union[str, None] = None, attachment: Union[str, None] = None, server: str = 'smtp.zoho.in', port: Literal[456, 587] = 587) -> None:
        self.aps = Application_Specific_Password
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.body = body
        self.attachment = attachment
        self.server = server
        self.port = port
    
    @property
    def send(self) -> bool:
        # Create Message Content
        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = self.receiver
        msg['Subject'] = self.subject

        if self.body:
            msg.attach(MIMEText(self.body, 'plain'))
        else:
            msg.attach(MIMEText('Email Sent from Python Script', 'plain'))
        
        # Attachment if any
        if self.attachment:
            attachment = open(self.attachment, 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={basename(self.attachment)}')

            msg.attach(part)
            attachment.close()
        
        # connect with server
        with smtplib.SMTP(self.server, self.port) as server:
            server.starttls()
            server.login(self.sender, self.aps)
            server.sendmail(self.sender, self.receiver, msg.as_string())
        
        return True

class ZipAll:
    @staticmethod
    def check_contents(dir: str) -> bool:
        return len(listdir(dir)) > 0

    def __init__(self, directory: str, outfile_name: str = 'output.zip') -> None:
        self.directory = directory
        self.files = [f for f in listdir(directory) if isfile(join(directory, f))]

        self.zip_filename = join(directory, outfile_name)
    
    @property
    def make(self) -> None:

        with zipfile.ZipFile(self.zip_filename, 'w') as zip_ref:
            for file in self.files:
                filepath = join(self.directory, file)
                zip_ref.write(filepath, arcname=file)
        
        for file in self.files:
            unlink(join(self.directory, file))
    
    @property
    def get_path(self) -> str:
        return self.zip_filename