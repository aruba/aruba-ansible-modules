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
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: arubaoscx_vlan_interface

version_added: "1.0"

description:
    - "This module implements VLAN interface configuration for ArubaOS_CX switch"

options:
    interface:
        description: Interface name, should be in form of 'vlan' + vlanid, eg. vlan2.
        type: string
        required: true
    admin_state:
        description: Admin status information about interface.
        default: 'up'
        choices: ['up', 'down']
        required: False
    description:
        description: Description of interface.
        type: string
        required: False
    ipv4:
        description: The IPv4 address and subnet mask in the address/mask format.
                     The first entry in the list is the primary IPv4, the remainings are secondary IPv4.
        type: list
        required: False
    ipv6:
        description: The IPv6 address and subnet mask in the address/mask format.
                     It takes multiple IPv6 with comma separated in the list.
        type: list
        required: False
    vrf:
        description: Attaching interface to VRF, commonly known as Virtual Routing and Forwarding.
                     The interface will be attached to default VRF if not specified.
        type: string
        required: False
    ip_helper_address:
        description: Configure a remote DHCP server/relay IP address on the device interface. Here the
                     helper address is same as the DHCP server address or another intermediate DHCP relay.
        type: list
        required: False
    active_gateway_ip:
        description: For VSX and active-active routing, virtual gateway IPv4 address.
        type: string
        required: False
    active_gateway_mac_v4:
        description: VSX virtual gateway MAC address for the corresponding virtual gateway IPv4 address.
        type: string
        required: False
    state:
        description: Create/Update or Delete interface
        default: 'present'
        choices: ['present', 'absent']
        required: False

author:
    - Aruba Networks
'''

EXAMPLES = '''
     - name: Adding VLAN interface
       arubaoscx_vlan_interface:
         interface: "{{ item.interface }}"
         description: "{{ item.description }}"
       with_items:
         - { interface: vlan2, description: 'This is interface vlan2' }
         - { interface: vlan3, description: 'This is interface vlan3' }

     - name: Attaching IP addresses to interface
       arubaoscx_vlan_interface:
         interface: "{{ item.interface }}"
         ipv4: "{{ item.ipv4 }}"
         ipv6: "{{ item.ipv6 }}"
       with_items:
         - { interface: vlan2, ipv4: ['1.2.3.4/24', '1.3.4.5/24'], ipv6: ['2000:db8::1234/32', '2001:db8::1234/32'] }
         - { interface: vlan3, ipv4: ['1.4.5.6/24', '1.5.6.7/24'], ipv6: ['2002:db8::1234/32', '2003:db8::1234/32'] }

     - name: Attaching IP helper addresses to interface
       arubaoscx_vlan_interface:
         interface: "{{ item.interface }}"
         ip_helper_address: "{{ item.ip_helper_address }}"
       with_items:
         - { interface: vlan2, ip_helper_address: ['10.6.7.10'] }
         - { interface: vlan3, ip_helper_address: ['10.6.7.10', '10.10.10.10'] }

     - name: Attaching active gateway to interface
       arubaoscx_vlan_interface:
         interface: "{{ item.interface }}"
         active_gateway_ip: "{{ item.active_gateway_ip }}"
         active_gateway_mac_v4: "{{ item.active_gateway_mac_v4 }}"
       with_items:
         - { interface: vlan2, active_gateway_ip: '172.1.3.254', active_gateway_mac_v4: '98:F2:68:FF:B3:00' }
         - { interface: vlan3, active_gateway_ip: '172.1.3.254', active_gateway_mac_v4: '98:F2:68:FF:B3:00' }

     - name: Adding VLAN interface with IP addresses, VRF, IP helper address and active gateway
       arubaoscx_vlan_interface:
         interface: "{{ item.interface }}"
         description: "{{ item.description }}"
         ipv4: "{{ item.ipv4 }}"
         ipv6: "{{ item.ipv6 }}"
         vrf: "{{ item.vrf }}"
         ip_helper_address: "{{ item.ip_helper_address }}"
         active_gateway_ip: "{{ item.active_gateway_ip }}"
         active_gateway_mac_v4: "{{ item.active_gateway_mac_v4 }}"
       with_items:
         - { interface: vlan2, description: 'This is interface vlan2', ipv4: ['1.2.3.4/24'], ipv6: ['2001:db8::1234/32'], vrf: myvrf, ip_helper_address: ['10.6.7.10'], active_gateway_ip: '172.1.3.254', active_gateway_mac_v4: '98:F2:68:FF:B3:00' }
         - { interface: vlan3, description: 'This is interface vlan3', ipv4: ['1.2.4.5/24'], ipv6: ['2001:db7::1234/32'], vrf: myvrf, ip_helper_address: ['10.6.7.10'], active_gateway_ip: '172.1.3.254', active_gateway_mac_v4: '98:F2:68:FF:B3:00' }

     - name: Deleting interface
       arubaoscx_vlan_interface:
         interface: "{{ item.interface }}"
         state: "{{ item.state }}"
       with_items:
           - { interface: vlan2, state: absent }
           - { interface: vlan3, state: absent }
'''


from ansible.module_utils.basic import AnsibleModule
import json
import re
import ipaddress
import sys
from ansible.module_utils.connection import Connection


'''
Vefiry if the input IP address is valid.
'''


def valid_ip(ip):
    try:
        if sys.version_info[0] == 2:
            ipaddress.ip_network(ip.strip().decode("utf-8"), strict=True)
        elif sys.version_info[0] == 3:
            ipaddress.ip_network(bytes(ip.strip().encode("utf-8")), strict=True)
        return True
    except Exception:
        return False


def main():
    module_args = dict(
       interface=dict(type='str', required=True),
       admin_state=dict(default='up', choices=['up', 'down']),
       description=dict(type='str', default=None),
       ipv4=dict(type='list', default=None),
       ipv6=dict(type='list', default=None),
       vrf=dict(type='str', default=None),
       ip_helper_address=dict(type='list', default=None),
       active_gateway_ip=dict(type='str', default=None),
       active_gateway_mac_v4=dict(type='str', default=None),
       state=dict(default='present', choices=['present', 'absent'])
    )
    warnings = list()
    result = dict(changed=False, warnings=warnings)
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(changed=False)

    connection = Connection(module._socket_path)
    get_response = connection.get_running_config()
    module.log(msg=get_response)
    interface = module.params['interface'].lower()
    admin_state = module.params['admin_state']
    description = module.params['description']
    ipv4 = module.params['ipv4']
    ipv6 = module.params['ipv6']
    vrf = module.params['vrf']
    ip_helper_address = module.params['ip_helper_address']
    active_gateway_ip = module.params['active_gateway_ip']
    active_gateway_mac_v4 = module.params['active_gateway_mac_v4']
    state = module.params['state']

    try:
        json_data = json.loads(get_response)
    except ValueError:
        module.fail_json(msg=get_response)

    '''
    Verify if input interface string is valid
    '''
    if (len(interface.encode('utf-8')) > 8) or (not bool(re.match('^[a-zA-Z0-9/]+$', interface))):
        module.fail_json(msg='Interface is not valid.')

    '''
    Deleting interface
    '''
    if state == 'absent':
        get_json = json.loads(get_response)
        encode_interface = interface.replace('/', '%2F')
        if encode_interface in json_data["Port"].keys():
            json_data["Port"].pop(encode_interface)
        else:
            warnings.append("Interface " + interface + " has already been removed.")
        if encode_interface in json_data["System"]["bridge"]["Bridge1"].setdefault("ports", []):
            json_data["System"]["bridge"]["Bridge1"]["ports"].remove(encode_interface)
        if "Interface" in json_data.keys():
            if encode_interface in json_data["Interface"].keys():
                json_data["Interface"].pop(encode_interface)
        for item in json_data["System"]["vrfs"].keys():
            if encode_interface in json_data["System"]["vrfs"][item].setdefault("ports", []):
                json_data["System"]["vrfs"][item].get("ports").remove(encode_interface)

    '''
    Adding interface
    '''
    if state == 'present':
        get_json = json.loads(get_response)
        if interface is not None:
            vid = interface.replace('vlan', '')
            if "vlans" not in json_data["System"]["bridge"]["Bridge1"].keys():
                module.fail_json(msg='VLAN ' + str(vid) + ' should be created before creating interface ' + interface)
            if vid not in json_data["System"]["bridge"]["Bridge1"]["vlans"].keys():
                module.fail_json(msg='VLAN ' + str(vid) + ' should be created before creating interface ' + interface)
            if "Port" not in json_data:
                json_data["Port"] = {}
            json_data["Port"].setdefault(interface, {})["name"] = interface
            json_data["Port"][interface]["vlan_tag"] = interface.replace('vlan', '')
            if interface not in json_data["Port"][interface].setdefault("interfaces", []):
                json_data["Port"][interface]["interfaces"].append(interface)
            if "default" in json_data["System"]["vrfs"].keys():
                if interface not in json_data["System"]["vrfs"]["default"]["ports"]:
                    json_data["System"]["vrfs"]["default"].setdefault("ports", []).append(interface)
            else:
                json_data["System"]["vrfs"]["default"] = {"name": "default", "ports": [interface]}
            if interface not in json_data["System"]["bridge"]["Bridge1"].setdefault("ports", []):
                json_data["System"]["bridge"]["Bridge1"]["ports"].append(interface)
            module.log(msg='Added Interface: ' + interface)

        if admin_state == "up":
            json_data["Port"][interface]["admin"] = "up"
            json_data.setdefault("Interface", {})[interface] = {"name": interface, "type": "internal", "user_config": {"admin": "up"}}
        elif admin_state == "down":
            json_data["Port"][interface]["admin"] = "down"
            json_data.setdefault("Interface", {})[interface] = {"name": interface, "type": "internal", "user_config": {"admin": "down"}}

        if description is not None:
            json_data["Port"][interface]["description"] = description
            module.log(msg="Added interface with name='" + interface + "' description='" + description + "'")

        '''
        Attaching IPv4 address to interface
        '''
        if ipv4 is not None:
            json_data["Port"][interface]["ip4_address"] = ipv4[0]
            if len(ipv4) > 2:
                json_data["Port"][interface]["ip4_address_secondary"] = []
                for item in ipv4[1:]:
                    json_data["Port"][interface]["ip4_address_secondary"].append(item)
            elif len(ipv4) == 2:
                json_data["Port"][interface]["ip4_address_secondary"] = ipv4[1]
            module.log(msg='Attached IPv4 address ' + ''.join(ipv4) + ' to interface ' + interface)

        '''
        Attaching IPv6 address to interface
        '''
        if ipv6 is not None:
            if "ip6_addresses" in json_data["Port"][interface].keys():
                json_data["Port"][interface]["ip6_addresses"] = {}
            for item in ipv6:
                json_data["Port"][interface].setdefault("ip6_addresses", {})[item] =\
                    {"node_address": True, "preferred_lifetime": 604800, "ra_prefix": True, "type": "global-unicast", "valid_lifetime": 2592000}
            module.log(msg='Attached IPv6 address ' + ' '.join(ipv6) + ' to interface ' + interface)

        '''
        Attaching interface to non-default VRF
        '''
        if vrf is not None:
            if vrf not in json_data["System"]["vrfs"].keys():
                warnings.append('VRF ' + vrf + ' does not exist on switch.')
            elif interface not in json_data["System"]["vrfs"][vrf].setdefault("ports", []):
                json_data["System"]["vrfs"][vrf]["ports"].append(interface)
                if vrf != 'default' and (interface in json_data["System"]["vrfs"].get("default", {}).get("ports", [])):
                    json_data["System"]["vrfs"]["default"]["ports"].remove(interface)
                    if not json_data["System"]["vrfs"]["default"]["ports"]:
                        json_data["System"]["vrfs"].pop("default")
                module.log(msg='Attached interface ' + interface + ' to VRF ' + vrf)
            elif interface in json_data["System"]["vrfs"][vrf].get("ports", []):
                if vrf != 'default' and (interface in json_data["System"]["vrfs"].get("default", {}).get("ports", [])):
                    json_data["System"]["vrfs"]["default"]["ports"].remove(interface)
                    if not json_data["System"]["vrfs"]["default"]["ports"]:
                        json_data["System"]["vrfs"].pop("default")

        '''
        Attaching helper-address to interface
        '''
        if ip_helper_address is not None:
            if (vrf is not None) and (vrf in json_data["System"]["vrfs"].keys()):
                vrf_dhcp = vrf
            else:
                vrf_dhcp = "default"
            dhcp_name = vrf_dhcp + "/" + interface
            if len(ip_helper_address) <= 1:
                json_data.setdefault("DHCP_Relay", {})[dhcp_name] = {"ipv4_ucast_server": ip_helper_address[0], "port": interface, "vrf": vrf_dhcp}
            else:
                json_data.setdefault("DHCP_Relay", {})[dhcp_name] = {"ipv4_ucast_server": [], "port": interface, "vrf": vrf_dhcp}
                for item in ip_helper_address:
                    json_data["DHCP_Relay"][dhcp_name]["ipv4_ucast_server"].append(item)
                    json_data["DHCP_Relay"][dhcp_name]["ipv4_ucast_server"].sort()

        '''
        Attaching active gateway to interface
        '''
        if (active_gateway_ip is None) and (active_gateway_mac_v4 is not None):
            warnings.append("Both active_gateway_ip and active_gateway_mac_v4 are required for configure active gateway.")
        if (active_gateway_ip is not None) and (active_gateway_mac_v4 is not None):
            json_data["Port"][interface]["vsx_virtual_ip4"] = active_gateway_ip
            json_data["Port"][interface]["vsx_virtual_gw_mac_v4"] = active_gateway_mac_v4

    '''
    Updating running config on remote switch
    '''
    connection.put_running_config(json.dumps(json_data))

    '''
    Writing Debugging File
    '''
    with open('/tmp/debugging_running_config.json', 'w') as to_file:
        json.dump(json_data, to_file, indent=4)
        to_file.write("\n")

    '''
    Checking if change is idempotent
    '''
    if get_json != json_data:
        result["changed"] = True
    else:
        module.log(msg="========Nothing Changed=========")

    module.exit_json(**result)


if __name__ == '__main__':
    main()
