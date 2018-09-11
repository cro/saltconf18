import esp
import network

esp.osdebug(None)
STATION = network.WLAN(network.STA_IF);
STATION.active(True)




