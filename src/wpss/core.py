from pyautogui import screenshot
from datetime import datetime
from os.path import expanduser, expandvars, join, isdir
from os import getcwd
import psutil, pygetwindow as gw

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
        loc = join(self.location, f"screenshot_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png")
        ss.save(loc)
        print(f"Saved: {loc}")

class WhatsApp:
    def __init__(self) -> None:
        self.windows = gw.getAllTitles()
    
    @staticmethod
    def check_name(name: str) -> bool:
        to_check = ["chrome", 'safari', 'msedge', 'opera', 'firefox']
        for n in to_check:
            if n in name:
                return True
        
        return False

    @property
    def open(self) -> bool:
        for window in self.windows:
            if 'WhatsApp' in window or 'whatsapp' in window:
                return True
        
        for proc in psutil.process_iter(['name']):
            try:
                if WhatsApp.check_name(proc.info['name']):
                    for window in self.windows:
                        if 'WhatsApp Web' in window or 'whatsapp web' in window or 'WhatsApp' in window or 'whatsapp' in window:
                            return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        return False