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
module: arubaoscx_vlan

version_added: "1.0"

description:
    - "This module implements VLAN configuration for ArubaOS_CX switch"

options:
    vlan_id:
        description: The ID of this VLAN. Non-internal VLANs must have an 'id'
                     betwen 1 and 4094 to be effectively instantiated.
        required: true
    name:
        description: VLAN name
        required: false
    description:
        description: VLAN description
        required: false
    interfaces:
        description: Interfaces attached to VLAN
        required: False
    state:
        description: Create/Update or Delete VLAN
        default: present
        choices: ['present', 'absent']
        required: False

author:
    - Aruba Networks
'''

EXAMPLES = '''
     - name: Adding new VLAN
       arubaoscx_vlan:
         vlan_id: "{{ item.vlan_id }}"
         name: "{{ item.name }}"
         description: "{{ item.description }}"
       with_items:
           - { vlan_id: 2, name: VLAN2, description: 'This is VLAN2' }
           - { vlan_id: 3, name: VLAN3, description: 'This is VLAN3' }

     - name: Attaching interfaces to VLAN
       arubaoscx_vlan:
         vlan_id: "{{ item.vlan_id }}"
         interfaces: "{{ item.interfaces }}"
       with_items:
           - { vlan_id: 2, interfaces: ['1/1/3', '1/1/4'] }
           - { vlan_id: 3, interfaces: ['1/1/5', '1/1/6'] }

     - name: Adding new VLAN with name, description and interfaces
       arubaoscx_vlan:
         vlan_id: "{{ item.vlan_id }}"
         name: "{{ item.name }}"
         description: "{{ item.description }}"
         interfaces: "{{ item.interfaces }}"
       with_items:
           - { vlan_id: 2, name: VLAN2, description: 'This is VLAN2',
               interfaces: ['1/1/3', '1/1/4'] }
           - { vlan_id: 3, name: VLAN3, description: 'This is VLAN3',
               interfaces: ['1/1/5', '1/1/6'] }

     - name: Deleting VLAN
       arubaoscx_vlan:
         vlan_id: "{{ item.vlan_id }}"
         state: "{{ item.state }}"
       with_items:
           - { vlan_id: 2, state: absent }
           - { vlan_id: 3, state: absent }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
import json
import re


def main():
    module_args = dict(
        vlan_id=dict(type='int', required=True),
        name=dict(type='str', default=None),
        description=dict(type='str', default=None),
        interfaces=dict(type='list', default=None),
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
    vid = module.params['vlan_id']
    name = module.params['name']
    description = module.params['description']
    interfaces = module.params['interfaces']
    state = module.params['state']
    try:
        json_data = json.loads(get_response)
    except ValueError:
        module.fail_json(msg=get_response)

    get_json = json.loads(get_response)

    '''
    Deleting VLAN
    '''
    if state == 'absent':
        if "vlans" in json_data["System"]["bridge"]["Bridge1"].keys():
            if str(vid) in json_data["System"]["bridge"]["Bridge1"]["vlans"]\
                           .keys():
                json_data["System"]["bridge"]["Bridge1"]["vlans"].pop(str(vid))
                for item in json_data["Port"].values():
                    for v in item.values():
                        if v == str(vid):
                            item.pop("vlan_tag")
            else:
                warnings.append("VLAN " + str(vid) + " has already been removed")
        warnings.append("All VLANs have already been removed")

    '''
    Adding new VLAN
    '''
    if state == "present":
        if "vlans" not in json_data["System"]["bridge"]["Bridge1"].keys():
            json_data["System"]["bridge"]["Bridge1"]["vlans"] = {}
        if str(vid) in json_data["System"]["bridge"]["Bridge1"]["vlans"].keys():
            module.log("VLAN " + str(vid) + " already exist.")
        if name is not None:
            json_data["System"]["bridge"]["Bridge1"]["vlans"][str(vid)] = \
                {"admin": "up", "id": vid, "type": "static", "name": name}
            module.log(msg="Added VLAN " + str(vid) + " with name: " + name)
        else:
            json_data["System"]["bridge"]["Bridge1"]["vlans"][str(vid)] = \
                {"admin": "up", "id": vid, "type": "static", "name": "VLAN" + str(vid)}
            module.log(msg="Added VLAN " + str(vid) + " with name: " + "VLAN" +
                           str(vid))

        if description is not None:
            json_data["System"]["bridge"]["Bridge1"]["vlans"][str(vid)]["description"] = \
                description
            module.log(msg="Added description " + description + " to VLAN " + str(vid))

        '''
        Attaching interface to VLAN
        '''
        if interfaces is not None:
            '''
            Removing interfaces that already attached to VLAN
            '''
            for k, v in json_data.setdefault("Port",{}).items():
                if "vlan_tag" in v.keys():
                    if (v["vlan_tag"] == str(vid)):
                        json_data["Port"][k].pop("vlan_mode")
                        json_data["Port"][k].pop("vlan_tag")
            '''
            Adding interfaces to VLAN
            '''
            for item in interfaces:
                item = item.strip()
                if (len(item.encode('utf-8')) > 8) or (not bool(re.match('^[a-zA-Z0-9/]+$',
                                                       item))):
                    module.fail_json(msg='Interface ' + item + ' is not valid.')
                encode_interface = item.replace('/', '%2F')
                if encode_interface not in json_data["Port"]:
                    json_data["Port"][encode_interface] = {}
                    json_data["Port"][encode_interface]["interfaces"] = [encode_interface]
                    json_data["Port"][encode_interface]["name"] = item

                json_data["Port"][encode_interface]["vlan_mode"] = "access"
                json_data["Port"][encode_interface]["vlan_tag"] = str(vid)
                if encode_interface not in json_data["System"]["bridge"]["Bridge1"].setdefault("ports",[]):
                    json_data["System"]["bridge"]["Bridge1"]["ports"].append(encode_interface)

                '''
                Disable routing on interface
                '''
                if encode_interface in json_data["System"]["vrfs"].setdefault("default", {}).\
                        setdefault("ports", []):
                    json_data["System"]["vrfs"]["default"]["ports"].remove(encode_interface)
            if not json_data["System"]["vrfs"]["default"]["ports"]:
                json_data["System"]["vrfs"].pop("default")

    '''
    Checking if change is idempotent
    '''
    if get_json != json_data:
        result["changed"] = True
        connection.put_running_config(json.dumps(json_data))
    else:
        module.log("========No Change=========")

    '''
    Writing debugging file
    '''
    with open('/tmp/debugging_running_config.json', 'w') as to_file:
        json.dump(json_data, to_file, indent=4)
        to_file.write("\n")
    module.exit_json(**result)


if __name__ == '__main__':
    main()
