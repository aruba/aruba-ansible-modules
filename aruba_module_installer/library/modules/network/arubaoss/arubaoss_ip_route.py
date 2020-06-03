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
module: any_cli

short_description: implements rest api for static routing

version_added: "2.4"

description:
    - "This implements static routing rest api and global routing configuration"

extends_documentation_fragment:
    - arubaoss_rest

options:
    ip_route_mode:
        description:
            - Mode for route type
        choices: 'IRM_GATEWAY','IRM_REJECT','IRM_VLAN','IRM_BLACK_HOLE','IRM_TUNNEL_ARUBA_VPN'
        required: true
    destination_vlan:
        description:
            - vlan id for IRM_VLAN mode.
        required: false
    metric:
        description:
            - ip route metric
        default= 1
        required: false
    distance:
        description:
            - ip route distance
        defualt: 1
        required: false
    name:
        description:
            - name for ip route being configured
        required: false
    tag:
        description:
            - Tag that can be used to filter redistribution of this route via route-maps
        required: false
    logging:
        description:
            - if the packets received on the route need to be logged
        required: false
    ip_version:
        description:
            - Ip address type to be configured
        defualt: IAV_IPV_V4
        required: false
    gateway:
        description:
            - IP address of the gateway to forward traffic when route mode is IRM_GATEWAY
        required: false
    mask:
        description:
            - Subnet for the ip route.
        required: false
    destination:
        description:
            - IP address for the ip routed
        required: false
    bfd_ip_address:
        description:
            - Enable BFD for static routes. Only for Lava and Bolt platforms.
        required: false
    vlan_name:
        description:
            - vlan id/name to which route is being applied
        required: false


author:
    - Ashish Pant (@hpe)
'''

EXAMPLES = '''
     - name: add route vlan
       arubaoss_ip_route:
         ip_route_mode: IRM_VLAN
         ip_version: IAV_IP_V4
         destination: 1.1.1.0
         mask: 255.255.255.0
         destination_vlan: 20
         name: "test"

     - name: add route vlan
       arubaoss_ip_route:
         ip_route_mode: IRM_VLAN
         ip_version: IAV_IP_V4
         destination: 1.1.1.0
         mask: 255.255.255.0
         destination_vlan: 20
         name: "test"


     - name: add route blackhole
       arubaoss_ip_route:
         ip_route_mode: IRM_BLACK_HOLE
         ip_version: IAV_IP_V4
         destination: 2.2.2.0
         mask: 255.255.255.0

     - name: delete route vlan
       arubaoss_ip_route:
         ip_route_mode: IRM_VLAN
         destination_vlan: 20
         destination: 1.1.1.0
         mask: 255.255.255.0
         state: delete

     - name: delete route blackhole
       arubaoss_ip_route:
         ip_route_mode: IRM_BLACK_HOLE
         destination: 2.2.2.0
         mask: 255.255.255.0
         state: delete

     - name: delete route blackhole
       arubaoss_ip_route:
         ip_route_mode: IRM_BLACK_HOLE
         destination: 2.2.2.0
         mask: 255.255.255.0
         state: delete

'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.arubaoss.arubaoss import run_commands,get_config
from ansible.module_utils.network.arubaoss.arubaoss import arubaoss_argument_spec, arubaoss_required_if
from ansible.module_utils._text import to_text


def route(module):

    params = module.params
    url = "/ip-route"
    data={}

    route_type = params['ip_route_mode']
    if route_type == 'IRM_VLAN':
        for key in ['destination_vlan','vlan_name']:
            if key not in params:
                return {'msg': '{} is required for {}'.format(key,route_type),
                        'changed': False}

    data = {'ip_route_mode': params['ip_route_mode'],
            'metric': params['metric'],
            'distance': params['distance']
            }

    if route_type == 'IRM_GATEWAY':
        if 'gateway' not in params:
            return {'msg': 'gateway is required for {}'.format(route_type),
                    'changed': False}
        else:
            data['gateway'] = {'version': params['ip_version'],
                    'octets': params['gateway']                                                                                      }

    if params['logging'] and route_type == 'IRM_BLACK_HOLE':
            data['logging'] = params['logging']

    for key in ['destination','mask','bfd_ip_address']:
        if params[key]:
            data[key] = {}
            data[key]['version'] = params['ip_version']
            data[key]['octets'] = params[key]

    if params['tag']:
        data['tag'] = params['tag']


    if route_type == 'IRM_GATEWAY':
        check_url = url + "/" + params['destination'] + "-" + params['mask'] + "-" +\
            params['ip_route_mode'] + "-" + params['gateway']
    else:
        check_url = url + "/" + params['destination'] + "-" + params['mask'] + "-" +\
            params['ip_route_mode']

    if params['destination_vlan']:
        vlan_url = '/vlans/' + str(params['destination_vlan'])
        check_vlan = get_config(module,vlan_url)
        if not check_vlan:
            return {'msg': 'Vlan {} not configured'.format(params['destination_vlan']),
                    'changed':False}


        data['id'] = params['destination'] + "-" +params['mask'] + "-" +\
                params['ip_route_mode'] + "-" + str(params['destination_vlan'])

        data['destination_vlan'] = {'vlan_id':params['destination_vlan'],
                                    'vlan_name': params['vlan_name']
                                    }

        check_url = check_url + '-' + str(params['destination_vlan'])

    if params['state'] == 'create':
        result = run_commands(module, url, data, 'POST',check=check_url)
    else:
        result = run_commands(module, check_url, {}, 'DELETE',check=check_url)

    return result


def run_module():
    module_args = dict(
        state=dict(type='str', required=False, default='create',
            choices=['create','delete']),
        ip_route_mode=dict(type='str', required=True, choices=['IRM_GATEWAY',
            'IRM_REJECT','IRM_VLAN','IRM_BLACK_HOLE','IRM_TUNNEL_ARUBA_VPN']),
        destination_vlan=dict(type='int', required=False,default=False),
        metric=dict(type='int', required=False,default=1),
        distance=dict(type='int', required=False,default=1),
        name=dict(type='str', required=False,default=''),
        tag=dict(type='int', required=False,default=0),
        logging=dict(type='bool', required=False,default=False),
        ip_version=dict(type='str', required=False, default='IAV_IP_V4'),
        gateway=dict(type='str', required=False,default=''),
        mask=dict(type='str', required=True),
        destination=dict(type='str', required=True),
        bfd_ip_address=dict(type='str', required=False,default=''),
        vlan_name=dict(type='str', required=False, default=""),
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
        result = route(module)
    except Exception as err:
        return module.fail_json(msg=err)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
