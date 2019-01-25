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
module: arubaoss_tacacs_profile

short_description: implements rest api for Tacacs configuration

version_added: "2.4"

description:
    - "This implements rest apis which can be used to configure TACACS Server"

options:
    command:
        description: Function name calls according to configuration required
        choices: config_tacacs_profile, config_tacacs_server
        required: True
    config:
        description: To config or unconfig the required command
        choices: create, delete
        required: False
    dead_time
        description: Dead time for unavailable TACACS+ servers
        required: False
    time_out
        description: TACACS server response timeout
        required: False
    global_auth_key
        description: Authentication key
        required: False
    server_ip
        description: TACACS Server IP Address
        required: False
    auth_key
        description: Authentication key
        required: False
    is_oobm
        description: Use oobm interface to connect the server
        required: False
author:
    - Sanju Sadanandan (@hpe)
'''

EXAMPLES = '''
     - name: Updates the given tacacs profile configuration to the system
       arubaoss_tacacs_profile:
         command: config_tacacs_profile
         dead_time: 10
         time_out: 3
         global_auth_key: ""
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.arubaoss.arubaoss import run_commands
from ansible.module_utils.network.arubaoss.arubaoss import arubaoss_argument_spec
from ansible.module_utils.network.arubaoss.arubaoss import get_config

"""
-------
Name: config_tacacs_profile

Configures port with tacacs profile config

param request: module

Returns
 Configure the switch with params sent
-------
"""
def config_tacacs_profile(module):

    params = module.params

    data = {}
    data['dead_time'] = params ['dead_time']
    data['time_out'] = params ['time_out']
    data['global_auth_key'] = params ['global_auth_key']

    url = '/tacacs_profile'
    method = 'PUT'

    result = run_commands(module, url, data, method, check=url)
    return result
"""
-------
Name: config_tacacs_server

Configures port with tacas server

param request: module

Returns
 Configure the switch with params sent
-------
"""
def config_tacacs_server(module):

    params = module.params

    data = {}
    if params['ip_address'] == "" or params['version'] == "":
        return {'msg': "IP Address or version cannot be null",
                'changed': False, 'failed': False}
    else:
        data ["server_ip"] = {"version": params['version'], "octets": params['ip_address']}

    data ["auth_key"] = params ['auth_key']
    data ["is_oobm"] = params ['is_oobm']

    create_url = '/tacacs_profile/server'
    check_url = '/tacacs_profile/server/' + str(params['ip_address'])

    if params['config'] == "create":
       check_presence = get_config(module, '/tacacs_profile/server/' + str(params['ip_address']))
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
        command=dict(type='str', required=False, default="config_tacacs_profile",
            choices=["config_tacacs_profile", "config_tacacs_server"]),
        config=dict(type='str', required=False, default="create",
            choices=["create", "delete"]),
        dead_time=dict(type='int', required=False, default='10'),
        time_out=dict(type='int', required=False, default='0'),
        global_auth_key=dict(type='str', required=False,default=""),
        auth_key=dict(type='str', required=False,default=""),
        ip_address=dict(type='str', required=False,default=""),
        version=dict(type='str', required=False,default=""),
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
        if module.params['command'] == "config_tacacs_profile":
            result = config_tacacs_profile(module)
        else:
            result = config_tacacs_server(module)
    except Exception as err:
        return module.fail_json(msg=err)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
