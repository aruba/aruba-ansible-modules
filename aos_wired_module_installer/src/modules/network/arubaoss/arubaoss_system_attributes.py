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
module: arubaoss_system_attributes

short_description: implements rest api for DOT1x configuration

version_added: "2.4"

description:
    - "This implements rest apis which can be used to configure DOT1x"

options:
    hostname:
        description: The system name
        required: False
    location:
        description: Location where the system is installed
        required: False
    contact:
        description: Contact information for the system.
        required: False
    domain_name:
        description: Regulatory domain where the system is operating on
        required: False
    version:
        description: Version of ip address
        required: False
    device_operation_mode:
        description: Mode in which the device is operating on
        required: False
    uplink_vlan_id:
        description: Vlan via which central is connected. This is applicable
                     only when device_operation_mode is DOM_CLOUD or DOM_CLOUD_WITH_SUPPORT.
                     This won't be available for non Central uses case
        required: False
    uplink_ip:
        description: Ip address of Vlan via which central is connected. This is
                     applicable only when device_operation_mode is DOM_CLOUD or
                     DOM_CLOUD_WITH_SUPPORT. This won't be available for non Central uses case
        required: False
    default_gateway_ip:
        description: The global IPV4 default gateway. Input octets as 0.0.0.0 to reset.
        required: False

author:
    - Sanju Sadanandan (@hpe)
'''

EXAMPLES = '''
     - name: Updates the given console authorization configuration to the system
       arubaoss_system_attributes:
         hostname: "Test_santorini"
         location: "Bangalore"
         contact: "08099035734"
         domain_name: "hpe.com"
         version: "IAV_IP_V4"
         device_operation_mode: "DOM_AUTONOMOUS"
         uplink_vlan_id: "10"
         uplink_ip: "10.100.20.30"
         default_gateway_ip: "10.100.119.1"
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.arubaoss.arubaoss import run_commands
from ansible.module_utils.network.arubaoss.arubaoss import arubaoss_argument_spec

"""
-------
Name: config

Configures port with system_attributes config

param request: module

Returns
 Configure the switch with params sent
-------
"""
def config(module):

    params = module.params
    data = {}

    if not params['hostname'] == "":
        data['name'] = params['hostname']

    if not params['location'] == "":
        data['location'] = params['location']

    if not params['contact'] == "":
        data['contact'] = params['contact']

    if not params['domain_name'] == "":
        data['regulatory_domain'] = params['domain_name']

    if not params['uplink_ip'] == "":
        data['uplink_ip_address'] = {'version': params['version'], 'octets': params['uplink_ip']}

    if not params['default_gateway_ip'] == "":
        data['default_gateway'] = {'version': params['version'], 'octets': params['default_gateway_ip']}

    if not params['uplink_vlan_id'] == "":
        data['uplink_vlan_id'] = params['uplink_vlan_id']

    if not params['device_operation_mode'] == "":
        data['device_operation_mode'] = params['device_operation_mode']

    url = '/system'
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
        hostname=dict(type='str', required=False, default=''),
        location=dict(type='str', required=False, default=''),
        contact=dict(type='str', required=False, default=''),
        version=dict(type='str', required=False, default='IAV_IP_V4',
           choices=['IAV_IP_V4','IAV_IP_V6']),
        domain_name=dict(type='str', required=False, default=''),
        default_gateway=dict(type='str', required=False, default=''),
        device_operation_mode=dict(type='str', required=False, default='DOM_AUTONOMOUS',
           choices = ["DOM_CLOUD","DOM_CLOUD_WITH_SUPPORT","DOM_AUTONOMOUS"]),
        uplink_vlan_id=dict(type='str', required=False, default=''),
        uplink_ip=dict(type='str', required=False, default=''),
        default_gateway_ip=dict(type='str', required=False, default=''),
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
