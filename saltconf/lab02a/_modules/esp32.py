# Execution module for interfacing with the esp32 proxyminion.
import json

AUTH_TYPES = ('Open', 'WEP', 'WPA_PSK', 'WPA2_PSK', 'WPA_WPA2_PSK', 'WPA_Enterprise_Mixed')


def upload(name):
    return __proxy__['esp32.upload_file'](name)


def exec_on_board(name):
    return __proxy__['esp32.exec_on_board'](name)


def run(name):
    return __proxy__['esp32.run_file'](name)

    
def list():
    return __proxy__['esp32.list_files']()


def delete(name):
    return __proxy__['esp32.delete_file'](name)


def reset():
    return __proxy__['esp32.reset_esp32']()


def scan():
    return exec_on_board('scan_results.py')

