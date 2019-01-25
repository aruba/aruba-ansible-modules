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
module: arubaoscx_l2_interface

version_added: "1.0"

description:
    - "This module implements Layer2 Interface configuration for ArubaOS_CX switch"

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
    vlan_mode:
        description: VLAN mode of access or trunk.
        default: 'access'
        choices: ['access', 'trunk']
    vlan_id:
        description: VLAN attached to the interface.
        type: list
        required: False
    vlan_trunk_native_id:
        description: Native ID of trunk VLAN.
        type: string
        required: False
    vlan_trunk_native_tag:
        description: Switching trunk VLAN between "native_untagged" and "native_tagged".
        default: False
        bool: ['true', 'false']
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
    state:
        description: Create/Update or Delete interface.
        default: 'present'
        choices: ['present', 'absent']
        required: False

author:
    - Aruba Networks
'''

EXAMPLES = '''
     - name: Adding new interface
       arubaoscx_l2_interface:
         interface: "{{ item.interface }}"
         description: "{{ item.description }}"
       with_items:
         - { interface: 1/1/3, description: 'This is interface 1/1/3' }
         - { interface: 1/1/4, description: 'This is interface 1/1/4' }

     - name: Attaching VLAN to interface
       arubaoscx_l2_interface:
         interface: "{{ item.interface }}"
         vlan_mode: " {{ item.vlan_mode }}"
         vlan_id: "{{ item.vlan_id }}"
       with_items:
         - { interface: 1/1/3, vlan_mode: access, vlan_id: [1] }
         - { interface: 1/1/4, vlan_mode: trunk, vlan_id: [2,3,4] }

     - name: Attaching QoS to interface
       arubaoscx_l2_interface:
         interface: "{{ item.interface }}"
         vlan_mode: "{{ item.vlan_mode }}"
         qos_rate: "{{ item.qos_rate }}"
         qos_schedule_profile: "{{ item.qos_schedule_profile }}"
       with_items:
         - { interface: 1/1/3, vlan_mode: access, qos_rate: {'unknown-unicast': 100pps,
           'broadcast': 200pps, 'multicast': 200pps}, qos_schedule_profile: dwrr }
         - { interface: 1/1/4, vlan_mode: access, qos_rate: {'unknown-unicast': 100pps,
           'broadcast': 200pps, 'multicast': 200pps}, qos_schedule_profile: dwrr }

     - name: Attaching ACL to interface
       arubaoscx_l2_interface:
         interface: "{{ item.interface }}"
         vlan_mode: "{{ item.vlan_mode }}"
         aclv4_in: "{{ item.aclv4_in }}"
         aclv6_in: "{{ item.aclv6_in }}"
         aclmac_in: "{{ item.aclmac_in }}"
       with_items:
         - { interface: 1/1/3, vlan_mode: access, aclv4_in: ipv4test1, aclv6_in: ipv6test1, aclmac_in: mactest1 }
         - { interface: 1/1/4, vlan_mode: access, aclv4_in: ipv4test2, aclv6_in: ipv6test2, aclmac_in: mactest2 }

     - name: Adding new interface with VLAN, QoS, ACL attached
       arubaoscx_l2_interface:
         interface: "{{ item.interface }}"
         description: "{{ item.description }}"
         vlan_mode: "{{ item.vlan_mode }}"
         vlan_id: "{{ item.vlan_id }}"
         qos_rate: "{{ item.qos_rate }}"
         qos_schedule_profile: "{{ item.qos_schedule_profile }}"
         aclv4_in: "{{ item.aclv4_in }}"
         aclv6_in: "{{ item.aclv6_in }}"
         aclmac_in: "{{ item.aclmac_in }}"
       with_items:
         - { interface: 1/1/3, description: 'interface description', vlan_mode: access,
             vlan_id: [1], qos_rate: {'unknown-unicast': 100pps, 'broadcast': 200pps, 'multicast': 200pps},
             qos_schedule_profile: dwrr, aclv4_in: ipv4test1, aclv6_in_type: ipv6test1, aclmac_in_type: mactest1 }
         - { interface: 1/1/4, description: 'interface description', vlan_mode: trunk,
             vlan_id: [2,3,4], qos_rate: {'unknown-unicast': 100pps, 'broadcast': 200pps, 'multicast': 200pps},
             qos_schedule_profile: dwrr, aclv4_in: ipv4test2, aclv6_in_type: ipv6test2, aclmac_in_type: mactest2 }

     - name: Deleting interface
       arubaoscx_l2_interface:
         interface: "{{ item.interface }}"
         state: "{{ item.state }}"
       with_items:
           - { interface: 1/1/3, state: absent }
           - { interface: 1/1/4, state: absent }
'''

from ansible.module_utils.basic import AnsibleModule
import json
import re
from ansible.module_utils.connection import Connection
from random import randint


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
    acl_id = name + '/' + typ
    if typ == 'mac':
        acl_in_cfg = 'aclmac_in_cfg'
    elif typ == 'ipv4' or 'ipv6':
        acl_in_cfg = 'acl' + typ[2:] + '_in_cfg'
    if ('ACL' not in json_data.keys()) or (acl_id not in json_data["ACL"].keys()):
        warnings.append("ACL " + acl_id + " does not exist on switch.")
    else:
        json_data["Port"][encode_interface][acl_in_cfg] = acl_id
        '''
        Generate a random number used by acl_in_cfg_version.
        '''
        json_data["Port"][encode_interface][acl_in_cfg + '_version'] = randint(-900719925474099, 900719925474099)
        if acl_in_cfg + '_version' in get_json["Port"].setdefault(encode_interface, {}).keys():
            get_json["Port"][encode_interface][acl_in_cfg + '_version'] = json_data["Port"][encode_interface][acl_in_cfg + '_version']


def main():
    module_args = dict(
       interface=dict(type='str', required=True),
       admin_state=dict(default='up', choices=['up', 'down']),
       description=dict(type='str', default=None),
       vlan_mode=dict(default='access', choices=['access', 'trunk']),
       vlan_id=dict(type='list', default=None),
       vlan_trunk_native_id=dict(type='str', default=None),
       vlan_trunk_native_tag=dict(type='bool', default=False),
       qos_rate=dict(type='dict', default=None),
       qos_schedule_profile=dict(type='str', default=None),
       aclv4_in=dict(type='str', default=None),
       aclv6_in=dict(type='str', default=None),
       aclmac_in=dict(type='str', default=None),
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
    vlan_mode = module.params['vlan_mode']
    vlan_id = module.params['vlan_id']
    vlan_trunk_native_id = module.params['vlan_trunk_native_id']
    vlan_trunk_native_tag = module.params['vlan_trunk_native_tag']
    qos_rate = module.params['qos_rate']
    qos_schedule_profile = module.params['qos_schedule_profile']
    aclv4_in = module.params['aclv4_in']
    aclv6_in = module.params['aclv6_in']
    aclmac_in = module.params['aclmac_in']
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
            json_data["System"]["bridge"]["Bridge1"]["ports"].remove(encode_interface)
            if "Interface" in json_data.keys():
                if encode_interface in json_data["Interface"].keys():
                    json_data["Interface"].pop(encode_interface)
        else:
            warnings.append("Interface " + interface + " has already been removed.")

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
                if encode_interface not in json_data["System"]["vrfs"]["default"]["ports"]:
                    json_data["System"]["vrfs"]["default"].setdefault("ports", []).append(encode_interface)
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
        Attaching access VLAN to interface
        '''
        if (vlan_mode == 'access') and (vlan_id is not None):
            vlan_id = vlan_id[0]
            if "vlans" not in json_data["System"]["bridge"]["Bridge1"].keys():
                warnings.append('VLAN ' + str(vlan_id) + ' does not exist on switch.')
            elif str(vlan_id) not in json_data["System"]["bridge"]["Bridge1"]["vlans"].keys():
                warnings.append('VLAN ' + str(vlan_id) + ' does not exist on switch.')
            else:
                json_data["Port"][encode_interface]["vlan_mode"] = "access"
                json_data["Port"][encode_interface]["vlan_tag"] = str(vlan_id)
            if encode_interface not in json_data["System"]["bridge"]["Bridge1"].setdefault("ports", []):
                json_data["System"]["bridge"]["Bridge1"]["ports"].append(encode_interface)
            if encode_interface in json_data["System"]["vrfs"].get("default", {}).setdefault("ports", []):
                json_data["System"]["vrfs"]["default"]["ports"].remove(encode_interface)
                if not json_data["System"]["vrfs"]["default"]["ports"]:
                    json_data["System"]["vrfs"].pop("default")
            module.log(msg='Attached interface ' + interface + ' to access VLAN ' + str(vlan_id))

        '''
        Attaching trunk VLAN to interface
        '''
        if (vlan_mode == 'trunk') and (vlan_id is not None):
            if "vlan_trunks" in json_data["Port"][encode_interface].keys():
                json_data["Port"][encode_interface]["vlan_trunks"] = []
            if encode_interface not in json_data["System"]["bridge"]["Bridge1"].setdefault("ports", []):
                json_data["System"]["bridge"]["Bridge1"]["ports"].append(encode_interface)
            if encode_interface in json_data["System"]["vrfs"].get("default", {}).setdefault("ports", []):
                json_data["System"]["vrfs"]["default"]["ports"].remove(encode_interface)
                if not json_data["System"]["vrfs"]["default"]["ports"]:
                    json_data["System"]["vrfs"].pop("default")
            for vid in vlan_id:
                if ("vlans" not in json_data["System"]["bridge"]["Bridge1"].keys()) and (vid != 1):
                    warnings.append('VLAN ' + str(vid) + ' does not exist on switch.')
                elif (str(vid) not in json_data["System"]["bridge"]["Bridge1"].get("vlans", {}).keys()) and (vid != 1):
                    warnings.append('VLAN ' + str(vid) + ' does not exist on switch.')
                else:
                    json_data["Port"][encode_interface]["vlan_mode"] = "native-untagged"
                    json_data["Port"][encode_interface]["vlan_tag"] = "1"
                    json_data["Port"][encode_interface].setdefault("vlan_trunks", []).append(str(vid))
                    module.log(msg='Attached interface ' + interface + ' to trunk VLAN ' + str(vid))
                    if vlan_trunk_native_tag:
                        json_data["Port"][encode_interface]["vlan_mode"] = "native-tagged"
                    if (vlan_trunk_native_id is not None) and\
                            (vlan_trunk_native_id in json_data["System"]["bridge"]["Bridge1"].get("vlans", {}).keys()):
                        json_data["Port"][encode_interface]["vlan_tag"] = vlan_trunk_native_id

        if (vlan_mode is not None) and (vlan_id is None):
            module.fail_json(msg='Missing vlan_id')
        elif (vlan_mode is None) and (vlan_id is not None):
            module.fail_json(msg='Missing vlan_mode')

        '''
        Attaching QoS rate to interface
        '''
        if qos_rate is not None:
            for k, v in qos_rate.items():
                number, unit = number_unit(v)
                json_data["Port"][encode_interface].setdefault("rate_limits", {})[k] = number
                json_data["Port"][encode_interface].setdefault("rate_limits", {})[k + '_units'] = unit
            module.log(msg='Applied QoS_rate ' + json.dumps(qos_rate) + ' to inteface ' + interface)

        '''
        Attaching QoS schedule profile to interface
        '''
        if qos_schedule_profile is not None:
            if "QoS" not in json_data.keys():
                warnings.append('QoS_schedule_profile ' + qos_schedule_profile + ' does not exist on switch.')
            elif qos_schedule_profile not in json_data["QoS"].keys():
                warnings.append('QoS_schedule_profile ' + qos_schedule_profile + ' does not exist on switch.')
            else:
                json_data["Port"][encode_interface]["qos"] = qos_schedule_profile
                module.log(msg='Attached QoS_schedule_profile ' + qos_schedule_profile + ' to interface ' + interface)

        '''
        Attaching ACL to interface
        '''
        if (aclv6_in is not None) or (aclv4_in is not None) or (aclmac_in is not None):
            if "aclv4_in_cfg" in json_data["Port"][encode_interface].keys():
                json_data["Port"][encode_interface].pop("aclv4_in_cfg")
                json_data["Port"][encode_interface]["aclv4_in_cfg_version"] = randint(-900719925474099, 900719925474099)
            if "aclv6_in_cfg" in json_data["Port"][encode_interface].keys():
                json_data["Port"][encode_interface].pop("aclv6_in_cfg")
                json_data["Port"][encode_interface]["aclv6_in_cfg_version"] = randint(-900719925474099, 900719925474099)
            if "aclmac_in_cfg" in json_data["Port"][encode_interface].keys():
                json_data["Port"][encode_interface].pop("aclmac_in_cfg")
                json_data["Port"][encode_interface]["aclmac_in_cfg_version"] = randint(-900719925474099, 900719925474099)
        if aclv6_in is not None:
            add_acl(aclv6_in, 'ipv6', json_data, encode_interface, get_json, warnings)
        if aclv4_in is not None:
            add_acl(aclv4_in, 'ipv4', json_data, encode_interface, get_json, warnings)
        if aclmac_in is not None:
            add_acl(aclmac_in, 'mac', json_data, encode_interface, get_json, warnings)

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
