import configparser
import os

config = configparser.ConfigParser()
def activate(proto, ipaddr, puerto, yesno):
    if yesno == True:
        if proto == 'socks':
            pass
        elif proto == 'http':
            os.environ["http_proxy"] = 'http://' + ipaddr + ':' + puerto
            os.environ["https_proxy"] = 'http://' + ipaddr + ':' + puerto
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
        config.write(open("Config.ini", "w"))
        if enabled == True: activate(proto, ipaddr, puerto, True)
        else: activate(proto, ipaddr, puerto, False)
        return True
    except Exception as e:
        print('Error occurred: ' + str(e))
        return False

def ReadCfg():
    try:
        config.read("Config.ini")
        ena = config.get("Proxy", "Enabled").strip()
        enabled = True if ena == 'True' else False
        proto = config.get("Proxy", "Protocol").strip()
        ipaddr = config.get("Proxy", "IPAddr").strip()
        puerto = config.get("Proxy", "Port").strip()
        return enabled, proto, ipaddr, puerto
    except Exception as e:
        print('Error occurred: ' + str(e))
        return False, '', '', ''
