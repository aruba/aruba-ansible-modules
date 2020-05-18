#!/usr/bin/python
#
# Copyright (c) 2020 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: arubaoss_ntp

short_description: implements rest api for NTP configuration

version_added: "2.4"

description:
    - "This implements rest apis which can be used to configure NTP"

extends_documentation_fragment:
    - arubaoss_rest

options:
    command:
        description: To configure a specific feature of NTP -
          choice config_timesync allows you to configure the switch's timesync
          choice enable_includeCredentials allows you to enable include credentials on the switch, either Encrypt Credentials or Include Credentials must be enabled to use key-id authentication with this module
          choice config_ntp allows you to enable/disable and configure switch's global NTP settings
          choice config_ntp_ipv4addr allows you to configure an NTP server with IPv4 address or hostname
          choice config_ntp_keyId allows you to configure an authentication key to use
        choices: ['config_timesync', 'enable_includeCredentials', 'config_ntp', 'config_ntp_ipv4addr', 'config_ntp_keyId']
        required: True
    config:
        description: To config or unconfig the required command
        choices: create, delete
    ntp_ip4addr:
        description: The IPv4 address of the server used with config_ntp_ipv4addr command
        required: False
    minpoll_value:
        description: Configures the minimum time interval in seconds used with config_ntp_ipv4addr command
        required: False
    maxpoll_value:
        description: Configures the maximum time interval in seconds used with config_ntp_ipv4addr command
        required: False
    mode:
        description: Enable burst or iburst mode used with config_ntp_ipv4addr command
        choices: ['burst', 'iburst']
        required: False
    keyId:
        description: Sets the authentication key to use for this server used with config_ntp_ipv4addr and config_ntp_keyId command
        required: False
    timesyncType:
        description: Updates the timesync type  used with config_timesync command
        choices: ['burst', 'iburst']
        required: False
    include_credentials_in_response:
        description: Enables include credentials when value is set to ICS_ENABLED  used with enable_includeCredentials command
        choices: [ICS_ENABLED, ICS_DISABLED, ICS_RADIUS_TACAS_ONLY]
        required: False
    operate:
        description: Operate in broadcast or unicast mode  used with config_ntp command
        choices: [broadcast, unicast]
        required: False
    association_value:
        description: Maximum number of NTP associations used with config_ntp command
        required: False
    trap_value:
        description: Enable or disable traps used with config_ntp command, list of dictionary vaules of enable and trap, see example below.
        type: list of dictionaries
        enable:
            description: enable or disable traps
            choices: True, False
            required: False
        trap:
            description: Select trap variable
            choices: "ntp-Mode-Change",
                     "ntp-Stratum-Change",
                     "ntp-Peer-Change",
                     "ntp-New-Association",
                     "ntp-Remove-Association",
                     "ntp-Config-Change",
                     "ntp-LeapSec-announced",
                     "Ntp-alive-Heartbeat",
                     "all"
        required: true
    keyValue:
        description: The string to be added to authentication KeyId used with config_ntp_keyId command
        required: False
    use_oobm:
        description: Use the OOBM interface to connect to the server used with config_ntp_ipv4addr command. Note not all devices have OOBM ports
        choices: True, False
        required: False

author:
    - Sanju Sadanandan (@hpe)
'''

EXAMPLES = '''
      - name: configure timesync to be ntp
        arubaoss_ntp:
          command: "config_timesync"
          timesyncType: ntp

      - name: Enable NTP
        arubaoss_ntp:
          command: "config_ntp"
          config: create

      - name: Enable NTP in Unicast
        arubaoss_ntp:
          command: "config_ntp"
          config: create
          operate: "unicast"

      - name: Enable include Credentials
        arubaoss_ntp:
          command: "enable_includeCredentials"
          include_credentials_in_response: "ICS_ENABLED"

      - name: Configure ntp authentication keyID 2
        arubaoss_ntp:
          command: "config_ntp_keyId"
          authenticationMode: sha1
          keyId: 2
          keyValue: ARUBA
          trusted: True

      - name: Configure ntp server with keyID
        arubaoss_ntp:
          command: "config_ntp_ipv4addr"
          ntp_ip4addr: "10.20.40.33"
          keyId: 2
          mode: "iburst"

      - name: Configure ntp server 10.20.60.33 with iburst and using OOBM
        arubaoss_ntp:
          command: "config_ntp_ipv4addr"
          ntp_ip4addr: "10.20.60.33"
          mode: "iburst"
          use_oobm: True

      - name: configure ntp server time1.google.com
        arubaoss_ntp:
          command: "config_ntp_ipv4addr"
          ntp_ip4addr: "time1.google.com"
          mode: "iburst"

      - name: delete ntp server time1.google.com
        arubaoss_ntp:
          command: "config_ntp_ipv4addr"
          ntp_ip4addr: "time1.google.com"
          mode: "iburst"
          config: delete

      - name: Add NTP traps
        arubaoss_ntp:
          command: "config_ntp"
          config: create
          trap_value:
            - trap: "ntp-Stratum-Change"
            - trap: "ntp-Mode-Change"
            - trap: "ntp-Peer-Change"

      - name: Remove NTP traps
        arubaoss_ntp:
          command: "config_ntp"
          config: create
          trap_value:
            - enable: False
              trap: "ntp-Peer-Change"
            - enable: False
              trap: "ntp-Mode-Change"

      - name: Remove all NTP traps
        arubaoss_ntp:
          command: "config_ntp"
          trap_value:
            - enable: False
              trap: "all"
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.arubaoss.arubaoss import run_commands
from ansible.module_utils.network.arubaoss.arubaoss import arubaoss_argument_spec, arubaoss_required_if
from ansible.module_utils.network.arubaoss.arubaoss import get_config
import json
import socket

"""
-------
Name: config_present

Check if configuration is present

param request: module,
               url: url from which we need to fetch the data
               key: key which can be used to search from the fetched data
               values: value for the searched key
Returns
 return true if config is present else false
-------
"""


def config_present(module, url, key, value):
    check_presence = get_config(module, url)
    if check_presence:
        newdata = json.loads(check_presence)
        if key in newdata.keys():
            if newdata[key] == value:
                return True
    return False


"""
-------
Name: config_timesync

Configures timesync

param request: module

Returns
 Configure the switch with params sent
-------
"""


def config_timesync(module):
    params = module.params
    data = {}

    # Parameters
    timesyncType = params['timesyncType']

    data[timesyncType] = True

    # URI
    url = "/config/timesync"
    method = "PUT"

    # Check if timesync is set already
    check_presence = get_config(module, "/config/timesync")
    newdata = json.loads(check_presence)
    if timesyncType == 'ntp' and 'ntp' in newdata:
        return {'msg': 'timesync already set to NTP',
                'changed': False, 'failed': False}
    elif timesyncType == 'timep' and 'timep' in newdata:
        return {'msg': 'timesync already set to Timep',
                'changed': False, 'failed': False}
    elif timesyncType == 'sntp' and 'sntp' in newdata:
        return {'msg': 'timesync already set to SNTP',
                'changed': False, 'failed': False}
    elif timesyncType == 'timep-or-sntp' and 'timep-or-sntp' in newdata:
        return {'msg': 'timesync already set to timep or SNTP',
                'changed': False, 'failed': False}
    else:
        # Config
        result = run_commands(module, url, data, method)
        return result


"""
------
Name: enable_includeCredentials

Enabled Include Credentials on switch

param request: module

Returns
 Configure the switch with params sent
-------
"""


def enable_includeCredentials(module):
    params = module.params
    data = {}

    # Parameters
    data['include_credentials_in_response'] = params['include_credentials_in_response']

    # URI
    url = "/system/include-credentials"
    method = "PUT"

    # Config
    result = run_commands(module, url, data, method, check=url)
    return result


"""
-------
Name: config_ntp

Configures NTP Service  on switch

param request: module

Returns
 Configure the switch with params sent
-------
"""


def config_ntp(module):
    params = module.params
    data = {}

    # Check if timesync is set to NTP
    if config_present(module, "/config/timesync", "ntp", True) is False:
        return {'msg': 'timesync should be set to NTP',
                'changed': False, 'failed': True}

    # Parameters
    # unicast or broadcast are mutually exclusive
    if params['operate'] == "unicast":
        data['unicast'] = True
    else:
        data['broadcast'] = True

    data['max-association'] = {
        'max-association_value': params['association_value']}

    if params['config'] == "create":
        data['enable'] = True
    else:
        data['enable'] = False

    if params['trap_value'] is not None:
        data['trap'] = []
        for item in params['trap_value']:
            trap_dict = {'trap_value': item['trap']}
            if 'enable' in item and item['enable'] == False:
                trap_dict['cmd_no_form'] = True
            data['trap'].append(trap_dict)

    # URI
    url = "/config/ntp"
    method = "PUT"

    # Config
    result = run_commands(module, url, data, method, check=url)
    return result


"""
-------
Name: config_ntp_keyId

Configures NTP Server with Key Id

param request: module

Returns
 Configure the switch with params sent
-------
"""


def config_ntp_keyId(module):
    params = module.params
    data = {}
    include_cred = False
    encrypt_cred = False

    # Verify ntp is enabled
    if config_present(module, "/config/ntp", "enable", True) is False:
        return {'msg': 'NTP should be enabled',
                'changed': False, 'failed': True}

    # Verify include credentials is enabled
    if config_present(module, "/system/include-credentials",
                      "include_credentials_in_response",
                      "ICS_DISABLED") is False:
        include_cred = True

    # Verify include credentials is enabled
    if config_present(module, "/system/encrypt-credentials",
                      "encryption",
                      "ECS_DISABLED") is False:
        encrypt_cred = True

    if not (encrypt_cred or include_cred):
        return {'msg': 'Enable Encrypt Credentials or Include Credentials to'
                       ' use or configure key-id authentication',
                'changed': False, 'failed': True}

    # URI
    check_url = "/config/ntp/authentication/key-id/int/" + str(params['keyId'])
    url = "/config/ntp/authentication/key-id/int"

    if params['config'] == "delete":
        check_presence = get_config(module, "/config/ntp/server/ip4addr")
        if check_presence:
            newdata = json.loads(check_presence)
            if len(newdata['ntpServerIp4addr_element']) != 0:
                for ipadd_ele in newdata['ntpServerIp4addr_element']:
                    if ipadd_ele['ip4addr']['ip4addr_reference']['key-id']['key-id_value'] == params['keyId']:
                        return {
                            'msg': 'NTP Server IP should be cleared befere deleting NTP Key ID',
                            'changed': False, 'failed': True}
        url = check_url
        method = "DELETE"
        data = ""

        result = run_commands(module, url, data, method)
        return result

    # This returns an empty list if encrypt credentials is not enabled
    # This does not properly check if the key-id exists
    # Verify if key is already a trusted entry
    check_presence = get_config(module, check_url)
    if check_presence:
        newdata = json.loads(check_presence)
        if params['authenticationMode'] in newdata['int']['int_reference'][
            'authentication-mode'].keys():
            return {'msg': 'Key-ID {} exists'.format(params['keyId']),
                    'changed': False, 'failed': False}

    if params['keyValue'] == "":
        return {'msg': 'KeyValue parameter is mandatory',
                'changed': False, 'failed': True}

    # Parameters
    data["int"] = {
        "int_value": int(params['keyId']),
        "int_reference": {
            "authentication-mode": {
                params['authenticationMode']: {
                    "key-value": {
                        "key": {
                            "key_reference": {
                                "trusted": params['trusted']
                            },
                            "key_value": params['keyValue']
                        }
                    }
                }
            }
        }
    }

    # Config
    if params['config'] == "create":
        # check if already present
        check_presence = get_config(module, check_url)
        if not check_presence:
            method = "POST"
        else:
            url = check_url
            method = "PUT"
    # This will fail if key-id exists already, looking into a try/except
    result = run_commands(module, url, data, method, check=check_url)
    return result


"""
-------
Name: config_ntp_ipv4addr

Configures NTP Server of IPv4 address on switch

param request: module

Returns
 Configure the switch with params sent
-------
"""


def config_ntp_ipv4addr(module):
    params = module.params
    ip4_addr = "ip4addr"
    ip4_addr_val = "ip4addr_value"
    ip4_addr_ref = "ip4addr_reference"
    server = "server"
    address = str(params['ntp_ip4addr'])
    try:
        socket.inet_aton(params['ntp_ip4addr'])
    except:
        check_presence = get_config(module, "/dns")
        newdata = json.loads(check_presence)
        value = [newdata["server_1"], newdata["server_2"], newdata["server_3"],
                 newdata["server_4"]]
        if value.count(None) == 4:
            return {
                'msg': 'A DNS server must be configured before configuring NTP unicast server name',
                'changed': False, 'failed': True}

        ip4_addr = "ASCII-STR"
        ip4_addr_ref = "ASCII-STR_reference"
        ip4_addr_val = "ASCII-STR_value"
        server = "server-name"
        address = "%22" + str(params['ntp_ip4addr']) + "%22"

    # Verify ntp is enabled
    if (config_present(module, "/config/ntp", "enable", True) == False):
        return {'msg': 'NTP should be enabled',
                'changed': False, 'failed': True}

    data = {}
    if params['ntp_ip4addr'] is "":
        return {'msg': 'IP Address cannot be null',
                'changed': False, 'failed': True}
    else:
        data[ip4_addr] = {
            ip4_addr_ref: {
                'max-poll': {'max-poll_value': params['maxpoll_value']},
                'min-poll': {'min-poll_value': params['minpoll_value']},
            },
            ip4_addr_val: params['ntp_ip4addr']
        }

    if params['keyId'] and params['keyId'] is not 0:
        # This returns an empty list if encrypt credentials is not enabled
        # Verify the key is trusted
        check_presence = get_config(module,
                                    "/config/ntp/authentication/key-id/int/" + str(
                                        params['keyId']))
        if not check_presence:
            return {
                'msg': 'Authentication key-id {} needs to be configured to configure ipv4 server'.format(
                    params['keyId']),
                'changed': False, 'failed': True}

        keyVal = {}
        keyVal = {'key-id': {'key-id_value': params['keyId']}}
        data[ip4_addr][ip4_addr_ref].update(keyVal)

    # Configuring burst ot iburst
    if params['mode'] == "burst" or params['mode'] == "iburst":
        mode = {}
        mode = {params['mode']: True}
        data[ip4_addr][ip4_addr_ref].update(mode)

    # Configuring OOBM
    if params['use_oobm'] is True:
        use_oobm = {}
        use_oobm = {'oobm': params['use_oobm']}
        data[ip4_addr][ip4_addr_ref].update(use_oobm)

    # URIs
    url = "/config/ntp/" + server + "/" + ip4_addr
    check_url = url + "/" + address
    # idempotency check for ipv4addr addition
    diffseen = False
    check_presence = get_config(module, check_url)
    if check_presence:
        newdata = json.loads(check_presence)
        for key in data:
            if key == "ASCII-STR":
                # host name comes in the format "\"time2.google.com\"".
                # So removing '\"' to compare.
                newdata[key][ip4_addr_val] = newdata[key][ip4_addr_val].strip(
                    '\"')

            if not newdata[key] == data[key]:
                diffseen = True
                break
    else:
        diffseen = True

    if params['config'] == "create":
        # If a difference in desired state delete old configuration
        if diffseen:
            run_commands(module, check_url, data, method='DELETE')

        # Check if a server ip is already configured
        check_presence = get_config(module, check_url)
        if not check_presence:
            method = 'POST'
        else:
            method = 'PUT'
            url = check_url

    elif params['config'] == "delete":
        url = check_url
        method = 'DELETE'
    else:
        return {'msg': 'Valid config options are : create and delete',
                'changed': False, 'failed': True}

    # When address is in host name format, "check" in run_commands will not work.
    # so adding the additional check to verify idempotency
    if ip4_addr == "ASCII-STR" and diffseen == False and method != 'DELETE':
        return {'msg': 'Configuration already exists',
                'changed': False, 'failed': False}
    result = run_commands(module, url, data, method, check=check_url)
    try:
        if result['status'] == 400:
            newdata = json.loads(result['body'])
            return {'msg': newdata['config_error'][0]['error'],
                'changed': False, 'failed': True}
        else :
            return result
    except:
        return result

"""
-------
Name: run_module()

The main module invoked

Returns
 Configure the switch with params sent
-------
"""


def run_module():
    module_args = dict(
        command=dict(type='str', required=True,
                     choices=["config_timesync",
                              "enable_includeCredentials",
                              "config_ntp",
                              "config_ntp_keyId", "config_ntp_ipv4addr"]),
        config=dict(type='str', required=False, default="create",
                    choices=["create", "delete"]),
        timesyncType=dict(type='str', required=False,
                          default="timep-or-sntp",
                          choices=["ntp", "sntp", "timep",
                                   "timep-or-sntp"]),
        operate=dict(type='str', required=False, default="broadcast",
                     choices=["broadcast",
                              "unicast"]),
        association_value=dict(type='int', required=False, default=8),
        trap_value=dict(type='list', required=False,
                        enable=dict(type='bool', required=False,
                                    default=False),
                        trap=dict(type='str', required=True,
                                  choices=["ntp-Mode-Change",
                                           "ntp-Stratum-Change",
                                           "ntp-Peer-Change",
                                           "ntp-New-Association",
                                           "ntp-Remove-Association",
                                           "ntp-Config-Change",
                                           "ntp-LeapSec-announced",
                                           "Ntp-alive-Heartbeat", "all"])),
        ntp_ip4addr=dict(type='str', required=False, default=""),
        maxpoll_value=dict(type='int', required=False, default=10),
        minpoll_value=dict(type='int', required=False, default=6),
        mode=dict(type='str', required=False, default="burst",
                  choices=["burst", "iburst"]),
        include_credentials_in_response=dict(type='str', required=False,
                                             default="ICS_ENABLED",
                                             choices=['ICS_ENABLED',
                                                      'ICS_DISABLED',
                                                      'ICS_RADIUS_TACAS_ONLY']),
        keyId=dict(type='int', required=False, default=0),
        trusted=dict(type='bool', required=False, default=True),
        keyValue=dict(type='str', required=False, default=""),
        authenticationMode=dict(type='str', required=False, default="md5",
                                choices=["md5", "sha1"]),
        use_oobm=dict(type='bool', required=False, default=False),
    )

    module_args.update(arubaoss_argument_spec)

    result = dict(changed=False)

    module = AnsibleModule(
        required_if=arubaoss_required_if,
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    try:
        if module.params['command'] == "config_timesync":
            result = config_timesync(module)
        elif module.params['command'] == "enable_includeCredentials":
            result = enable_includeCredentials(module)
        elif module.params['command'] == "config_ntp":
            result = config_ntp(module)
        elif module.params['command'] == "config_ntp_ipv4addr":
            result = config_ntp_ipv4addr(module)
        else:
            result = config_ntp_keyId(module)
    except Exception as err:
        return module.fail_json(msg=err)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
