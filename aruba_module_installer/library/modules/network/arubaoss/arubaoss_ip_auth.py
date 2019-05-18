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
module: arubaoss_ip_auth

short_description: implements rest api for ip authorization

version_added: "2.6"

description:
    - "This implements rest api's which configure ip autorization on device"

options:
    auth_ip:
        description:
            - Ip address for autherization.
        required: false
    access_role:
        description:
            - Type of access to be allowed.
        required: false
        choices: AR_MANAGER, AR_OPERATOR
    mask:
        description:
            - Net mask for auth_ip.
        required: false
    access_method:
        description:
            - Type of access method allowed.
        required: false
    auth_id:
        description:
            - Sequence number for auth rule
        required: false
    state:
        description:
            - Enable/disable/read ip auth data
        required: false
        default: create
        choices: create, delete


author:
    - Ashish Pant (@hpe)
'''

EXAMPLES = '''
      - name: create ip auth all
        arubaoss_ip_auth:
          auth_ip: 10.0.12.91
          mask: 255.255.248.0
          access_role: AR_MANAGER
          access_method: AM_ALL
        register: auth_1

      - name: delete ip auth all
        arubaoss_ip_auth:
          auth_ip: 10.0.12.92
          auth_id: "{{auth_1.id}}"
          state: delete
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.arubaoss.arubaoss import run_commands,get_config
from ansible.module_utils.network.arubaoss.arubaoss import arubaoss_argument_spec
from ansible.module_utils._text import to_text


def ip_auth(module):

    params=module.params
    url = '/ip_auth'

    if params['auth_id']:
        url = url + '/' + str(params['auth_id'])

    if params['state'] == 'create':
        if not params['mask'] or not params['auth_ip']:
            return {'msg': 'Required args: auth_ip, mask','changed':False}

        data = {
                'auth_ip': {
                    'octets': params['auth_ip'],
                    'version': 'IAV_IP_V4'
                    },
                'auth_ip_mask': {
                    'octets': params['mask'],
                    'version': 'IAV_IP_V4',
                    },
                'access_role': params['access_role'],
                'access_method': params['access_method']
                }

        if not params['auth_id']:
            auth_check = get_config(module, url)
            if auth_check:
                check_config = module.from_json(to_text(auth_check))
                total = 0
                check = 0

                for ele in check_config['ip_auth_element']:
                    for key in data:
                        if key in ele:
                            if ele[key] != data[key]:
                                check += 1
                                break

                total = check_config['collection_result']['total_elements_count']
                print("COUNT",total,check)
                diff = total - check
                if (total > 1 and diff == 1) or (total == 1 and check == 0):
                    return {'msg': 'Ip auth rule already exists.','changed':False}


            result = run_commands(module, url, data, 'POST')
        else:
            result = run_commands(module, url, data, 'PUT',check=url)

    else:
        if not params['auth_id']:
            return {'msg': 'auth_id is required for deletion','changed':False}

        result = run_commands(module, url, {}, 'DELETE',check=url)

    return result


def run_module():
    module_args = dict(
        state=dict(type='str', required=False, default='create',
            choices=['create','delete']),
        auth_ip=dict(type='str', required=False),
        access_role=dict(type='str', required=False,choices=['AR_MANAGER','AR_OPERATOR']),
        mask=dict(type='str', required=False),
        access_method=dict(type='str', required=False,defualt='AM_ALL',
            choices=['AM_ALL','AM_SSH','AM_TELNET','AM_WEB','AM_SNMP','AM_TFTP']),
        auth_id=dict(type='int', required=False),
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
        result = ip_auth(module)
    except Exception as err:
        return module.fail_json(msg=err)

    module.exit_json(**result)


def main():
    run_module()

if __name__ == '__main__':
    main()
