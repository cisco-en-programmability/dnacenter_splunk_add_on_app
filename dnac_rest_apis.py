
# -*- coding: utf-8 -*-
"""

Cisco DNA Center Command Runner

Copyright (c) 2019 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""

__author__ = "Gabriel Zapodeanu TME, ENB"
__email__ = "gzapodea@cisco.com"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2020 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"


import os
import sys
import time
import datetime
import requests
import urllib3
import json

from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings
from requests.auth import HTTPBasicAuth  # for Basic Auth

urllib3.disable_warnings(InsecureRequestWarning)  # disable insecure https warnings


# Cisco DNA Center info

username = 'username'
password = 'password'
DNAC_URL = 'https://cisco_dnac'


DNAC_AUTH = HTTPBasicAuth(username, password)


def get_dnac_jwt_token(dnac_auth):
    """
    Create the authorization token required to access DNA C
    Call to Cisco DNA Center - /api/system/v1/auth/login
    :param dnac_auth - Cisco DNA Center Basic Auth string
    :return: Cisco DNA Center JWT token
    """
    url = DNAC_URL + '/dna/system/api/v1/auth/token'
    header = {'content-type': 'application/json'}
    response = requests.post(url, auth=dnac_auth, headers=header, verify=False)
    dnac_jwt_token = response.json()['Token']
    return dnac_jwt_token


def get_all_device_info(limit, dnac_jwt_token):
    """
    The function will return all network devices info, using the specified limit of devices/API Call
    :param limit: the number of devices to return per API call
    :param dnac_jwt_token: Cisco DNA C token
    :return: DNA C device inventory info
    """
    offset = 1
    all_devices_list = []
    all_devices_info = ['']  # assign a value, to make sure the API call will run at least once
    while all_devices_info:
        all_devices_info = ''
        url = DNAC_URL + '/dna/intent/api/v1/network-device?offset=' + str(offset) + '&limit=' + str(limit)
        header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
        all_devices_response = requests.get(url, headers=header, verify=False)
        all_devices_json = all_devices_response.json()
        all_devices_info = all_devices_json['response']
        all_devices_list += all_devices_info
        offset += limit
    return all_devices_list


def get_all_device_dict(limit, dnac_jwt_token):
    """
    The function will return all network devices info, using the specified limit of devices/API Call
    :param limit: the number of devices to return per API call
    :param dnac_jwt_token: Cisco DNA C token
    :return: DNA C device inventory info
    """
    offset = 1
    all_devices_dict = {}
    all_devices_list = []
    all_devices_info = ['']  # assign a value, to make sure the API call will run at least once
    while all_devices_info:
        while all_devices_info:
            all_devices_info = ''
            url = DNAC_URL + '/dna/intent/api/v1/network-device?offset=' + str(offset) + '&limit=' + str(limit)
            header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
            all_devices_response = requests.get(url, headers=header, verify=False)
            all_devices_json = all_devices_response.json()
            all_devices_info = all_devices_json['response']
            all_devices_list += all_devices_info
            offset += limit
    for device in all_devices_list:
        all_devices_dict.update({device['hostname']: device})
    return all_devices_dict


def get_overall_network_health(dnac_jwt_token):
    """
    This function will retrieve the network health at the time the function is called
    :param dnac_jwt_token: Cisco DNA C token
    :return: network health
    """
    epoch_time = get_epoch_current_time()
    url = DNAC_URL + '/dna/intent/api/v1/network-health?timestamp=' + str(epoch_time)
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    network_health_response = requests.get(url, headers=header, verify=False)
    network_health_json = network_health_response.json()
    network_health = {'overall_network_health': network_health_json['response'][0]['healthScore']}
    for device_group in network_health_json['healthDistirubution']:
        network_health.update({device_group['category']: device_group['healthScore']})  # merge the device category health
    return network_health


def pprint(json_data):
    """
    Pretty print JSON formatted data
    :param json_data:
    :return:
    """
    print(json.dumps(json_data, indent=4, separators=(' , ', ' : ')))


def get_epoch_current_time():
    """
    This function will return the epoch time for the {timestamp}
    :return: epoch time including msec
    """
    epoch = time.time()*1000
    return int(epoch)


def main():
    # get the Cisco DNA Center Auth
    dnac_auth = get_dnac_jwt_token(DNAC_AUTH)

    # get all the devices info, 500 devices collect per each API call (this is the max), print them as list
    # all_devices_info = get_all_device_info(500, dnac_auth)
    # print(json.dumps(all_devices_info))  # save the all devices info to Splunk App index

    # get all the devices info, 500 devices collect per each API call (this is the max), print them as dict
    all_devices_info_dict = get_all_device_dict(5, dnac_auth)
    print(json.dumps(all_devices_info_dict))  # save the all devices info to Splunk App index

    # get the overall network health
    overall_network_health = get_overall_network_health(dnac_auth)
    print(json.dumps(overall_network_health))  # save the network health to Splunk App index


if __name__ == '__main__':
    main()


