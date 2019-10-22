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
module: arubaoss_sntp

short_description: implements rest api for sntp and sntp server priority configuration

version_added: "2.4"

description:
    - "This implements rest apis which can be used to configure sntp"

options:
    command:
        description: Name of sub module, according to the configuration required.
        choices: config_sntp, config_sntp_priority,
        required: True
    config:
        description: To config, unconfig the required command
        choices: create, delete
        required: True
    sntp_config_poll_interval:
        description: The number of seconds between updates of the system clock using SNTP.
        required: false
    sntp_client_operation_mode:
        description: The mode in which clients are sending packets to SNTP server.
      choices: SNTP_DISABLE, SNTP_DHCP_MODE, SNTP_UNICAST_MODE, SNTP_BROADCAST_MODE
        required: false
      default : SNTP_DHCP_MODE
    sntp_ip_address:
        description: IP Address to be configured on sntp server priority
        required: True
    version:
        description: Version of IP Address
        choices: IAV_IP_V4. (V6 is not supported via REST)
        required: True
    sntp_server_priority:
        description: Priority of Server Address.
        required: True
    sntp_server_version:
        description: SNTP version of server.
        required: false
      default : 7
    sntp_server_is_oobm:
        description:  Use the OOBM interface to connect to the server
        required: false
      default : false



author:
    - Naveen Prabhu S D (sd.naveen-prabhu@hpe.com)
'''

EXAMPLES = '''
      - name: config sntp server priority
        arubaoss_sntp:
          command: config_sntp_priority
          sntp_ip_address: "2.2.3.4"
          version: "IAV_IP_V4"
          sntp_server_priority: 3
          sntp_server_version : 5
          sntp_server_is_oobm : true
      
      - name: Delete sntp server priority
        arubaoss_sntp:
          config: "delete"
          command: config_sntp_priority
          sntp_ip_address: "2.2.3.4"
          version: "IAV_IP_V4"
          sntp_server_priority: 3
          sntp_server_version : 5
          sntp_server_is_oobm : true
      
      - name: disable sntp
        arubaoss_sntp:
          command: config_sntp
          sntp_client_operation_mode: SNTP_DISABLE          
      
      - name: configure sntp poll interval 44 in Unicast
        arubaoss_sntp:
          sntp_config_poll_interval: 44
          sntp_client_operation_mode: "SNTP_UNICAST_MODE"
          command: config_sntp      
'''


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.arubaoss.arubaoss import run_commands
from ansible.module_utils.network.arubaoss.arubaoss import get_config
from ansible.module_utils.network.arubaoss.arubaoss import arubaoss_argument_spec


"""
-------
Name: config_sntp_priority

Configures sntp server priority with the id and name given

param request: module

Returns
 Configure the switch with params sent
-------
"""
def config_sntp_priority(module):

    params = module.params
    data = {}

    # Parameters
    if params['version'] == "" or params['sntp_ip_address'] == "":
        return {'msg': "IP Address or version cannot be null",
                'changed': False, 'failed': True}
    else:
        data['sntp_server_address'] = {'version': params['version'], 'octets': params['sntp_ip_address']}

    if params['sntp_server_priority'] == "":
        return {'msg': "Sntp Server Priority cannot be null",
                'changed': False, 'failed': True}
    else:
        data['sntp_server_priority'] = params['sntp_server_priority']

    data['sntp_server_version'] = params['sntp_server_version']
    data['sntp_server_is_oobm'] = params['sntp_server_is_oobm']

    config_url = "/system/sntp_server/" + str(params['sntp_server_priority']) + "-" +  str(params['sntp_ip_address'])
    check_presence = get_config(module, config_url)
    if params ['config'] == "create":
        if not check_presence:
            url = "/system/sntp_server"
            method = 'POST'
        else:
            """
            REST-PUT Operation not supported
            """
            return {'msg': "SNTP Server Address or Priority already configured.",
                    'changed': False, 'failed': True}
    else:
        if not check_presence:
            return {'msg': "SNTP Server Address or Priority entered is not configured.",
                    'changed': False, 'failed': True}
        else:
            url = config_url
            method = 'DELETE'

    result = run_commands(module, url, data, method, check=config_url)
    return result


"""
-------
Name: config_sntp

Updates SNTP with the mode and poll interval given

param request: module

Returns
 Configure the switch with params sent
-------
"""


def config_sntp(module):

    params = module.params
    data = {}

    # Parameters
    data['sntp_client_operation_mode'] = params['sntp_client_operation_mode']
    data['sntp_config_poll_interval'] = params['sntp_config_poll_interval']

    config_url = "/system/sntp"
    if params['config'] == "create":
        """
        REST - POST Method Not Supported
        """
        method = 'PUT'
        url = "/system/sntp"
        result = run_commands(module, url, data, method, check=config_url)
        return result
    else:
        return {'msg': "REST-DELETE Method not supported",'changed': False,
                'failed': True}


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
        command=dict(type='str', default='config_sntp',
                     choices=['config_sntp', 'config_sntp_priority']),
        config=dict(type='str', required=False, default="create",
                    choices=["create","delete"]),
        sntp_config_poll_interval=dict(type='int',
                                       required=False, default=720),
        sntp_client_operation_mode=dict(type='str', required=False,
                                        default="SNTP_DHCP_MODE",
                                        choices=['SNTP_DISABLE',
                                                 'SNTP_DHCP_MODE',
                                                 'SNTP_UNICAST_MODE',
                                                 'SNTP_BROADCAST_MODE']),
        sntp_ip_address=dict(type='str', required=False, default=""),
        version=dict(type='str', required=False, default='IAV_IP_V4',
                     choices=['IAV_IP_V4', 'IAV_IP_V6']),
        sntp_server_priority=dict(type='int', required=False),
        sntp_server_version=dict(type='int', required=False, default=3),
        sntp_server_is_oobm=dict(type='bool', required=False, default=False),
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
        if module.params['command'] == "config_sntp":
            result = config_sntp(module)
        else:
            result = config_sntp_priority(module)
    except Exception as err:
        return module.fail_json(msg=err)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
