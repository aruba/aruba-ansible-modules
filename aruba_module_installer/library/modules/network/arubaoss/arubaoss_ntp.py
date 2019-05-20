#!/usr/bin/python
#
# Copyright (c) 2019 Hewlett Packard Enterprise Development LP
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

options:
    command:
        description: To config or unconfig the required command
        choices: config_timesync, enable_includeCredentials, config_ntp,
                 config_ntp_keyId, config_ntp_ipv4addr
        required: False
    ntp_ip4addr:
        description: The IPv4 address of the server
        required: False
    minpoll_value:
        description: Configures the minimum time interval in seconds
        required: False
    maxpoll_value:
        description: Configures the maximum time interval in seconds
        required: False
    burst:
        description: Enables burst mode
        required: False
    iburst:
        description: Enables initial burst mode
        required: False
    keyId:
        description: Sets the authentication key to use for this server
        required: False
    timesyncType:
        description: Updates the timesync type, takes values: ntp, sntp, timep
                     and timep-or-sntp
        required: False
    include_credentials_in_response:
        description: Enables include credentials when value is set to ICS_ENABLED
        choices: ICS_ENABLED, ICS_DISABLED, ICS_RADIUS_TACAS_ONLY
        required: False
    broadcast:
        description: Operate in broadcast mode
        required: False
    association_value:
        description: Maximum number of NTP associations
        required: False
    trap_value:
        description: Sets trap type
        required: False
    keyValue:
        description: The string to be added to authentication KeyId
        required: False

author:
    - Sanju Sadanandan (@hpe)
'''

EXAMPLES = '''
     - name: Updates the  system with NTP Server configuration
       arubaoss_ntp:
         command: "config_ntp_ipv4addr"
         config: "create"
         ntp_ip4addr: "10.20.40.33"
         keyId: 2
         burst: True
         iburst: True
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.arubaoss.arubaoss import run_commands
from ansible.module_utils.network.arubaoss.arubaoss import arubaoss_argument_spec
from ansible.module_utils.network.arubaoss.arubaoss import get_config
import json

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
    elif timesyncType == 'timep-or-sntp'  and 'timep-or-sntp' in newdata:
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
    check_presence = get_config(module, "/config/timesync")
    newdata = json.loads(check_presence)
    if not 'ntp' in newdata:
        return {'msg': 'timesync should be set to NTP',
                'changed': False, 'failed': False}

    # Parameters
    data['broadcast'] = params['broadcast']
    #data['unicast'] = params['unicast']

    data['max-association'] = {'cmd_no_form': params['cmd_no_form'],
                'max-association_value': params['association_value']}

    if params['config'] == "create":
        data['enable'] = True
    else:
        data['enable'] = False

    if params['trap_cmd_no_form'] == "True" and params['trap_value'] == "":
        return {'msg': 'trap-value cannot be null',
                'changed': False, 'failed': False}
    else:
        data['trap'] = [{'cmd_no_form': params['trap_cmd_no_form'], \
                'trap_value': params['trap_value']}]

    # URI
    url = "/config/ntp"
    method = "PUT"
    #print data

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

    # Verify ntp is enabled
    check_presence = get_config(module, "/config/ntp")
    if not check_presence:
        return {'msg': 'NTP should be enabled',
                'changed': False, 'failed': False}

    # Verify include credentials is enabled
    check_presence = get_config(module, "/system/include-credentials")
    if not check_presence:
        return {'msg': 'Include Credentials should be enabled',
                'changed': False, 'failed': False}

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
                        return {'msg': 'NTP Server IP should be cleared befere deleting NTP Key ID',
                            'changed': False, 'failed': False}
        url = check_url
        method = "DELETE"
        data=""

        result = run_commands(module, url, data, method)
        return result

    # Verify if key is already a trusted entry
    check_presence = get_config(module, check_url)
    if check_presence:
        newdata = json.loads(check_presence)
        if newdata['int']['int_reference']['authentication-mode']['md5']:
            if newdata['int']['int_reference']['authentication-mode']['md5']['key-value']['key']['key_reference']['trusted'] == True:
                return {'msg': 'Key is already a trusted entry',
                    'changed': False, 'failed': False}
        if newdata['int']['int_reference']['authentication-mode']['sha1']:
            if newdata['int']['int_reference']['authentication-mode']['sha1']['key-value']['key']['key_reference']['trusted'] == True:
                return {'msg': 'Key is already a trusted entry',
                    'changed': False, 'failed': False}
    if params['keyValue'] == "":
        return {'msg': 'KeyValue parameter is mandatory',
            'changed': False, 'failed': False}


    # Parameters
    data["int"] = {
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
        },
        "int_value": params['keyId']}

    # Config
    if params['config'] == "create":
        # check if already present
        check_presence = get_config(module, check_url)
        if not check_presence:
            method = "POST"
        else:
            url = check_url
            method = "PUT"

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

    # Verify ntp is enabled
    check_presence = get_config(module, "/config/ntp")
    if not check_presence:
        return {'msg': 'NTP should be enabled',
                'changed': False, 'failed': False}

    # Verify the key is trusted
    check_presence = get_config(module, "/config/ntp/authentication/key-id/int/" + str(params['keyId']))
    if not check_presence:
        return {'msg': 'Authentication key-id 2 needs to be configured to configure ipv4 server',
            'changed': False, 'failed': False}
    data = {}
    if params['ntp_ip4addr'] is "":
        return {'msg': 'IP Address cannot be null',
                'changed': False, 'failed': False}
    else:
        data['ip4addr'] = {
                      'ip4addr_reference': {
                         'max-poll': {'max-poll_value': params['maxpoll_value']},
                         'min-poll': {'min-poll_value': params['minpoll_value']},
                                           },
                      'ip4addr_value': params['ntp_ip4addr']
                      }

    if params['keyId'] is not 0:

        keyVal = {}
        keyVal = {'key-id': {'key-id_value': params['keyId']}}
        data['ip4addr']['ip4addr_reference'].update(keyVal)

    # Sanju: Changed from "" to False
    if params['iburst'] is True:
        iburst = {}
        iburst = {'iburst' :  params['iburst']}
        data['ip4addr']['ip4addr_reference'].update(iburst)

    # ISSUE: These values throw error: Error: JSON OneOf validation failed: 'burst'
    #if params['burst'] is True:
    #    burst = {}
    #    burst = {'burst' :  params['burst']}
    #    data['ip4addr']['ip4addr_reference'].update(burst)

    # URIs
    url = "/config/ntp/server/ip4addr"
    check_url = "/config/ntp/server/ip4addr/" + str(params['ntp_ip4addr'])
    #idempotency check for ipv4addr addition
    diffseen = False
    check_presence = get_config(module, check_url)
    if check_presence:
        newdata = json.loads(check_presence)
        for key in data:
            if not newdata[key] == data[key]:
               diffseen = True
               break
    else:
       diffseen = True
    if diffseen:
        # Config
        if params['config'] == "create":

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
                    'changed': False, 'failed': False}

        result = run_commands(module, url, data, method, check=check_url)
        return result
    else:
       return {'msg': 'Config already present.',
                    'changed': False, 'failed': False}


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
        command=dict(type='str', required=False, default="config_ntp",
            choices=["config_timesync", "enable_includeCredentials", "config_ntp", "config_ntp_keyId", "config_ntp_ipv4addr"]),
        config=dict(type='str', required=False, default="create",
            choices=["create", "delete"]),
        sntp=dict(type='bool', required=False, default=False),
        timep=dict(type='bool', required=False, default=False),
        timepOrSntp=dict(type='bool', required=False, default=False),
        timesyncType=dict(type='str', required=False, default="ntp",
            choices=["ntp", "sntp", "timep", "timep-or-sntp"]),
        broadcast=dict(type='bool', required=False, default=True),
        unicast=dict(type='bool', required=False, default=False),
        cmd_no_form=dict(type='bool', required=False, default=False),
        association_value=dict(type='int', required=False, default=8),
        trap_cmd_no_form=dict(type='bool', required=False, default=False),
        trap_value=dict(type='str', required=False, default=""),
        ntp_ip4addr=dict(type='str', required=False, default=""),
        maxpoll_value=dict(type='int', required=False, default=10),
        minpoll_value=dict(type='int', required=False, default=6),
        burst=dict(type='bool', required=False, default=False),
        iburst=dict(type='bool', required=False, default=False),
        include_credentials_in_response=dict(type='str', required=False, default="ICS_ENABLED",
           choices = ['ICS_ENABLED','ICS_DISABLED','ICS_RADIUS_TACAS_ONLY']),
        keyId=dict(type='int', required=False, default=1),
        trusted=dict(type='bool', required=False, default=True),
        keyValue=dict(type='str', required=False, default=""),
        authenticationMode=dict(type='str', required=False, default="md5"),
    )

    module_args.update(arubaoss_argument_spec)

    result = dict(changed=False)

    module = AnsibleModule(
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
