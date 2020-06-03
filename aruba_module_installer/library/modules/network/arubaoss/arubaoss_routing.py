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
module: arubaoss_routing

short_description: implements rest api for routing

version_added: "2.6"

description:
    - "This implements routing rest api to enable/disable routing on device"

extends_documentation_fragment:
    - arubaoss_rest

options:
    state:
        description:
            - To enable/disable routing globally.
        required: true
        choices: create, delete


author:
    - Ashish Pant (@hpe)
'''

EXAMPLES = '''
     - name: enable routing
       arubaoss_routing:
         state: create

     - name: disable routing
       arubaoss_routing:
         state: delete

'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.arubaoss.arubaoss import run_commands
from ansible.module_utils.network.arubaoss.arubaoss import arubaoss_argument_spec, arubaoss_required_if


def routing(module):

    params = module.params
    url = "/ip-route/settings"

    if params['state'] == 'create':
        true = True
    else:
        true = False
    data = {'is_ip_routing_enable':true}

    result = run_commands(module, url, data, 'PUT',check=url)

    return result

def run_module():
    # define the available arguments/parameters that a user can pass to
    # the module
    module_args = dict(
        state=dict(type='str', required=False, choices=['create','delete']),
    )

    module_args.update(arubaoss_argument_spec)

    result = dict(changed=False)


    module = AnsibleModule(
        required_if=arubaoss_required_if,
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        return result

    try:
        result = routing(module)
    except Exception as err:
        return module.fail_json(msg=err)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
