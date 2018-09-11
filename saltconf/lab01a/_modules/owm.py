
# -*- Coding: utf-8 -*-
'''
Support for OpenWeatherMap
'''

# Import Python libs
from __future__ import absolute_import
import logging
import json

# Import salt libs
from salt.exceptions import CommandExecutionError
import salt.utils.path
import pyowm.exceptions

log = logging.getLogger(__name__)


def __virtual__():
    if 'proxy' not in __opts__:
        return (False, 'This module only works with proxy minions.')
    return True


def weather(place=None):
    '''
    Call the OpenWeatherMap API through a proxy minion.  Return the JSON
    results for weather at a particular place.  Place can be a well-known
    geographic location like Salt Lake City, UT; Disneyland, USA; or 
    Washington, DC or a zipcode (84041).
    '''
    if not place:
        raise CommandExecutionError('owm.weather needs a place or a zipcode.')
    else:
        try:
            # The str() in this line is because OWM will accept
            # a zipcode but Salt and the YAML parser will convert it 
            # to an integer.  OWM wants a string.
            weather_result = __proxy__['owm.api']().weather_at_place(str(place))
            weather_json = weather_result.to_JSON()
        except pyowm.exceptions.api_response_error.NotFoundError:
            return 'Place not found.'

    weather_dictionary = json.loads(weather_json)

    return weather_dictionary
