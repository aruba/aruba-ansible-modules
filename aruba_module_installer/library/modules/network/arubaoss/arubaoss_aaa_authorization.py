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
module: arubaoss_aaa_authorization

short_description: implements rest api for AAA Authorization configuration

version_added: "2.4"

description:
    - "This implements rest apis which can be used to configure authorization"

options:
    authorization_method:
        description: To authorization method needed
        choices: AZM_NONE, AZM_TACACS
        required: False

author:
    - Sanju Sadanandan (@hpe)
'''

EXAMPLES = '''
     - name: Updates the given console authorization configuration to the system
       arubaoss_aaa_authorization:
         authorization_method: "AZM_TACACS"
'''

RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
message:
    description: The output message that the sample module generates
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.arubaoss.arubaoss import run_commands
from ansible.module_utils.network.arubaoss.arubaoss import arubaoss_argument_spec

"""
-------
Name: config

Configures port with authorization config

param request: module

Returns
 Configure the switch with params sent
-------
"""
def config(module):

    params = module.params
    data = {'authorization_method': params['authorization_method']}
    url = '/authorization'
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
        authorization_method=dict(type='str', required=False, default="AZM_NONE",
                         choices=["AZM_NONE","AZM_TACACS"]),
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
        result = config(module)
    except Exception as err:
        return module.fail_json(msg=err)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
