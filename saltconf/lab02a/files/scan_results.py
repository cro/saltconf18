import json
import time
import network
import binascii

AUTHTYPES = ['Open','WPA-PSK','WPA2_PSK','WPA_WPA2_PSK','WPA_Enterpise']
def scan_for_networks():
    sta_if = network.WLAN(network.STA_IF)
    return sta_if.scan()

def run():
    keys = ['ssid', 'bssid', 'channel', 'rssi', 'authtype', 'hidden']
    edited_networks = {}
    edited_networks['aps'] = {}

    for net in scan_for_networks():
        thisnet_list = list(net)
        thisnet_list[1] = binascii.hexlify(net[1])
        thisnet = dict(zip(keys, thisnet_list))
        try:
            thisnet['authtype'] = AUTHTYPES[thisnet['authtype']]
        except KeyError:
            pass
        edited_networks['aps'][thisnet['bssid']] = thisnet
    print(json.dumps(edited_networks))


