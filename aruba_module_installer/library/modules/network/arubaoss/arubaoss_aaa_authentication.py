#!/usr/bin/python
#
# Copyright (c) 2019-2020 Hewlett Packard Enterprise Development LP
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

extends_documentation_fragment:
    - arubaoss_rest

options:
  command:
    description: Function name calls according to configuration required.
      config_authentication - To enable/disable privilaged mode, Specify that
        switch respects the authentication server's privilege level.
      config_authentication_console - Configure authentication mechanism used to control
        access to the switch console.
      config_authentication_ssh - Configure authentication mechanism used to control SSH
        access to the switch.
      config_authentication_local_user - Create or remove a local user account.
    default: config_authentication
    choices: ['config_authentication', 'config_authentication_console',
      'config_authentication_ssh', 'config_authentication_local_user']
    required: False
  primary_method:
    description: The primary authentication method, used with config_authentication_console
      and config_authentication_ssh command.
    choices: ['PAM_LOCAL', 'PAM_TACACS']
    default: PAM_LOCAL
    required: False
  secondary_method:
    description: The secondary authentication method, used with config_authentication_console
      and config_authentication_ssh command.
    choices: ['SAM_NONE', 'SAM_LOCAL']
    default: SAM_NONE
    required: False
  local_user_name:
    description: Create or remove a local user account. Used with config_authentication_local_user
      command.
    type: 'str'
    required: False
  group_name:
    description: Specify the group for a username. Used with config_authentication_local_user
      command.
    type: 'str'
  password_type:
    description: Specify the password type. Used with config_authentication_local_user
      command.
    choices=["PET_SHA1","PET_PLAIN_TEXT", "PET_SHA256"]
    required: False
    default="PET_SHA1"
  user_password:
    description: Specify the password.  Used with config_authentication_local_user
      command.
    type: 'str'
  min_pwd_len:
    description: Configures the minimum password length for a user. Used with
      config_authentication_local_user command.
    type='int' <1-64>
    default=8
  aging_period:
    description: Configures the password aging time for a user. Used with
      config_authentication_local_user command.
    type: int
    default: 0

author:
    - Sanju Sadanandan (@hpe)
'''

EXAMPLES = '''
- name: aaa authentication login privilege-mode
  arubaoss_aaa_authentication:
    command: config_authentication

- name: aaa authentication console login tacacs
  arubaoss_aaa_authentication:
    command: config_authentication_console
    primary_method: PAM_TACACS
    secondary_method: SAM_LOCAL

- name: aaa authentication ssh login tacacs
  arubaoss_aaa_authentication:
    command: config_authentication_ssh
    primary_method: PAM_TACACS
    secondary_method: SAM_LOCAL

- name: Create Authentication local user plaintext password
  arubaoss_aaa_authentication:
    command: config_authentication_local_user
    group_name: "Level-15"
    local_user_name: "ARUBA"
    password_type: "PET_PLAIN_TEXT"
    user_password: "ArubaR0Cks!"

- name: Create Authentication local user sha256
  arubaoss_aaa_authentication:
    command: config_authentication_local_user
    group_name: "super"
    local_user_name: "ARUBA"
    password_type: "PET_SHA256"
    user_password: "1c6976e5b5410115bde308bd4dee15dfb167a9c873fc4bb8a81f6f2ab478a918"

  - name: Create Authentication local user2
    arubaoss_aaa_authentication:
      command: config_authentication_local_user
      group_name: "super"
      local_user_name: "user2"
      password_type: "PET_SHA1"
      user_password: "d033e22ae348aeb5660fc2140aec35850c4da997"

  - name: update Authentication local user min_pwd_len, aging_period
    arubaoss_aaa_authentication:
      command: config_authentication_local_user
      local_user_name: "user1"
      min_pwd_len: 10
      aging_period: 20

  - name: Delete Authentication local user
    arubaoss_aaa_authentication:
      command: config_authentication_local_user
      local_user_name: "user1"
      config: "delete"
'''


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.arubaoss.arubaoss import run_commands
from ansible.module_utils.network.arubaoss.arubaoss import arubaoss_argument_spec, arubaoss_required_if
from ansible.module_utils.network.arubaoss.arubaoss import get_config

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
Name: config_authentication_local_user

Configures local user with authentication config

param request: module

Returns
 Configure the switch with params sent
-------
"""
def config_authentication_local_user(module):
    params = module.params
    data = {}

    # URI
    url = "/authentication/local_user"
    get_url = url + "/" + params['local_user_name']

    if params['config'] == "create":
        method = "POST"
    else:
        method = "DELETE"
        url = get_url

    data['local_user_name'] = params['local_user_name']
    data['min_pwd_len'] = params['min_pwd_len']
    data['aging_period'] = params['aging_period']

    check_presence = get_config(module, get_url)

    if params['group_name'] != "":
        data['group_name'] = params['group_name']
    else:
        # if group name is empty, only scope is to modify an existing user
        if check_presence:
            # User exists
            if method == "POST":
                method = "PUT"
                url = get_url

    if method == "POST":
        data['password'] = params['user_password']
        data['password_type'] = params['password_type']

    #check_presence = get_config(module, get_url)
    if check_presence:
        # User exist
        if method == "POST":
            return {'msg': 'The user account already exists.',
                    'changed': False, 'failed': False}
    else:
        # User does not exist
        if method == "DELETE":
            return {'msg': 'The user account does not exist.',
                    'changed': False, 'failed': False}

    # Config
    result = run_commands(module, url, data, method)
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
           choices=['config_authentication','config_authentication_console',
                    'config_authentication_ssh', 'config_authentication_local_user']),
        config=dict(type='str', required=False, default='create', choices=["create","delete"]),
        primary_method=dict(type='str', required=False, default="PAM_LOCAL",
           choices=["PAM_LOCAL", "PAM_TACACS"]),
        secondary_method=dict(type='str', required=False, default="SAM_NONE",
           choices=["SAM_NONE", "SAM_LOCAL"]),
        local_user_name=dict(type='str', required=False, default=""),
        group_name=dict(type='str', required=False, default=""),
        password_type=dict(type='str', required=False, default="PET_SHA1",
                           choices=["PET_SHA1","PET_PLAIN_TEXT", "PET_SHA256"]),
        user_password=dict(type='str', required=False, default=""),
        min_pwd_len=dict(type='int', required=False, default=8),
        aging_period=dict(type='int', required=False, default=0),
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
        if module.params['command'] == "config_authentication":
            result = config_authentication(module)
        elif module.params['command'] == "config_authentication_console":
            result = config_authentication_console(module)
        elif module.params['command'] == "config_authentication_local_user":
            result = config_authentication_local_user(module)
        else:
            result = config_authentication_ssh(module)
    except Exception as err:
        return module.fail_json(msg=err)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
