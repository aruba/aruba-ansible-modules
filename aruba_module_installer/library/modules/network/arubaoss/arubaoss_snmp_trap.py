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
module: arubaoss_snmp_trap

short_description: implements rest api for snmp trap configuration

version_added: "2.6"

description:
    - "This implements rest api's which enable/disable snmp traps for
       differente features on device"

extends_documentation_fragment:
    - arubaoss_rest

options:
    arp_protect:
        description:
            - Traps for dynamic arp protection
        required: false
        default: STM_ENABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    aut_server_fail:
        description:
            - Traps reporting authentication server unreachable
        required: false
        default: STM_ENABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    dhcp_server:
        description:
            - Trpas for dhcp server
        required: false
        default: STM_ENABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    dhcp_snooping:
        description:
            - Traps for dhcp snooping
        required: false
        default: STM_ENABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    dhcpv6_snooping_out_of_resource:
        description:
            - Enable traps for dhcpv6 snooping out of resource
        required: false
        default: STM_ENABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    dhcpv6_snooping_errant_replies:
        description:
            - Traps for DHCPv6 snooping errant replies
        required: false
        default: STM_ENABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    dyn_ip_lockdown:
        description:
            - Traps for Dynamic Ip Lockdown
        required: false
        default: STM_ENABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    dyn_ipv6_ld_out_of_resources:
        description:
            - Enable traps for Dynamic IPv6 Lockdown out of resources
        required: false
        default: STM_ENABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    dyn_ipv6_ld_violations:
        description:
            - Enable traps for Dynamic IPv6 Lockdown violations.
        required: false
        default: STM_ENABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    login_failure_mgr:
        description:
            - Traps for management interface login failure
        required: false
        default: STM_ENABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    mac_count_notify:
        description:
            - Traps for MAC addresses learned on the specified ports exceeds the threshold
        required: false
        default: STM_ENABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    nd_snooping_out_of_resources:
        description:
            - The trap for nd snooping out of resources
        required: false
        default: STM_ENABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    password_change_mgr:
        description:
            - Traps for management interface password change
        required: false
        default: STM_ENABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    port_security:
        description:
            - Traps for port access authentication failure
        required: false
        default: STM_ENABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    startup_config_change:
        description:
            - Traps for changed to the startup config
        required: false
        default: STM_DISABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    macsec_failure:
        description:
            - Enable the MACsec Connectivity Association (CA) failure trap
        required: false
        default: STM_ENABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    mac_move_notify_mode:
        description:
            - Traps for move mac address table changes
        required: false
        default: STM_DISABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    mac_notify_mode:
        description:
            - Traps for mac notify
        required: false
        default: STM_DISABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    running_conf_change_trap:
        description:
            - Traps mode for running config change
        required: false
        default: STM_DISABLE
        choices: STM_ENABLE, STM_DISABLE, STM_NONE
    snmp_authentication:
        description:
            - Select RFC1157 (standard) or HP-ICF-SNMP (extended) traps
        required: false
        default: SATM_EXTENDED
        choices: SATM_EXTENDED, SATM_STANDARD, SATM_NONE
    mac_notify_trap_interval:
        description:
            - Trap interval for mac_move_notify_mode and mac_notify_mode
        required: false
        default: 30
        choices: 0-120
    running_config_trap_interval:
        description:
            - Traps interval for running_conf_change_trap
        required: false
        default: 0
        choices: 0-120


author:
    - Ashish Pant (@hpe)
'''

EXAMPLES = '''
      - name: configure snmp trap
        arubaoss_snmp_traps:
          mac_move_notify_mode: "{{item}}"
        with_items:
          - STM_ENABLE
          - STM_DISABLE

'''


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.arubaoss.arubaoss import run_commands
from ansible.module_utils.network.arubaoss.arubaoss import arubaoss_argument_spec, arubaoss_required_if


def snmp_trap(module):

    params = module.params
    url = '/snmp-server/traps'

    data = {
            'arp_protect': params['arp_protect'],
            'auth_server_fail': params['auth_server_fail'],
            'dhcp_server': params['dhcp_server'],
            'dhcp_snooping': params['dhcp_snooping'],
            'dhcpv6_snooping_out_of_resource': params['dhcpv6_snooping_out_of_resource'],
            'dhcpv6_snooping_errant_replies': params['dhcpv6_snooping_errant_replies'],
            'dyn_ip_lockdown': params['dyn_ip_lockdown'],
            'dyn_ipv6_ld_out_of_resources': params['dyn_ipv6_ld_out_of_resources'],
            'dyn_ipv6_ld_violations': params['dyn_ipv6_ld_violations'],
            'login_failure_mgr': params['login_failure_mgr'],
            'mac_count_notify': params['mac_count_notify'],
            'nd_snooping_out_of_resources': params['nd_snooping_out_of_resources'],
            'password_change_mgr': params['password_change_mgr'],
            'port_security': params['port_security'],
            'startup_config_change': params['startup_config_change'],
            'macsec_failure': params['macsec_failure'],
            'mac_notify' : {
                'mac_move_notify_mode': params['mac_move_notify_mode'],
                'mac_notify_mode': params['mac_notify_mode'],
                'trap_interval': params['mac_notify_trap_interval']
                },
            'running_config_changes': {
                'running_conf_change_trap': params['running_conf_change_trap'],
                'trap_interval': params['running_config_trap_interval']
                },
            'snmp_authentication': params['snmp_authentication']
            }

    result = run_commands(module, url, data, 'PUT', check=url)

    return result


def run_module():
    module_args = dict(
        arp_protect=dict(type='str', required=False, default='STM_ENABLE',
            choices=['STM_ENABLE','STM_DISABLE','STM_NONE']),
        auth_server_fail=dict(type='str', required=False, default='STM_ENABLE',
            choices=['STM_ENABLE','STM_DISABLE','STM_NONE']),
        dhcp_server=dict(type='str', required=False, default='STM_ENABLE',
            choices=['STM_ENABLE','STM_DISABLE','STM_NONE']),
        dhcp_snooping=dict(type='str', required=False, default='STM_ENABLE',
            choices=['STM_ENABLE','STM_DISABLE','STM_NONE']),
        dhcpv6_snooping_out_of_resource=dict(type='str', required=False, default='STM_ENABLE',
            choices=['STM_ENABLE','STM_DISABLE','STM_NONE']),
        dhcpv6_snooping_errant_replies=dict(type='str', required=False, default='STM_ENABLE',
            choices=['STM_ENABLE','STM_DISABLE','STM_NONE']),
        dyn_ip_lockdown=dict(type='str', required=False, default='STM_ENABLE',
            choices=['STM_ENABLE','STM_DISABLE','STM_NONE']),
        dyn_ipv6_ld_out_of_resources=dict(type='str', required=False, default='STM_ENABLE',
            choices=['STM_ENABLE','STM_DISABLE','STM_NONE']),
        dyn_ipv6_ld_violations=dict(type='str', required=False, default='STM_ENABLE',
            choices=['STM_ENABLE','STM_DISABLE','STM_NONE']),
        login_failure_mgr=dict(type='str', required=False, default='STM_ENABLE',
            choices=['STM_ENABLE','STM_DISABLE','STM_NONE']),
        mac_count_notify=dict(type='str', required=False, default='STM_ENABLE',
            choices=['STM_ENABLE','STM_DISABLE','STM_NONE']),
        nd_snooping_out_of_resources=dict(type='str', required=False, default='STM_ENABLE',
            choices=['STM_ENABLE','STM_DISABLE','STM_NONE']),
        password_change_mgr=dict(type='str', required=False, default='STM_ENABLE',
            choices=['STM_ENABLE','STM_DISABLE','STM_NONE']),
        port_security=dict(type='str', required=False, default='STM_ENABLE',
            choices=['STM_ENABLE','STM_DISABLE','STM_NONE']),
        startup_config_change=dict(type='str', required=False, default='STM_DISABLE',
            choices=['STM_ENABLE','STM_DISABLE','STM_NONE']),
        macsec_failure=dict(type='str', required=False, default='STM_ENABLE',
            choices=['STM_ENABLE','STM_DISABLE','STM_NONE']),
        mac_move_notify_mode=dict(type='str', required=False, default='STM_DISABLE',
            choices=['STM_ENABLE','STM_DISABLE','STM_NONE']),
        mac_notify_mode=dict(type='str', required=False, default='STM_DISABLE',
            choices=['STM_ENABLE','STM_DISABLE','STM_NONE']),
        running_conf_change_trap=dict(type='str', required=False, default='STM_ENABLE',
            choices=['STM_ENABLE','STM_DISABLE','STM_NONE']),
        snmp_authentication=dict(type='str', required=False, default='SATM_EXTENDED',
            choices=['SATM_EXTENDED','SATM_STANDARD','SATM_NONE']),
        mac_notify_trap_interval=dict(type='int', requried=False, default=30),
        running_config_trap_interval=dict(type='int', required=False, default=0),
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
        result = snmp_trap(module)
    except Exception as err:
        return module.fail_json(msg=err)

    module.exit_json(**result)


def main():
    run_module()

if __name__ == '__main__':
    main()
