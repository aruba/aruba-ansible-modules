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
module: arubaoss_vlan

short_description: implements rest api for vlan configuration

version_added: "2.4"

description:
    - "This implements rest apis which can be used to configure vlan"

options:
    command:
        description: Name of sub module, according to the configuration required.
        choices: config_vlan, config_vlan_port,
                config_vlan_ipaddress, config_vlan_dhcpHelperAddress
        required: True
    config:
        description: To config or unconfig the required command
        choices: create, delete
        required: False
    vlan_id:
        description: vlan id to be configured
        required: true
    name:
        description: Name of the VLAN. While creating a Vlan If name is given
        as empty string, default value (VLANx, where x is the vlan_id) will be
        configured. Empty string will not be accepted while modifying a Vlan
        required: false
    status:
        description: the status of the VLAN
        choices: VS_PORT_BASED, VS_PROTOCOL_BASED, VS_DYNAMIC
        required: false
    vlantype:
        description: The type of VLAN, default being VT_STATIC
        choices: VT_STATIC, VT_STATIC_SVLAN, VT_GVRP
        required: false
    is_jumbo_enabled:
        description:  Whether Jumbo is enabled
        required: false
    is_voice_enabled:
        description:  Whether Voice is enabled
        required: false
    is_dsnoop_enabled:
        description:  Whether DSNOOP is enabled
        required: false
    is_dhcp_server_enabled:
        description:  Whether DHCP server is enabled
        required: false
    is_management_vlan:
        description:  Whether vlan is a management vlan or not
        required: false
    ip_address_mode:
        description: IP Address Mode to be configured on vlan
        choices: IAAM_DISABLED, IAAM_STATIC, IAAM_DHCP
        required: False
    vlan_ip_address:
        description: IP Address to be configured on vlan
        required: False
    vlan_ip_mask:
        description: IP Mask for the IP Address configured
        required: False
    version:
        description: Version of IP Address
        choices: IAV_IP_V4. (V6 is not supported via REST)
        required: False
    helper_addresses:
        description: DHCP helper address for the corresponding VLAN id
        required: False
    port_id:
        description: Port ID to be configured on the vlan
        required: False
    port_mode:
        description: Port modes to be configured
        choices: POM_UNTAGGED, POM_TAGGED_STATIC, POM_FORBIDDEN
        required: False
    qos_policy:
        description: Qos policy to be added to vlan
        required: False
    acl_id:
        description: Acl policy to be added to vlan
        required: false
    acl_type:
        description: Type of acl policy
        default: AT_STANDARD_IPV4
        choices: AT_STANDARD_IPV4, AT_EXTENDED_IPV4, AT_CONNECTION_RATE_FILTER
        required: false
    acl_direction:
        description: Direction is which acl to be applied
        choices: AD_INBOUND, AD_OUTPUND, AD_CRF
        required: false


author:
    - Sanju Sadanandan (@hpe)
'''

EXAMPLES = '''
     - name: configure vlan
       arubaoss_vlan:
         vlan_id: 300
         name: "vlan300"
         status: "VS_PORT_BASED"
         vlantype: "VT_STATIC"
         is_jumbo_enabled: false
         is_voice_enabled: false
         is_dsnoop_enabled: false
         is_dhcp_server_enabled: false
         is_management_vlan: false
         config: "create"
         command: config_vlan
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.arubaoss.arubaoss import run_commands
from ansible.module_utils.network.arubaoss.arubaoss import get_config
from ansible.module_utils.network.arubaoss.arubaoss import arubaoss_argument_spec
from ansible.module_utils._text import to_text
import json


"""
-------
Name: config_vlan_ipaddress

Configures IP Address on the VLAN

param request: module

Returns
 Configure the switch with params sent
-------
"""
def config_vlan_ipaddress(module):

    params = module.params
    data = {}

    # Parameters
    if params['vlan_id'] == "":
        return {'msg': "vlan_id cannot be null",
                'changed': False, 'failed': True}
    else:
        data = {'vlan_id': params['vlan_id']}

    if params['ip_address_mode'] == "IAAM_STATIC" and params['config'] == "create":
        if params['version'] == "" or params['vlan_ip_address'] == "":
            return {'msg': "IP Address or version cannot be null",
                    'changed': False, 'failed': True}
        else:
            data['ip_address'] = {'version': params['version'], 'octets': params['vlan_ip_address']}

        if params['version'] == "" or params['vlan_ip_mask'] == "":
            return {'msg': "Subnet mask or version cannot be null",
                    'changed': False, 'failed': True}
        else:
            data['ip_mask'] = {'version': params['version'], 'octets': params['vlan_ip_mask']}

    data['ip_address_mode'] = params['ip_address_mode']

    # URLs
    url = "/vlans/" + str(params['vlan_id']) + "/ipaddresses"

    # Check if the passed vlan is configured
    check_presence_vlan = get_config(module, url)
    if not check_presence_vlan:
        return {'msg': 'Cannot configure IP Address without Vlan configured',
                'changed': False, 'failed': True}
    else:
        if params['config'] == "create":
            check_presence = get_config(module, url)
            newdata = json.loads(check_presence)

            # Check if IP already configured
            if params['ip_address_mode'] == "IAAM_STATIC":
                if newdata['collection_result']['total_elements_count'] == 1:
                    if newdata['ip_address_subnet_element'][0]['ip_address']['octets'] == params['vlan_ip_address']:
                        return {'msg': 'The ip address is already present on switch',
                          'changed': False, 'failed': False}

                    else:
                        method = 'DELETE'
                        result = run_commands(module, url, data, method)

            # Create the ip address on vlan
            method = 'POST'
            result = run_commands(module, url, data, method)

        elif params['config'] == "delete":
            check_dhcp_url = "/vlans/" + str(params['vlan_id'])
            check_dhcp_enabled = get_config(module, check_dhcp_url)
            check_dhcp_enabled = json.loads(check_dhcp_enabled)
            if "is_dhcp_server_enabled" in check_dhcp_enabled.keys():
                if check_dhcp_enabled["is_dhcp_server_enabled"]:
                    return {'msg': 'DHCP server must be disabled on this '
                                   'VLAN {}'.format(params['vlan_id']),
                            'changed': False, 'failed': True}
            method = 'DELETE'
            result = run_commands(module, url, data, method)

        else:
            return {'msg': 'Valid config options are : create and delete',
                'changed': False, 'failed': True}

    return result

"""
-------
Name: config_vlan_port

Configures Port on VLAN

param request: module

Returns
 Configure the switch with params sent
-------
"""
def config_vlan_port(module):

    params = module.params
    # Parameters
    if params['vlan_id'] == "":
        return {'msg': "vlan_id cannot be null",
                'changed': False, 'failed': True}
    else:
        data = {'vlan_id': params['vlan_id']}

    if params['port_id'] == "":
        return {'msg': "port_id cannot be null",
                'changed': False, 'failed': True}
    else:
        data['port_id'] = params['port_id']

    data['port_mode'] = params['port_mode']

    del_url = "/vlans-ports/" + str(params['vlan_id']) + "-" + str(params['port_id'])

    # Check if the passed vlan is configured
    check_presence = get_config(module, "/vlans/"+ str(params['vlan_id']))
    if not check_presence:
        return {'msg': 'Cannot configure ports without Vlan configured',
                'changed': False, 'failed': True}
    else:
        if params['config'] == "create":
            check_presence = get_config(module, del_url)
            if not check_presence:
                url = '/vlans-ports'
                method = 'POST'
            else:
                url = "/vlans-ports/" + str(params['vlan_id']) + "-" + str(params['port_id'])
                method = 'PUT'
        elif params['config'] == "delete":
            url = "/vlans-ports/" + str(params['vlan_id']) + "-" + str(params['port_id'])
            method = 'DELETE'
        else:
            return {'msg': 'Valid config options are : create and delete',
                'changed': False, 'failed': True}

        result = run_commands(module, url, data, method, check=del_url)
        return result

# Add dhcp helper address to vlan
"""
-------
Name: config_vlan_dhcpHelperAddress

Configure DHCP Helper Address on VLAN

param request: module

Returns
 Configure the switch with params sent
-------
"""
def config_vlan_dhcpHelperAddress(module):

    params = module.params

    # Parameters
    if params['vlan_id'] == "":
        return {'msg': "vlan_id cannot be null",
                'changed': False, 'failed': True}
    else:
        data = {'vlan_id': params['vlan_id']}

    if params['helper_addresses'] == "":
        return {'msg': "DHCP Helper IP Addr cannot be null",
                'changed': False, 'failed': True}
    else:
        data['dhcp_helper_address'] = {'version': params['version'], 'octets': params['helper_addresses']}

    url = "/vlans/dhcp-relay"
    del_url = url + '/' + str(params['vlan_id']) + '-' + params['helper_addresses']

    # Check if the passed vlan is configured
    check_presence = get_config(module, "/vlans/"+ str(params['vlan_id']))
    if not check_presence:
        return {'msg': 'Cannot configure Helper Address without Vlan configured',
                'changed': False, 'failed': True}

    else:
        if params ['config'] == "create":
            method = 'POST'
        else:
            url = del_url
            method = 'DELETE'

        result = run_commands(module, url, data, method, check=del_url)
        return result

"""
-------
Name: config_vlan

Configures VLAN with the id and name given

param request: module

Returns
 Configure the switch with params sent
-------
"""
def config_vlan(module):

    params = module.params

    # Parameters
    if params['vlan_id'] == "":
        return {'msg': "vlan_id cannot be null",
                'changed': False, 'failed': True}
    else:
        data = {'vlan_id': params['vlan_id']}

    if params['name'] == "":
        data['name'] = "VLAN{}".format(params['vlan_id'])
    else:
        data['name'] = params['name']

    data['status'] = params['status']
    data['type'] = params['vlantype']
    data['is_jumbo_enabled'] = params['is_jumbo_enabled']
    data['is_voice_enabled'] = params['is_voice_enabled']
    data['is_dsnoop_enabled'] = params['is_dsnoop_enabled']

    firmware_url = "/system/status"
    check_firmware_version = get_config(module, firmware_url)
    dhcp_server = module.from_json(to_text(check_firmware_version))
    if (dhcp_server['firmware_version'][:2] == "YA") or (dhcp_server['firmware_version'][:2] == "YB"):
        if params['is_dhcp_server_enabled']:
            return {'msg': "option : is_dhcp_server_enabled is not supported on this platform",
                    'changed': False, 'failed': True}
    else:
        data['is_dhcp_server_enabled'] = params['is_dhcp_server_enabled']

    config_url = "/vlans/" + str(params['vlan_id'])
    if params['config'] == "create":
        check_presence = get_config(module, config_url)
        if not check_presence:
            data['is_management_vlan'] = params['is_management_vlan']
            url = "/vlans"
            method = 'POST'
        else:
            url = "/vlans/" + str(params['vlan_id'])
            method = 'PUT'
            management_vlan = module.from_json(to_text(check_presence))
            if params['is_management_vlan'] != management_vlan['is_management_vlan']:
                data['is_management_vlan'] = params['is_management_vlan']
    else:
        url = config_url
        method = 'DELETE'

    result = run_commands(module, url, data, method, check=config_url)
    return result


def config_qos(module):

    params = module.params

    url = '/qos/vlans-policies'
    # if no vlan exists
    config_vlan(module)

    # check qos policy is present
    qos_check = '/qos/policies/' + params['qos_policy'] + '~' + 'QPT_QOS'
    if not get_config(module, qos_check):
        return {'msg': 'Configure QoS policy first. {} does not exist'.\
                format(params['qos_policy']),'changed':False}


    if params['config'] == 'create':
        policy_id = params['qos_policy'] + '~' + 'QPT_QOS'
        vlan_config = get_config(module, url)
        if vlan_config:
            check_config = module.from_json(to_text(vlan_config))
            for vlans in check_config['qos_vlan_policy_element']:
                if vlans['vlan_id'] == params['vlan_id'] and\
                   vlans['policy_id'] == policy_id:
                       ret = {'changed':False}
                       ret.update(vlans)
                       return ret


        data = {
                'vlan_id': params['vlan_id'],
                'policy_id': policy_id
                }
        result = run_commands(module, url,data, 'POST')

    else:
        url = url + '/' + str(params['vlan_id']) + '-' + params['qos_policy'] + '~' + 'QPT_QOS'
        check_url = url + '/stats'

        result = run_commands(module, url, {}, 'DELETE', check=check_url)

    return result


def config_acl(module):

    params = module.params

    if params.get('acl_direction') is None:
        return {'msg': 'Missing parameter: acl_direction','changed':False}

    # Check if acl is present
    url = "/vlans-access-groups"
    acl_type = params['acl_type']
    direction = params['acl_direction']
    data = {'vlan_id': params['vlan_id'],
            'acl_id': params['acl_id'] + "~" + acl_type,
            'direction': direction}

    check_acl = '/acls/' + params['acl_id'] + "~" + acl_type
    if not get_config(module,check_acl):
        return {'msg': 'Configure ACL first. {} does not exist'.\
                                format(params['acl_id']),'changed':False}

    delete_url = "{}/{}-{}~{}-{}".format(url, params['vlan_id'],
                                         params['acl_id'], acl_type,
                                         direction)

    config_present = False
    current_acl = get_config(module,url)
    if current_acl:
        check_config = module.from_json(to_text(current_acl))

        for ele in check_config['acl_vlan_policy_element']:
            if ele['uri'] == delete_url:
                config_present = ele

    if params['config'] == 'create':
        if config_present:
            ret = {'changed': False}
            ret.update(ele)
            return ret
        else:
            result = run_commands(module, url, data, method='POST')
    else:
        if config_present:
            result = run_commands(module, delete_url, method='DELETE')
        else:
            return {'changed': False,'failed': False, 'msg': 'Not present'}

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
        command=dict(type='str', default='config_vlan',
               choices=['config_vlan', 'config_vlan_port',
                'config_vlan_ipaddress', 'config_vlan_dhcpHelperAddress',
                'config_vlan_qos','config_vlan_acl']),
        config=dict(type='str', required=False, default= "create",
               choices=["create","delete"]),
        vlan_id=dict(type='int', required=True),
        name=dict(type='str', required=False, default=""),
        ip_address_mode=dict(type='str', required=False, default="IAAM_STATIC",
           choices = ['IAAM_DISABLED', 'IAAM_STATIC', 'IAAM_DHCP']),
        status=dict(type='str', required=False, default="VS_PORT_BASED",
           choices = ["VS_PORT_BASED", "VS_PROTOCOL_BASED", "VS_DYNAMIC"]),
        vlantype=dict(type='str', required=False, default="VT_STATIC",
           choices = ["VT_STATIC", "VT_STATIC_SVLAN", "VT_GVRP"]),
        is_jumbo_enabled=dict(type='bool', required=False, default=False),
        is_voice_enabled=dict(type='bool', required=False, default=False),
        is_dsnoop_enabled=dict(type='bool', required=False, default=False),
        is_dhcp_server_enabled=dict(type='bool', required=False, default=False),
        is_management_vlan=dict(type='bool', required=False, default=False),
        vlan_ip_address=dict(type='str', required=False, default=""),
        vlan_ip_mask=dict(type='str', required=False, default=""),
        version=dict(type='str', required=False, default= 'IAV_IP_V4',
                         choices=['IAV_IP_V4','IAV_IP_V6']),
        helper_addresses=dict(type='str', required=False, default=""),
        port_id=dict(type='str', required=False, default=""),
        port_mode=dict(type='str', required=False, default="POM_UNTAGGED",
           choices=['POM_UNTAGGED','POM_TAGGED_STATIC','POM_FORBIDDEN']),
        qos_policy=dict(type='str', required=False),
        acl_id=dict(type='str', required=False),
        acl_type=dict(type='str', required=False, default='AT_STANDARD_IPV4',
            choices=['AT_STANDARD_IPV4','AT_EXTENDED_IPV4','AT_CONNECTION_RATE_FILTER']),
        acl_direction=dict(type='str', required=False, choices=['AD_INBOUND',
            'AD_OUTBOUND','AD_CRF']),
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
        if module.params['command'] == "config_vlan":
            result = config_vlan(module)
        elif module.params['command'] == "config_vlan_dhcpHelperAddress":
            result = config_vlan_dhcpHelperAddress(module)
        elif module.params['command'] == "config_vlan_port":
            result = config_vlan_port(module)
        elif module.params['command'] == 'config_vlan_qos':
            result = config_qos(module)
        elif module.params['command'] == 'config_vlan_acl':
            result = config_acl(module)
        else:
            result = config_vlan_ipaddress(module)
    except Exception as err:
        return module.fail_json(msg=err)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
