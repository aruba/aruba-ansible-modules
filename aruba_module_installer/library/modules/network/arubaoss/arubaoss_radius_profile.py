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

extends_documentation_fragment:
    - arubaoss_rest

options:
    command:
      description: "Function name calls according to configuration required -
        choice config_radius_profile allows you to configure the switch's global radius server settings
        choice config_radius_server allows you to configure a radius server IP host
        choice config_radius_serverGroup allows you to configure a radius-server group with existing radius server hosts"
      choices: ['config_radius_profile','config_radius_serverGroup','config_radius_server']
      required: True
      type: str
    config:
      description: To config or remove the required command
      choices: ['create','delete']
      required: False
      type: str
    retry_interval:
      description: The RADIUS server retry interval
      default: 7
      required: False
      type: int
    retransmit_attempts:
      description: The RADIUS server retransmit attempts
      default: 5
      type: int
      required: False
    dead_time:
      description: "The RADIUS server dead_time. dead_time cannot set when
        is_tracking_enabled is true. Input dead_time: null to
        reset the value. dead_time is indicated as null instead of '0' in CLI"
      default: 10
      type: int
      required: False
    dyn_autz_port:
      description: Configure the UDP port for dynamic authorization messages.
      default: 3799
      type: int
      required: False
    key:
      description: "Used with config_radius_profile command, Configure the default authentication key for all RADIUS.
        Input key as empty string to reset the value"
      type: str
      required: False
    tracking_uname:
      description: The RADIUS service tracking username
      default: radius-tracking-user
      type: str
      required: False
    is_tracking_enabled:
      description: "The RADIUS server for if tracking is enabled . The flag is_tracking_enabled,
        cannot set to true when dead_time is configured"
      required: False
    cppm_details:
      description: "Username and password combination of CPPM which is used to
        login to CPPM to download user roles, dictionary should be in the form: {'username':'superman','password': 'arubAn3tw0rks'}"
      type: dict
      required: False
    server_ip:
      description: "Used with config_radius_server or config_radius_serverGroup -
        Radius server hosts IP address. Minimum is 1 servers, and maximum is 3"
      type: str
      required: False
    shared_secret:
      description: "Used with config_radius_server command - The Radius server secret key"
      type: str
      required: False
    version:
      description: Version of the IP Address used
      default: IAV_IP_V4
      choices: IAV_IP_V4. (V6 is not supported via REST)
      required: False
    server_group_name:
      description: the AAA Server Group name
      required: False
    time_window_type:
        description: Time window type
        choices: TW_POSITIVE_TIME_WINDOW, TW_PLUS_OR_MINUS_TIME_WINDOW
        required: False
author:
    - Sanju Sadanandan (@hpe)
'''

EXAMPLES = '''
    - name: Configure Radius server 10.0.0.1 with shared secret RADIUS!
      arubaoss_radius_profile:
        command: config_radius_server
        server_ip: 10.0.0.1
        shared_secret: "RADIUS!"

    - name: Configure Global Radius Profile key
      arubaoss_radius_profile:
        command: config_radius_profile
        key: "RADIUS!"

    - name: Configure Radius Profile CPPM details for User Roles
      arubaoss_radius_profile:
        command: config_radius_profile
        cppm_details: {'username':'superman','password': 'upupandaway'}

    - name: Configure Radius Server -
      arubaoss_radius_profile:
        command: config_radius_server
        server_ip: 10.0.0.1
        shared_secret: "RADIUS!"
        is_dyn_authorization_enabled: True
        time_window: 0

    - name: Configure Radius Server Group
      arubaoss_radius_profile:
        command: config_radius_serverGroup
        server_ip: 10.0.0.1
        server_group_name: SUPER

    - name: Configure Radius server 10.1.1.1 with shared secret ARUBA!
      arubaoss_radius_profile:
        command: config_radius_server
        server_ip: 10.1.1.1
        shared_secret: "ARUBA!"

    - name: Configure Radius server group
      arubaoss_radius_profile:
        command: config_radius_serverGroup
        server_group_name: AVENGERS
        server_ip: 10.1.1.1
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.arubaoss.arubaoss import run_commands
from ansible.module_utils.network.arubaoss.arubaoss import arubaoss_argument_spec, arubaoss_required_if
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
        cppm_details=dict(type='dict', required=False, default=None),
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
        required_if=arubaoss_required_if,
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
