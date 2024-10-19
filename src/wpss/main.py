from .core import ConfigManager, Email, WhatsApp, Screenshot, ZipAll
from argpi import ArgumentDescription, Arguments, FetchType
from os.path import basename, dirname, expanduser, expandvars, join, exists
from os import getcwd as cwd
from typing import Tuple, Dict, Literal, Union
from time import sleep
from datetime import datetime, timedelta

arguments = Arguments().__capture__()
arguments.__add__('set-config', ArgumentDescription().shorthand('setconf'))
arguments.__add__('capture', ArgumentDescription().shorthand('cap'))
arguments.__add__('capture-bulk', ArgumentDescription().shorthand('bcap'))
arguments.__analyse__()

def get_config() -> Tuple[ConfigManager, Dict]:
    if arguments.__there__('set-config'):
        location: str = arguments.__fetch__('set-config', FetchType.SINGULAR)
        location = expanduser(expandvars(location))
        if location.startswith('./'):
            location = join(cwd(), location[2:])
        
        # save this location to ~/.wpss
        with open(join(expanduser('~'), '.wpss'), 'w+') as ref:
            ref.write(location)
        print(f"Saved Where to look for config to: {join(expanduser('~'), '.wpss')}")
        
        config_file = ConfigManager(dirname(location), basename(location))
    else:
        # if ~/.wpss exists
        if exists(join(expanduser('~'), '.wpss')):
            with open(join(expanduser('~'), '.wpss'), 'r+') as ref:
                location = ref.read().replace('\n', '')
            
            config_file = ConfigManager(dirname(location), basename(location))
        else:
            config_file = ConfigManager()
            with open(join(expanduser('~'), '.wpss'), 'w+') as ref:
                ref.write(join(expanduser('~'), '.ss-config.toml'))
            print(f"Saved Where to look for config to: {join(expanduser('~'), '.wpss')}")
            print(f"Where to look: {join(expanduser('~'), '.ss-config.toml')} (default)")
    
    # get the info
    # CONFIG: keywords, store, delay, browsers
    # EMAIL: APS, sender, receiver, subject, body, server, port

    keywords = config_file.fetch('config.keywords')
    store = config_file.fetch('config.store')
    delay = config_file.fetch('config.delay')
    browsers = config_file.fetch('config.browsers')
    bulk = config_file.fetch('config.bulk')
    bulk_time = config_file.fetch('config.bulk-time')

    APS = config_file.fetch('email.APS')
    sender = config_file.fetch('email.sender')
    receiver = config_file.fetch('email.receiver')
    subject = config_file.fetch('email.subject')
    body = config_file.fetch('email.body')
    server = config_file.fetch('email.server')
    port = config_file.fetch('email.port')

    # handle default
    if not keywords:
        keywords = ['whatsapp', 'WhatsApp', 'whatsapp web', 'WhatsApp Web']
    
    if not store:
        raise EnvironmentError("config.store is a manadatory config variable. NOT FOUND in toml file.")
    
    if not delay:
        delay = 10
    elif not isinstance(delay, int):
        delay = int(delay)
    
    if not browsers:
        browsers = ['chrome', 'firefox', 'safari', 'msedge', 'opera']
    
    if not bulk:
        bulk = False
    elif not isinstance(bulk, bool):
        raise ValueError("config.bulk only accepts boolean value.")
    
    if bulk:
        if not bulk_time:
            bulk_time = 2
        elif not isinstance(bulk_time, int):
            try:
                bulk_time = int(bulk_time)
            except Exception:
                raise RuntimeError(f"Cannot convert config.bulk-time value to int: {bulk_time}")
    
    if not APS:
        raise EnvironmentError("email.APS is a mandatory config variable. NOT FOUND.")
    
    if not sender:
        raise EnvironmentError("email.sender is a mandatory config variable. NOT FOUND.")
    
    if not receiver:
        raise EnvironmentError("email.receiver is a mandatory config variable. NOT FOUND.")
    
    if not subject:
        subject = "Screenshot_Delivery"
    
    if not server:
        raise EnvironmentError("email.server is a mandatory config variable. NOT FOUND.")
    
    if not port:
        port = 587
    elif not isinstance(port, int):
        port = int(port)
    
    res = {}
    res['keywords'] = keywords
    res['store'] = store
    res['delay'] = delay
    res['browsers'] = browsers
    res['bulk'] = bulk
    res['bulk-time'] = bulk_time
    res['APS'] = APS
    res['sender'] = sender
    res['receiver'] = receiver
    res['subject'] = subject
    res['body'] = body
    res['server'] = server
    res['port'] = port
    
    return (config_file, res)

def main_normal():
    main('normal')

def main_bulk():
    main('bulk')

def main(capture_type: Union[Literal['normal', 'bulk'], None] = None):
    config, configurations = get_config()

    def has_bulk_time_reached(start_time: datetime) -> bool:
        return (datetime.now() - start_time) >= timedelta(hours=configurations['bulk-time'])
    
    

    if arguments.__there__('capture') or capture_type == 'normal':
        while True:
            # Take ss only if whatsapp is open
            if WhatsApp(configurations['keywords'], configurations['browsers']).open:
                ss = Screenshot(configurations['store'])
                ss.take

                print(f"Screenshot saved to {ss.saved_to}")
                
                # Email it
                email = Email(
                    Application_Specific_Password=configurations['APS'],
                    sender=configurations['sender'],
                    receiver=configurations['receiver'],
                    subject=configurations['subject'],
                    body=configurations['body'],
                    attachment=ss.saved_to,
                    server=configurations['server'],
                    port=configurations['port'],
                )

                print("Sending to Moderator ...", end='\r')
                email.send
                print("                         ", end='\r')
                print("Sent to Moderator.")
                sleep(configurations['delay']//2)
            else:
                sleep(configurations['delay'])
    elif arguments.__there__('capture-bulk') or capture_type == 'bulk':
        start_time = datetime.now()
        while True:
            if WhatsApp(configurations['keywords'], configurations['browsers']).open:
                ss = Screenshot(configurations['store'])
                ss.take

                print(f"Screenshot saved to {ss.saved_to}")

            if has_bulk_time_reached(start_time):
                # Zip it.
                if ZipAll.check_contents(configurations['store']):

                    zipper = ZipAll(configurations['store'], f'screenshots_at_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.zip')
                    zipper.make

                    # Email it
                    email = Email(
                        Application_Specific_Password=configurations['APS'],
                        sender=configurations['sender'],
                        receiver=configurations['receiver'],
                        subject=configurations['subject'],
                        body=configurations['body'],
                        attachment=zipper.get_path,
                        server=configurations['server'],
                        port=configurations['port'],
                    )

                    print(f"Time Elapsed: {configurations['bulk-time']} hours")

                    print("Sending to Moderator ...", end='\r')
                    email.send
                    print("                         ", end='\r')
                    print("Sent to Moderator.")
                    sleep(configurations['delay']//2)
            else:
                sleep(configurations['delay'])
                