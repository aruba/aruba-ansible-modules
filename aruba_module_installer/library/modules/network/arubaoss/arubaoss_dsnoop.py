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
module: arubaoss_dsnoop

short_description: implements REST API for DHCP snooping

version_added: "2.4"

description:
    - "This implements REST APIs which can be used to configure DHCP snooping"

extends_documentation_fragment:
    - arubaoss_rest

options:
    command:
        description: To configure a specific feature on DHCP snooping
        choices: ["authorized_server","option_82", "dsnoop"]
        required: False
        default: "dsnoop"
    dsnoop:
        description: To enable or disable DHCP snooping.
        choices: [True, False]
        required: False
        default: False
    is_dsnoop_option82_enabled:
        description: To enable/disable adding option 82 relay information to DHCP client
                     packets that are forwarded on trusted ports
        choices: [True, False]
        required: False
        default: True
    remote_id:
        description: To select the address used as the Remote ID for option 82
        choices: ["DRI_MAC","DRI_SUBNET_IP", "DRI_MGMT_IP"]
        required: False
        default: "DRI_MAC"
    untrusted_policy:
        description: To set the policy for DHCP packets containing option 82 that are 
                     received on untrusted ports
        choices: ["DUP_DROP","DUP_KEEP", "DUP_REPLACE"]
        required: False
        default: "DUP_DROP"
    server_ip:
        description: Add an authorized DHCP server address.
        required: False
        default: ""
    config:
        description: To configure or unconfigure the required command
        choices: ["create", "delete"]
        default: "create"

author:
    - Sunil Veeramachaneni (@hpe)
'''  # NOQA

EXAMPLES = '''
      - name: enable dsnoop
        arubaoss_dsnoop:
          dsnoop: true

      - name: disable dsnoop
        arubaoss_dsnoop:
          dsnoop: false

      - name: enable dsnoop option82 with untrusted-policy keep remote-id subnet-ip
        arubaoss_dsnoop:
          command: option_82
          is_dsnoop_option82_enabled: true
          remote_id: "DRI_SUBNET_IP"
          untrusted_policy: "DUP_KEEP"

      - name: disable dsnoop option82
        arubaoss_dsnoop:
          command: option_82
          is_dsnoop_option82_enabled: false

      - name: add dsnoop authorized_server
        arubaoss_dsnoop:
          command: authorized_server
          server_ip: "30.0.0.1"

      - name: remove dsnoop authorized_server
        arubaoss_dsnoop:
          command: authorized_server
          server_ip: "30.0.0.1"
          config: "delete"
'''  # NOQA


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.arubaoss.arubaoss import run_commands
from ansible.module_utils.network.arubaoss.arubaoss import arubaoss_argument_spec  # NOQA


def config(module):
    """
    -------
    Name: config

    Configures port with system_attributes config

    param request: module

    Returns
     Configure the switch with params sent
    -------
    """
    params = module.params
    data = {'is_dhcp_snooping_enabled': params['dsnoop']}
    url = '/dsnoop'
    method = 'PUT'
    result = run_commands(module, url, data, method, check=url)

    return result


def option_82(module):
    """
    -------
    Name: option_82

    Configures DHCP Snooping option 82

    param request: module

    Returns
     Configure the switch with params sent
    -------
    """
    params = module.params
    url = '/dsnoop/option_82'

    data = {'is_dsnoop_option82_enabled': params['is_dsnoop_option82_enabled']}
    data['remote_id'] = params['remote_id']
    data['untrusted_policy'] = params['untrusted_policy']

    method = 'PUT'
    result = run_commands(module, url, data, method, check=url)

    return result


def authorized_server(module):
    """
    -------
    Name: authorized_server

    Configures DHCP Snooping authorized server

    param request: module

    Returns
     Configure the switch with params sent
    -------
    """
    params = module.params
    url = '/dsnoop/authorized_server'

    data = {'is_dsnoop_option82_enabled': params['is_dsnoop_option82_enabled']}
    data['authorized_server'] = {"version": "IAV_IP_V4",
                                 "octets": params['server_ip']}

    method = 'POST'
    if params['config'] == 'delete':
        method = 'DELETE'
        url = url + '/' + params['server_ip']

    result = run_commands(module, url, data, method)

    return result


def run_module():
    """
    -------
    Name: run_module()

    The main module invoked

    Returns
     Configure the switch with params sent
    -------
    """
    module_args = dict(
        command=dict(type='str', required=False, default="dsnoop",
                     choices=["authorized_server",
                              "option_82",
                              "dsnoop"]),
        dsnoop=dict(type='bool', required=False, default=False),
        is_dsnoop_option82_enabled=dict(type='bool', required=False,
                                        default=True),
        remote_id=dict(type='str', required=False, default="DRI_MAC",
                       choices=["DRI_MAC", "DRI_SUBNET_IP", "DRI_MGMT_IP"]),
        untrusted_policy=dict(type='str', required=False, default="DUP_DROP",
                              choices=["DUP_DROP", "DUP_KEEP", "DUP_REPLACE"]),
        server_ip=dict(type='str', required=False, default=""),
        config=dict(type='str', required=False, default="create",
                    choices=["create", "delete"]),
    )

    module_args.update(arubaoss_argument_spec)

    result = dict(changed=False, warnings='Not Supported')

    module = AnsibleModule(
        required_if=arubaoss_required_if,
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    try:
        if module.params['command'] == "authorized_server":
            result = authorized_server(module)
        elif module.params['command'] == "option_82":
            result = option_82(module)
        else:
            result = config(module)
    except Exception as err:
        return module.fail_json(msg=err)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
