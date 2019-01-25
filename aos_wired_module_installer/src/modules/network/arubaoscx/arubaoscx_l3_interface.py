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
module: arubaoscx_l3_interface

version_added: "1.0"

description:
    - "This module implements Layer3 interface configuration for ArubaOS_CX switch"

options:
    interface:
        description: Interface name, should be alphanumeric and no more than about 8 bytes long.
        type: string
        required: true
    admin_state:
        description: Status information about interface.
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
    qos_rate:
        description: The rate limit value configured for broadcast/multicast/unknown unicast traffic.
        type: dictionary
        required: False
    qos_schedule_profile:
        description: Attaching existing QoS schedule profile to interface.
        type: string
        required: False
    aclv4_in:
        description: Attaching ingress IPv4 ACL to interface.
        type: string
        required: False
    aclv6_in:
        description: Attaching ingress IPv6 ACL to interface.
        type: string
        required: False
    aclmac_in:
        description: Attaching ingress MAC ACL to interface.
        type: string
        required: False
    aclv4_out:
        description: Attaching egress IPv4 ACL to interface.
        type: string
        required: False
    vrf:
        description: Attaching interface to VRF, commonly known as Virtual Routing and Forwarding.
                     The interface will be attached to default vrf if not specified.
        type: string
        required: False
    ip_helper_address:
        description: Configure a remote DHCP server/relay IP address on the device interface. Here the
                     helper address is same as the DHCP server address or another intermediate DHCP relay.
        type: list
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
     - name: Adding new interface
       arubaoscx_l3_interface:
         interface: "{{ item.interface }}"
         description: "{{ item.description }}"
       with_items:
         - { interface: 1/1/3, description: 'This is interface 1/1/3' }
         - { interface: 1/1/4, description: 'This is interface 1/1/4' }

     - name: Attaching IP addresses to interface
       arubaoscx_l3_interface:
         interface: "{{ item.interface }}"
         ipv4: "{{ item.ipv4 }}"
         ipv6: "{{ item.ipv6 }}"
       with_items:
         - { interface: 1/1/3, ipv4: ['1.2.3.4/24', '1.3.4.5/24'], ipv6: ['2000:db8::1234/32', '2001:db8::1234/32'] }
         - { interface: 1/1/4, ipv4: ['1.4.5.6/24', '1.5.6.7/24'], ipv6: ['2002:db8::1234/32', '2003:db8::1234/32'] }

     - name: Attaching QoS to interface
       arubaoscx_l3_interface:
         interface: "{{ item.interface }}"
         qos_rate: "{{ item.qos_rate }}"
         qos_schedule_profile: "{{ item.qos_schedule_profile }}"
       with_items:
         - { interface: 1/1/3, qos_rate: {'unknown-unicast': 100pps, 'broadcast': 200pps, 'multicast': 200pps}, qos_schedule_profile: dwrr }
         - { interface: 1/1/4, qos_rate: {'unknown-unicast': 100pps, 'broadcast': 200pps, 'multicast': 200pps}, qos_schedule_profile: dwrr }

     - name: Attaching ACL to interface
       arubaoscx_l3_interface:
         interface: "{{ item.interface }}"
         aclv4_in: "{{ item.aclv4_in }}"
         aclv6_in: "{{ item.aclv6_in }}"
         aclmac_in: "{{ item.aclmac_in }}"
         aclv4_out: "{{ item.aclv4_out }}"
       with_items:
         - { interface: 1/1/3, aclv4_in: ipv4test1, aclv6_in: ipv6test1, aclmac_in: mactest1, aclv4_out: ipv4egress1 }
         - { interface: 1/1/4, aclv4_in: ipv4test2, aclv6_in: ipv6test2, aclmac_in: mactest2, aclv4_out: ipv4egress2 }

     - name: Attaching user configured VRF to interface
       arubaoscx_l3_interface:
         interface: "{{ item.interface }}"
         vrf: "{{ item.vrf }}"
       with_items:
         - { interface: 1/1/3, vrf: myvrf }
         - { interface: 1/1/4, vrf: myvrf }

     - name: Attaching IP helper address to interface
       arubaoscx_l3_interface:
         interface: "{{ item.interface }}"
         ip_helper_address: "{{ item.ip_helper_address }}"
       with_items:
         - { interface: 1/1/3, ip_helper_address: ['5.6.7.8', '10.10.10.10'] }
         - { interface: 1/1/4, ip_helper_address: 1.2.3.4 }

     - name: Adding new interface with IP, QoS, ACL, VRF attached
       arubaoscx_l3_interface:
         interface: "{{ item.interface }}"
         description: "{{ item.description }}"
         ipv4: "{{ item.ipv4 }}"
         ipv6: "{{ item.ipv6 }}"
         qos_rate: "{{ item.qos_rate }}"
         qos_schedule_profile: "{{ item.qos_schedule_profile }}"
         aclv4_in: "{{ item.aclv4_in }}"
         aclv6_in: "{{ item.aclv6_in }}"
         aclmac_in: "{{ item.aclmac_in }}"
         aclv4_out: "{{ item.aclv4_out }}"
         vrf: "{{ item.vrf }}"
         ip_helper_address: "{{ item.ip_helper_address }}"
       with_items:
         - { interface: 1/1/3, description: 'This is interface 1/1/3',
             ipv4: ['1.2.3.4/24'], ipv6: ['2001:db8::1234/32'],
             qos_rate: {'unknown-unicast': 100pps, 'broadcast': 200pps, 'multicast': 200pps},
             qos_schedule_profile: dwrr, aclv4_in: ipv4test1, aclv6_in_type: ipv6test1,
             aclmac_in_type: mactest1, aclv4_out: ipv4egress1, vrf: myvrf, ip_helper_address: 10.10.10.10 }
         - { interface: 1/1/4, description: 'This is interface 1/1/4',
             ipv4: ['1.3.4.5/24'], ipv6: ['2001:db7::1234/32'],
             qos_rate: {'unknown-unicast': 100pps, 'broadcast': 200pps, 'multicast': 200pps},
             qos_schedule_profile: dwrr, aclv4_in: ipv4test2, aclv6_in_type: ipv6test2,
             aclmac_in_type: mactest2, aclv4_out: ipv4egress2, vrf: myvrf, ip_helper_address: 10.10.10.10 }

     - name: Deleting interface
       arubaoscx_l3_interface:
         interface: "{{ item.interface }}"
         state: "{{ item.state }}"
       with_items:
           - { interface: 1/1/3, state: absent }
           - { interface: 1/1/4, state: absent }
'''

from ansible.module_utils.basic import AnsibleModule
import json
import re
import sys
import ipaddress
from ansible.module_utils.connection import Connection
from random import randint


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


'''
Parsing the QoS rate dictionary parameter to number and unit as desired by running configuration in JSON format.
'''


def number_unit(s):
    for i, c in enumerate(s):
        if not c.isdigit():
            break
    number = s[:i]
    unit = s[i:].lstrip()
    return number, unit


'''
Parsing aclv4_in, aclv6_in, aclmac_in parameters to ACL name with type as desired by running configuration in JSON format.
'''


def add_acl(name, typ, json_data, encode_interface, get_json, warnings):
    iptype = typ.replace('in', '').replace('out', '')
    acl_id = name + '/' + iptype
    if iptype == 'mac':
        acl_in_cfg = 'aclmac_in_cfg'
    elif iptype == 'ipv4' or 'ipv6':
        acl_in_cfg = 'acl' + iptype[2:] + '_in_cfg'
        acl_out_cfg = 'acl' + iptype[2:] + '_out_cfg'
    if ('ACL' not in json_data.keys()) or (acl_id not in json_data["ACL"].keys()):
        warnings.append("ACL " + acl_id + " does not exist on switch.")
    elif 'in' in typ:
        json_data["Port"][encode_interface][acl_in_cfg] = acl_id
        json_data["Port"][encode_interface][acl_in_cfg + '_version'] = randint(-900719925474099, 900719925474099)
        if acl_in_cfg + '_version' in get_json["Port"].setdefault(encode_interface, {}).keys():
            get_json["Port"][encode_interface][acl_in_cfg + '_version'] = json_data["Port"][encode_interface][acl_in_cfg + '_version']
    elif 'out' in typ:
        json_data["Port"][encode_interface][acl_out_cfg] = acl_id
        json_data["Port"][encode_interface][acl_out_cfg + '_version'] = randint(-900719925474099, 900719925474099)
        if acl_out_cfg + '_version' in get_json["Port"].setdefault(encode_interface, {}).keys():
            get_json["Port"][encode_interface][acl_out_cfg + '_version'] = json_data["Port"][encode_interface][acl_out_cfg + '_version']


def main():
    module_args = dict(
       interface=dict(type='str', required=True),
       admin_state=dict(default='up', choices=['up', 'down']),
       description=dict(type='str', default=None),
       ipv4=dict(type='list', default=None),
       ipv6=dict(type='list', default=None),
       qos_rate=dict(type='dict', default=None),
       qos_schedule_profile=dict(type='str', default=None),
       aclv4_in=dict(type='str', default=None),
       aclv6_in=dict(type='str', default=None),
       aclmac_in=dict(type='str', default=None),
       aclv4_out=dict(type='str', default=None),
       vrf=dict(type='str', default=None),
       ip_helper_address=dict(type='list', default=None),
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
    interface = module.params['interface']
    admin_state = module.params['admin_state']
    description = module.params['description']
    ipv4 = module.params['ipv4']
    ipv6 = module.params['ipv6']
    qos_rate = module.params['qos_rate']
    qos_schedule_profile = module.params['qos_schedule_profile']
    aclv4_in = module.params['aclv4_in']
    aclv6_in = module.params['aclv6_in']
    aclmac_in = module.params['aclmac_in']
    aclv4_out = module.params['aclv4_out']
    vrf = module.params['vrf']
    ip_helper_address = module.params['ip_helper_address']
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
            encode_interface = interface.replace('/', '%2F')
            if "Port" not in json_data:
                json_data["Port"] = {}
            json_data["Port"].setdefault(encode_interface, {})["name"] = interface
            if encode_interface not in json_data["Port"][encode_interface].setdefault("interfaces", []):
                json_data["Port"][encode_interface]["interfaces"].append(encode_interface)
            if "default" in json_data["System"]["vrfs"].keys():
                if encode_interface not in json_data["System"]["vrfs"]["default"].setdefault("ports", []):
                    json_data["System"]["vrfs"]["default"].get("ports").append(encode_interface)
            else:
                json_data["System"]["vrfs"]["default"] = {"name": "default", "ports": [encode_interface]}
            module.log(msg='Added Interface: ' + interface)

        if admin_state == "up":
            json_data["Port"][encode_interface]["admin"] = "up"
            json_data.setdefault("Interface", {})[encode_interface] = {"name": interface, "user_config": {"admin": "up"}}
        elif admin_state == "down":
            json_data["Port"][encode_interface]["admin"] = "down"
            json_data.setdefault("Interface", {})[encode_interface] = {"name": interface, "user_config": {"admin": "down"}}

        if description is not None:
            encode_interface = interface.replace('/', '%2F')
            json_data["Interface"][encode_interface]["description"] = description
            module.log(msg="Added interface with name='" + interface + "' description='" + description + "'")

        '''
        Attaching IPv4 address to interface
        '''
        if ipv4 is not None:
            json_data["Port"][encode_interface]["ip4_address"] = ipv4[0]
            if len(ipv4) > 2:
                json_data["Port"][encode_interface]["ip4_address_secondary"] = []
                for item in ipv4[1:]:
                    json_data["Port"][encode_interface]["ip4_address_secondary"].append(item)
            elif len(ipv4) == 2:
                json_data["Port"][encode_interface]["ip4_address_secondary"] = ipv4[1]
            if encode_interface in json_data["System"]["bridge"]["Bridge1"].setdefault("ports", []):
                json_data["System"]["bridge"]["Bridge1"]["ports"].remove(encode_interface)
            if "default" not in json_data["System"]["vrfs"].keys():
                json_data["System"]["vrfs"]["default"] = {"name": "default", "ports": [encode_interface]}
            elif encode_interface not in json_data["System"]["vrfs"].get("default", {}).get("ports", []):
                json_data["System"]["vrfs"]["default"]["ports"].append(encode_interface)
            module.log(msg='Attached IPv4 address ' + ''.join(ipv4) + ' to interface ' + interface)

        '''
        Attaching IPv6 address to interface
        '''
        if ipv6 is not None:
            if "ip6_addresses" in json_data["Port"][encode_interface].keys():
                json_data["Port"][encode_interface]["ip6_addresses"] = {}
            for item in ipv6:
                json_data["Port"][encode_interface].setdefault("ip6_addresses", {})[item] =\
                    {"node_address": True, "preferred_lifetime": 604800, "ra_prefix": True, "type": "global-unicast", "valid_lifetime": 2592000}
            if encode_interface in json_data["System"]["bridge"]["Bridge1"]["ports"]:
                json_data["System"]["bridge"]["Bridge1"]["ports"].remove(encode_interface)
            if "default" not in json_data["System"]["vrfs"].keys():
                json_data["System"]["vrfs"]["default"] = {"name": "default", "ports": [encode_interface]}
            elif encode_interface not in json_data["System"]["vrfs"].get("default", {}).get("ports", []):
                json_data["System"]["vrfs"]["default"]["ports"].append(encode_interface)
            module.log(msg='Attached IPv6 address ' + ' '.join(ipv6) + ' to interface ' + interface)

        '''
        Adding QoS_rate to interface
        '''
        if qos_rate is not None:
            for k, v in qos_rate.items():
                number, unit = number_unit(v)
                json_data["Port"][encode_interface].setdefault("rate_limits", {})[k] = number
                json_data["Port"][encode_interface].setdefault("rate_limits", {})[k + '_units'] = unit
            module.log(msg='Applied QoS_rate ' + json.dumps(qos_rate) + ' to inteface ' + interface)

        '''
        Attaching QoS_schedule_profile to interface
        '''
        if qos_schedule_profile is not None:
            if "QoS" not in json_data.keys():
                warnings.append('QoS_schedule_profile ' + qos_schedule_profile + ' does not exist on switch.')
            elif qos_schedule_profile not in json_data["QoS"].keys():
                warnings.append('QoS_schedule_profile ' + qos_schedule_profile + ' does not exist on switch.')
            else:
                json_data["Port"][encode_interface]["qos"] = qos_schedule_profile
                module.log(msg='Applied QoS_schedule_profile ' + qos_schedule_profile + ' to interface ' + interface)

        '''
        Attaching ACL to interface
        '''
        if (aclv6_in is not None) or (aclv4_in is not None) or (aclmac_in is not None) or (aclv4_out is not None):
            if "aclv4_in_cfg" in json_data["Port"][encode_interface].keys():
                json_data["Port"][encode_interface].pop("aclv4_in_cfg")
                json_data["Port"][encode_interface]["aclv4_in_cfg_version"] = randint(-900719925474099, 900719925474099)
            if "aclv6_in_cfg" in json_data["Port"][encode_interface].keys():
                json_data["Port"][encode_interface].pop("aclv6_in_cfg")
                json_data["Port"][encode_interface]["aclv6_in_cfg_version"] = randint(-900719925474099, 900719925474099)
            if "aclmac_in_cfg" in json_data["Port"][encode_interface].keys():
                json_data["Port"][encode_interface].pop("aclmac_in_cfg")
                json_data["Port"][encode_interface]["aclmac_in_cfg_version"] = randint(-900719925474099, 900719925474099)
            if "aclv4_out_cfg" in json_data["Port"][encode_interface].keys():
                json_data["Port"][encode_interface].pop("aclv4_out_cfg")
                json_data["Port"][encode_interface]["aclv4_out_cfg_version"] = randint(-900719925474099, 900719925474099)
        if aclv4_in is not None:
            add_acl(aclv4_in, 'ipv4in', json_data, encode_interface, get_json, warnings)
        if aclv6_in is not None:
            add_acl(aclv6_in, 'ipv6in', json_data, encode_interface, get_json, warnings)
        if aclmac_in is not None:
            add_acl(aclmac_in, 'macin', json_data, encode_interface, get_json, warnings)
        if aclv4_out is not None:
            add_acl(aclv4_out, 'ipv4out', json_data, encode_interface, get_json, warnings)

        '''
        Attaching interface to non-default VRF
        '''
        if vrf is not None:
            if vrf not in json_data["System"]["vrfs"].keys():
                warnings.append('VRF ' + vrf + ' does not exist on switch.')
            elif encode_interface not in json_data["System"]["vrfs"][vrf].get("ports", []):
                json_data["System"]["vrfs"][vrf].setdefault("ports", []).append(encode_interface)
                if vrf != 'default' and (encode_interface in json_data["System"]["vrfs"].get("default", {}).get("ports", [])):
                    json_data["System"]["vrfs"]["default"]["ports"].remove(encode_interface)
                    if not json_data["System"]["vrfs"]["default"]["ports"]:
                        json_data["System"]["vrfs"].pop("default")
                module.log(msg='Attached interface ' + interface + ' to VRF ' + vrf)
            elif encode_interface in json_data["System"]["vrfs"][vrf].get("ports", []):
                if vrf != 'default' and (encode_interface in json_data["System"]["vrfs"].get("default", {}).get("ports", [])):
                    json_data["System"]["vrfs"]["default"]["ports"].remove(encode_interface)
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
            dhcp_name = vrf_dhcp + "/" + encode_interface.replace('%2F', '%252F')
            if len(ip_helper_address) <= 1:
                json_data.setdefault("DHCP_Relay", {})[dhcp_name] = {"ipv4_ucast_server": ip_helper_address[0], "port": encode_interface, "vrf": vrf_dhcp}
            else:
                json_data.setdefault("DHCP_Relay", {})[dhcp_name] = {"ipv4_ucast_server": [], "port": encode_interface, "vrf": vrf_dhcp}
                for item in ip_helper_address:
                    json_data["DHCP_Relay"][dhcp_name]["ipv4_ucast_server"].append(item)
                    json_data["DHCP_Relay"][dhcp_name]["ipv4_ucast_server"].sort()

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
