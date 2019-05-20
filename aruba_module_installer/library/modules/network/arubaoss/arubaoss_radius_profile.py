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
module: arubaoss_radius_profile

short_description: implements rest api for aaa configuration

version_added: "2.4"

description:
    - "This implements rest apis which can be used to configure RADIUS Server"

options:
    command:
        description: Function name calls according to configuration required
        choices: config_radius_profile,config_radius_serverGroup,config_radius_server
        required: True
    config:
        description: To config or unconfig the required command
        choices: create, delete
        required: False
    retry_interval
        description: The RADIUS server retry interval
        required: False
    retransmit_attempts
        description: The RADIUS server retransmit attempts
        required: False
    dead_time
        description: The RADIUS server dead_time. dead_time cannot set when
                     is_tracking_enabled is true. Input dead_time as null to
                     reset the value. dead_time is indicated as null instead of '0' in CLI
        required: False
    dyn_autz_port
        description: The RADIUS dyn_autz_port
        required: False
    key
        description: The RADIUS server key. Input key as empty string to reset the value
        required: False
    tracking_uname
        description: The RADIUS tracking_uname, default is radius-tracking-user
        required: False
    is_tracking_enabled
        description: The RADIUS server for if tracking is enabled . The flag is_tracking_enabled,
                     cannot set to true when dead_time is configured
        required: False
    cppm_details
        description: Username and password combination of CPPM which is used to
                     login to CPPM to download user roles
        required: False
    server_ip
        description: IP Address of the Radius Server
        required: False
    shared_secret
        description: The Radius server shared secret
        required: False
    version
        description: Version of the IP Address used
        choices: IAV_IP_V4. (V6 is not supported via REST)
        required: False
    server_group_name
        description: Server Group name
        required: False
   time_window_type
        description: Time window type
        choices: TW_POSITIVE_TIME_WINDOW, TW_PLUS_OR_MINUS_TIME_WINDOW
        required: False
    server_ip
        description: Radius server hosts. Minimum is 1 servers, and maximum is 3
        required: False
author:
    - Sanju Sadanandan (@hpe)
'''

EXAMPLES = '''
     - name: Updates the radius profile details on system
       arubaoss_radius_profile:
         command: config_radius_profile
         retry_interval: 7
         retransmit_attempts: 5
         dead_time: 12
         dyn_autz_port: 3799
         key: ""
         tracking_uname: "radius-tracking-user"
         is_tracking_enabled: false
         cppm_details: null
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.arubaoss.arubaoss import run_commands
from ansible.module_utils.network.arubaoss.arubaoss import arubaoss_argument_spec
from ansible.module_utils.network.arubaoss.arubaoss import get_config
import json

"""
-------
Name: config_radius_profile

Configures port with radius profile config

param request: module

Returns
 Configure the switch with params sent
-------
"""
def config_radius_profile(module):

    params = module.params

    data = {}
    data['retry_interval'] = params['retry_interval']
    data['retransmit_attempts'] = params['retransmit_attempts']
    data['dyn_autz_port'] = params['dyn_autz_port']
    data['key'] = params['key']
    data['tracking_uname'] = params['tracking_uname']
    data['is_tracking_enabled'] = params['is_tracking_enabled']
    check_presence = get_config(module, '/radius_profile')
    if check_presence:
        newdata = json.loads(check_presence)
    if params['dead_time'] == 0:
        data['dead_time'] = None
    else:
        data['dead_time'] = params['dead_time']
    if params['is_tracking_enabled'] == True:
        if params['dead_time'] != 0:
            return {'msg': "dead_time should be set to 0 when is_tracking_enabled to be changed to true",
                 'changed': False, 'failed': False}
    else:
       if newdata['is_tracking_enabled'] == True and params['dead_time'] != 0:
           return {'msg': "dead_time should be set to 0 to disable is_tracking_enabled",
                'changed': False, 'failed': False}

    data['cppm_details'] = params['cppm_details']

    url = '/radius_profile'
    method = 'PUT'

    result = run_commands(module, url, data, method, check=url)
    return result
"""
-------
Name: config_radius_serverGroup

Configures port with radius server Group details

param request: module

Returns
 Configure the switch with params sent
-------
"""
def config_radius_serverGroup(module):

    params = module.params

    data = {}
    if params['server_ip'] == "" or params['version'] == "":
        return {'msg': "IP Address or version cannot be null",
                'changed': False, 'failed': False}
    else:
        data["server_ip"] = [{'version': params['version'], 'octets': params['server_ip']}]

    if params['server_group_name'] == "":
        return {'msg': "Server group name cannot be null",
                'changed': False, 'failed': False}
    else:
        data["server_group_name"] = params['server_group_name']

    method = 'POST'
    url = '/radius/server_group'
    del_url = '/radius/server_group/' + str(params['server_group_name'])

    if params['config'] == "create":
       method = 'POST'
    else:
       url = del_url
       method = 'DELETE'

    result = run_commands(module, url, data, method, check=del_url)
    return result

"""
-------
Name: config_radius_server

Configures port with radius server details

param request: module

Returns
 Configure the switch with params sent
-------
"""
def config_radius_server(module):

    params = module.params

    data = {}
    data["radius_server_id"] = params['radius_server_id']

    if params['server_ip'] == "" or params['version'] == "":
        return {'msg': "IP Address or version cannot be null",
                'changed': False, 'failed': False}
    else:
        data["address"] = {'version': params['version'], 'octets': params['server_ip']}

    if params['shared_secret'] == "":
        return {'msg': "Shared secret cannot be null",
                'changed': False, 'failed': False}
    else:
        data["shared_secret"] = params['shared_secret']

    data["authentication_port"] = params['authentication_port']
    data["accounting_port"] = params['accounting_port']
    data["is_dyn_authorization_enabled"] = params['is_dyn_authorization_enabled']
    data["time_window_type"] = params['time_window_type']
    data["time_window"] = params['time_window']
    data["is_oobm"] = params['is_oobm']

    create_url = '/radius_servers'
    check_url = '/radius_servers/' + str(params['radius_server_id'])

    if params['config'] == "create":
       # Check if it already exists
       check_presence = get_config(module, check_url)
       if not check_presence:
           url = create_url
           method = 'POST'
       else:
           url = check_url
           method = 'PUT'
    else:
       url = check_url
       method = 'DELETE'

    result = run_commands(module, url, data, method,check=check_url)
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
           choices=['config_radius_profile','config_radius_serverGroup','config_radius_server']),
        config=dict(type='str', required=False, default="create",
           choices=['create','delete']),
        retry_interval=dict(type='int', required=False, default='7'),
        retransmit_attempts=dict(type='int', required=False, default='5'),
        dead_time=dict(type='int', required=False, default='10'),
        dyn_autz_port=dict(type='int', required=False, default=3799),
        key=dict(type='str', required=False, default=""),
        tracking_uname=dict(type='str', required=False, default='radius-tracking-user'),
        is_tracking_enabled=dict(type='bool', required=False, default=False),
        cppm_details=dict(type='str', required=False, default='0'),
        server_ip=dict(type='str', required=False, default=""),
        shared_secret=dict(type='str', required=False, default=""),
        version=dict(type='str', required=False, default="IAV_IP_V4",
            choices=["IAV_IP_V4"]),
        server_group_name=dict(type='str', required=False, default=""),
        radius_server_id=dict(type='int', required=False, default=1),
        authentication_port=dict(type='int', required=False, default="1812"),
        accounting_port=dict(type='int', required=False, default="1813"),
        is_dyn_authorization_enabled=dict(type='bool', required=False, default=False),
        time_window_type=dict(type='str', required=False, default="TW_POSITIVE_TIME_WINDOW",
            choices=['TW_POSITIVE_TIME_WINDOW', 'TW_PLUS_OR_MINUS_TIME_WINDOW']),
        time_window=dict(type='int', required=False, default="300"),
        is_oobm=dict(type='bool', required=False,default=False),
    )

    module_args.update(arubaoss_argument_spec)

    result = dict(changed=False,warnings='Not Supported')

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    try:
        if module.params['command'] == "config_radius_profile":
            result = config_radius_profile(module)
        elif module.params['command'] == "config_radius_serverGroup":
            result = config_radius_serverGroup(module)
        else:
            result = config_radius_server(module)
    except Exception as err:
        return module.fail_json(msg=err)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
