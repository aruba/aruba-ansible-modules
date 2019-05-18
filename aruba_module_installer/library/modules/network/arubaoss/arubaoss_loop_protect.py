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
module: loop_protect

short_description: implements loop-protect rest api

version_added: "2.6"

description:
    - "This configures loop protect on device over vlan or port"

options:
    command:
        description:
            - Type of action to be taken.
        required: true
    port_disable_timer:
        description:
            - Set the number of seconds before disabled ports are
              automatically re-enabled
        required: false
    trasmit_interval:
        description:
            - Set the number of seconds between loop detect packet transmissions.
        required: false
    mode:
        description:
            - Configures vlan or port mode
        required: false
        default: LPM_PORT
        choices: LPM_PORT, LPM_VLAN
    interface:
        description:
            - Interface id on which loop protect to be configured
        required: false
    receiver_action:
        description:
            - Set the action to take when a loop is detected.
              is_loop_protection_enabled must be true to update the receiver_action.
        required: false
        default: LPRA_SEND_DISABLE
        choices: LPRA_SEND_DISABLE, LPRA_NO_DISABLE, LPRA_SEND_RECV_DISABLE
    vlan:
        description:
            - Vlan id on which loop protect is to be configured
        required: false


extends_documentation_fragment:
    - azure

author:
    - Ashish Pant (@hpe)
'''

EXAMPLES = '''
     - name: update loop
       arubaoss_loop_protect:
         command: update
         trap: True

     - name: enable loop-prtoect on port
       arubaoss_loop_protect:
         command: update_port
         interface: 1

     - name: disable loop-prtoect on port
       arubaoss_loop_protect:
         command: update_port
         interface: 1
         loop_protected: False

     - name: change loop-protect mode to vlan
       arubaoss_loop_protect:
         command: update
         mode: LPM_VLAN

     - name: enable loop-prtoect on vlan
       arubaoss_loop_protect:
         command: update_vlan
         vlan: 10

'''


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.arubaoss.arubaoss import run_commands,get_config
from ansible.module_utils.network.arubaoss.arubaoss import arubaoss_argument_spec
import sys


def update(module):

    params = module.params
    url = "/loop_protect"

    data = {
            'port_disable_timer_in_senconds': params['port_disable_timer'],
            'trasmit_interval_in_seconds': params['transmit_interval'],
            'mode': params['mode'],
            'is_trap_on_loop_detected_enabled': params['trap']
            }

    result = run_commands(module, url, data, 'PUT',check=url)

    return result


def update_port(module):

    params = module.params
    url = '/loop_protect/ports/' +  params['interface']
    port_url = '/ports/' + str(params['interface'])
    check_port = get_config(module,port_url)
    if not check_port:
        return {'msg': 'Port {} not present on device'.format(params['interface']),
                'changed':False}


    data = {
            'port_id': params['interface'],
            'is_loop_protection_enabled': params['loop_protected'],
            'receiver_action': params['receiver_action']
            }

    result = run_commands(module, url, data, 'PUT',check=url)

    return result


def update_vlan(module):

    params = module.params
    url = '/loop_protect/vlans/' +  str(params['vlan'])
    vlan_url = '/vlans/' + str(params['vlan'])
    check_vlan = get_config(module,vlan_url)
    if not check_vlan:
        return {'msg': 'Vlan {} not configured'.format(params['vlan']),
                'changed':False}


    data = {
            'vlan_id': params['vlan'],
            'is_vlan_loop_protected': params['loop_protected'],
            }

    result = run_commands(module, url, data, 'PUT',check=url)

    return result


def run_module():
    module_args = dict(
        command=dict(type='str', required=True,
            choices=['update','update_port','update_vlan']),
        port_disable_timer=dict(type='int', required=False, default=0),
        transmit_interval=dict(type='int', required=False, default=5),
        mode=dict(type='str', required=False, choices=['LPM_PORT','LPM_VLAN'],
            default='LPM_PORT'),
        trap=dict(type='bool', required=False, default=False),
        interface=dict(type='str', required=False,),
        loop_protected=dict(type='bool', required=False, default=True),
        receiver_action=dict(type='str', required=False, default='LPRA_SEND_DISABLE',
            choices=['LPRA_SEND_DISABLE','LPRA_NO_DISABLE','LPRA_SEND_RECV_DISABLE']),
        vlan=dict(type='int', required=False),
    )

    module_args.update(arubaoss_argument_spec)

    result = dict(changed=False,warnings='Not Supported')

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    command = module.params['command']

    try:
        thismod = sys.modules[__name__]
        method = getattr(thismod, command)

        result = method(module)
    except Exception as err:
        return module.fail_json(msg=err)

    module.exit_json(**result)


def main():
    run_module()

if __name__ == '__main__':
    main()
