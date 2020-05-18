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
module: arubaoss_poe

short_description: implements rest api for PoE configuration

version_added: "2.4"

description:
    - "This implements rest apis which can be used to configure PoE"

extends_documentation_fragment:
    - arubaoss_rest

options:
    command:
        description: The module to be called.
        choices: reset_poe_port, config_poe_port and config_poe_slot
        required: False
    port_id:
        description: The Port id
        required: False
    is_poe_enabled:
        description: The port PoE status
        required: False
    poe_priority:
        description: The port PoE priority
        choices: PPP_CRITICAL, PPP_HIGH, PPP_LOW
        required: False
    poe_allocation_method:
        description: The PoE allocation method
        choices: PPAM_USAGE, PPAM_CLASS, PPAM_VALUE
        required: False
    allocated_power_in_watts:
        description: Allocated power value. Default value for this is
                     platform dependent
        required: False
    port_configured_type:
        description:  Port configured type
        required: False
    pre_standard_detect_enabled:
        description: pre_std_detect enable or disable
        required: False
    slot_name:
        description: The slot name
        required: False
    power_threshold_percentage:
        description: The power threshold percentage
        required: False

author:
    - Sanju Sadanandan (@hpe)
'''

EXAMPLES = '''
     - name: Updates poe port
       arubaoss_poe:
         command: config_poe_port
         port_id: 2
         is_poe_enabled: True
         poe_priority: "PPP_HIGH"
         poe_allocation_method: "PPAM_VALUE"
         allocated_power_in_watts: 15
         port_configured_type: ""
         pre_standard_detect_enabled: False

'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.arubaoss.arubaoss import run_commands
from ansible.module_utils.network.arubaoss.arubaoss import arubaoss_argument_spec, arubaoss_required_if
from ansible.module_utils.network.arubaoss.arubaoss import get_config
import json

"""
-------
Name: config

Resets the PoE controller to which the port belongs

param request: module

Returns
 Configure the switch with params sent
-------
"""
def reset_poe_port(module):

    params = module.params
    data = {}

    # Check if port_id is null
    if params['port_id'] == "":
        return {'msg': 'port_id cannot be null',
                'changed': False, 'failed': False}

    url = '/poe/ports/' + str(params['port_id']) + '/reset'
    method = 'POST'

    result = run_commands(module, url, data, method, check=url)

    return result
"""
-------
Name: config

Resets the PoE controller to which the port belongs

param request: module

Returns
 Configure the switch with params sent
-------
"""
def config_poe_port(module):

    params = module.params
    data = {}

    data['port_id'] = params['port_id']
    data['is_poe_enabled'] = params['is_poe_enabled']
    data['poe_priority'] = params['poe_priority']
    data['poe_allocation_method'] = params['poe_allocation_method']
    data['port_configured_type'] = params['port_configured_type']
    data['pre_standard_detect_enabled'] = params['pre_standard_detect_enabled']

    # allocated_power_in_watts can be set only when poe_allocation_method is PPAM_VALUE
    if params['poe_allocation_method'] == "PPAM_VALUE":
        data['allocated_power_in_watts'] = params['allocated_power_in_watts']

    # Check if port_id is null
    if params['port_id'] == "":
        return {'msg': 'port_id cannot be null',
                'changed': False, 'failed': False}

    url = '/ports/' + str(params['port_id']) + '/poe'
    method = 'PUT'

    diffSeen = False
    check_presence = get_config(module, url)
    newdata = json.loads(check_presence)
    for key in data:
        if not newdata[key] == data[key]:
            diffSeen = True
            break

    if diffSeen:
        result = run_commands(module, url, data, method, check=url)
        return result
    else:
        return {'msg': 'Already Configured',
                'changed': False, 'failed': False}

"""
-------
Name: config

Resets the PoE controller to which the port belongs

param request: module

Returns
 Configure the switch with params sent
-------
"""
def config_poe_slot(module):

    params = module.params
    data = {}

    data['slot_name'] = params['slot_name']
    data['power_threshold_percentage'] = params['power_threshold_percentage']

    # Check if slot_name is null
    if params['slot_name'] == "":
        return {'msg': 'slot_name cannot be null',
                'changed': False, 'failed': False}

    url = '/slots/' + str(params['slot_name']) + '/poe'
    method = 'PUT'

    diffSeen = False
    check_presence = get_config(module, url)
    newdata = json.loads(check_presence)
    for key in data:
        if not newdata[key] == data[key]:
            diffSeen = True
            break

    if diffSeen:
        result = run_commands(module, url, data, method, check=url)
        return result
    else:
        return {'msg': 'Already Configured',
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
        command=dict(type='str', required=False, default="config_poe",
            choices=["reset_poe_port", "config_poe_port", "config_poe_slot"]),
        port_id=dict(type='str', required=False, default=""),
        is_poe_enabled=dict(type='bool', required=False, default=True),
        poe_priority=dict(type='str', required=False, default="PPP_LOW",
            choices=["PPP_CRITICAL", "PPP_HIGH", "PPP_LOW"]),
        poe_allocation_method=dict(type='str', required=False, default="PPAM_USAGE",
            choices=["PPAM_USAGE", "PPAM_CLASS", "PPAM_VALUE"]),
        allocated_power_in_watts=dict(type='int', required=False, default=1),
        port_configured_type=dict(type='str', required=False, default=""),
        pre_standard_detect_enabled=dict(type='bool', required=False, default=False),
        slot_name=dict(type='str', required=False, default=""),
        power_threshold_percentage=dict(type='int', required=False, default=1),
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
        if module.params['command'] == "reset_poe_port":
            result = reset_poe_port(module)
        if module.params['command'] == "config_poe_slot":
            result = config_poe_slot(module)
        else:
            result = config_poe_port(module)
    except Exception as err:
        return module.fail_json(msg=err)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
