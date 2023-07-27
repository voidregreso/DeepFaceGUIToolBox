import configparser
import os

config = configparser.ConfigParser()

def activate(proto, ipaddr, puerto, yesno):
    if yesno and proto == 'http':
        os.environ["http_proxy"] = f'http://{ipaddr}:{puerto}'
        os.environ["https_proxy"] = f'http://{ipaddr}:{puerto}'
        print('Enabled global proxy')
    else:
        os.environ["http_proxy"] = ''
        os.environ["https_proxy"] = ''
        print('Disabled global proxy')

def WriteCfg(enabled, proto, ipaddr, puerto):
    try:
        config.read("Config.ini")
        config.remove_section('Proxy')
        config.add_section("Proxy")
        config.set("Proxy", "Enabled", str(enabled))
        config.set("Proxy", "Protocol", proto)
        config.set("Proxy", "IPAddr", ipaddr)
        config.set("Proxy", "Port", puerto)
        with open("Config.ini", "w") as f:
            config.write(f)
        activate(proto, ipaddr, puerto, enabled)
        return True
    except Exception as e:
        print(f'Error occurred: {e}')
        return False

def ReadCfg():
    try:
        config.read("Config.ini")
        enabled = config.getboolean("Proxy", "Enabled")
        proto = config.get("Proxy", "Protocol").strip()
        ipaddr = config.get("Proxy", "IPAddr").strip()
        puerto = config.get("Proxy", "Port").strip()
        return enabled, proto, ipaddr, puerto
    except Exception as e:
        print(f'Error occurred: {e}')
        return False, '', '', ''
