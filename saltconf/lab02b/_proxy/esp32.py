# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import os.path
# Import python libs
import salt.utils.path
import logging
import tempfile

# Variables are scoped to this module so we can have persistent data
# across calls to fns in here.
GRAINS_CACHE = {}
DETAILS = {}

# Want logging!
log = logging.getLogger(__file__)

__proxyenabled__ = ['esp32']

def __virtual__():
    '''
    Check for ampy
    '''
    UPLOADER = salt.utils.path.which('ampy')
    if not UPLOADER:
        return (False, 'The esp32 proxymodule needs access to the ampy utility')
    DETAILS['uploader'] = UPLOADER
    return True


def init(opts):
    log.debug('esp32 init() called...')
    DETAILS['initialized'] = False
    try:
        DETAILS['port'] = opts['proxy']['port']
    except KeyError:
        DETAILS['port'] = '/tmp/ttyV0'
    try:
        DETAILS['baud'] = opts['proxy']['baud']
    except KeyError:
        DETAILS['baud'] = '115200'

    DETAILS['initialized'] = ping()

    return DETAILS['initialized']


def initialized():
    '''
    Since grains are loaded in many different places and some of those
    places occur before the proxy can be initialized, return whether
    our init() function has been called
    '''
    return DETAILS.get('initialized', False)


def ping():

    cmd = [DETAILS['uploader'], '--port', DETAILS['port'], '--baud', DETAILS['baud'], 'ls']

    result = __salt__['cmd.run_all'](cmd)
    if result['retcode'] != 0:
        log.debug('Tried listing files {}'.format(result['stdout']))

    return result['retcode'] == 0


def list_files():

    cmd = ['ampy', '--port', DETAILS['port'], '--baud', DETAILS['baud'],
           'ls']
    list_result = __salt__['cmd.run_all'](cmd)
    if list_result['retcode'] != 0:
        return list_result
        log.debug(list_result)
    else:
        return list_result['stdout'].splitlines()


def reset_esp32():

    cmd = ['ampy', '--port', DETAILS['port'], '--baud', DETAILS['baud'],
            'reset']
    reset_result = __salt__['cmd.run_all'](cmd)
    log.debug(reset_result)
    return reset_result


def upload_file(source):

    ret = __salt__['cp.cache_file'](source)

    if ret:
        path = os.path.dirname(ret)
        filename = os.path.basename(ret)
        cmd = ['ampy', '--port', DETAILS['port'], '--baud', DETAILS['baud'],
                'put', filename]
        upload_result = __salt__['cmd.run_all'](cmd, cwd=path)
        log.debug(upload_result)
        if upload_result['retcode'] == 0:
            return filename
        else:
            return upload_result
    else:
        return '{} not found'.format(source)


def delete_file(filename):

    cmd = ['ampy', '--port', DETAILS['port'], '--baud', DETAILS['baud'],
                'file', 'rm', filename]
    tries = 0
    delete_result = __salt__['cmd.run_all'](cmd)

    if delete_result['retcode'] == 0:
        return True
    else:
        return delete_result


def run_file(name):

    ret = __salt__['cp.cache_file'](name)

    if ret:
        path = os.path.dirname(ret)
        filename = os.path.basename(ret)
        cmd = ['ampy', '--port', DETAILS['port'], '--baud', DETAILS['baud'],
                'run', filename]
        run_result = __salt__['cmd.run_all'](cmd, cwd=path)
        log.debug(run_result)
        if run_result['retcode'] == 0:
            return run_result['stdout']
        else:
            return run_result
    else:
        return '{} not found'.format(source)


def exec_on_board(name):
    '''
    Execute a script from the ESP32 board's filesystem
    '''
    basename = name.split('.')[0]
    stub_code = '''import {}
{}.run()
'''.format(basename, basename)
    with tempfile.NamedTemporaryFile(mode='rw+b') as f:
        f.write(stub_code)
        f.flush()
        f.seek(0)
        cmd = ['ampy', '--port', DETAILS['port'], '--baud', DETAILS['baud'],
                'run', f.name]
        run_result = __salt__['cmd.run_all'](cmd)
        if run_result['retcode'] == 0:
            return run_result['stdout']
        else:
            return run_result


def shutdown(opts):
    '''
    For this proxy shutdown is a no-op
    '''
    log.debug('esp32 proxy shutdown() called...')


