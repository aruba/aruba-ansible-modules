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
module: arubaoss_aaa_authentication

short_description: implements rest api for AAA Authentication configuration

version_added: "2.4"

description:
    - "This implements rest apis which can be used to configure authentication"

options:
    command:
        description: Function name calls according to configuration required
        choices: config_authentication, config_authentication_console, config_authentication_ssh
        required: False
    is_privilege_mode_enabled:
        description: To enable/disable privilaged mode
        required: False
    primary_method:
        description: The primary authentication method
        choices: PAM_LOCAL, PAM_TACACS
        required: False
    secondary_method
        description: The secondary authentication method
        choices: SAM_NONE, SAM_LOCAL
        required: False

author:
    - Sanju Sadanandan (@hpe)
'''

EXAMPLES = '''
     - name: Updates the given console authentication configuration to the system
       arubaoss_aaa_authentication:
         primary_method: "PAM_TACACS"
         secondary_method: "SAM_LOCAL"
         command: config_authentication_console
'''


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.arubaoss.arubaoss import run_commands
from ansible.module_utils.network.arubaoss.arubaoss import arubaoss_argument_spec

"""
-------
Name: config_authentication

Configures port with authentication config

param request: module

Returns
 Configure the switch with params sent
-------
"""
def config_authentication(module):

    params = module.params

    url = "/authentication"

    if params['config'] == "create":
        data = {'is_privilege_mode_enabled': True}
    else:
        data = {'is_privilege_mode_enabled': False}

    method = 'PUT'

    result = run_commands(module, url, data, method, check=url)
    return result

"""
-------
Name: config_authentication_console

Configures port with authentication config

param request: module

Returns
 Configure the switch with params sent
-------
"""
def config_authentication_console(module):

    params = module.params

    url = "/authentication/console"

    data = {}
    data['auth_console_login'] = {'primary_method': params['primary_method'], 'secondary_method': params['secondary_method']}

    method = 'PUT'

    result = run_commands(module, url, data, method, check=url)
    return result

"""
-------
Name: config_authentication_ssh

Configures port with authentication config

param request: module

Returns
 Configure the switch with params sent
-------
"""
def config_authentication_ssh(module):

    params = module.params

    url = "/authentication/ssh"

    data = {}
    data['auth_ssh_login'] = {'primary_method': params['primary_method'], 'secondary_method': params['secondary_method']}

    method = 'PUT'

    result = run_commands(module, url, data, method, check=url)
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
        command=dict(type='str', required=False,default='config_authentication',
           choices=['config_authentication','config_authentication_console','config_authentication_ssh']),
        config=dict(type='str', required=False, default='create', choices=["create","delete"]),
        is_privilege_mode_enabled=dict(type='bool', required=False, default=False),
        primary_method=dict(type='str', required=False, default="PAM_LOCAL",
           choices=["PAM_LOCAL", "PAM_TACACS"]),
        secondary_method=dict(type='str', required=False, default="SAM_NONE",
           choices=["SAM_NONE", "SAM_LOCAL"]),
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
        if module.params['command'] == "config_authentication":
            result = config_authentication(module)
        elif module.params['command'] == "config_authentication_console":
            result = config_authentication_console(module)
        else:
            result = config_authentication_ssh(module)
    except Exception as err:
        return module.fail_json(msg=err)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
