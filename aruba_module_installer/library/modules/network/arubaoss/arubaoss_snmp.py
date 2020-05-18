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
module: arubaoss_snmp

short_description: implements rest api for snmp configuration

version_added: "2.6"

description:
    - "This implements rest api's which configure snmp on device"

extends_documentation_fragment:
    - arubaoss_rest

options:
    commmunity_nme:
        description:
            - snmp community name. Required when configuring community
        required: false
    access_type:
        description:
            - Type of access required. Operator or Manager.
        required: false
    restricted:
        description:
            - Extent of access restricted or unrestricted
        required: false
    host_ip:
        description:
            - Snmp host ip address
        required: false
    version:
        description:
            - Host IP address version
        required: false
    informs:
        description:
            - Enable/disables informs to host
        required: false
    inform_timeout:
        description:
            - Timeout for informs
        required: false
    inform_retires:
        description:
            - Retries required for informs
        required: false
    trap_level:
        description:
            - Trap level for host
        required: false
    use_oobm:
        description:
            - Enable/disable oobm port usage
        required: false
    location:
        description:
            - Server location
        required: false
    contact:
        description:
            - Server contact
        required: false


author:
    - Ashish Pant (@hpe)
'''

EXAMPLES = '''
      - name: configure snmp community
        arubaoss_snmp:
          community_name: test
          access_type: "{{item}}"
        with_items:
          - UT_MANAGER
          - UT_MANAGER
          - UT_OPERATOR
          - UT_OPERATOR

      - name: configure snmp community
        arubaoss_snmp:
          community_name: test
          access_type: "{{item.role}}"
          restricted: "{{item.res}}"
        with_items:
          - {"role":"UT_MANAGER","res":False}
          - {"role":"UT_MANAGER","res":True}
          - {"role":"UT_MANAGER","res":True}
          - {"role":"UT_OPERATOR","res":False}
          - {"role":"UT_OPERATOR","res":True}
          - {"role":"UT_OPERATOR","res":True}


      - name: configure snmp host
        arubaoss_snmp:
          community_name: test
          host_ip: "{{item}}"
        with_items:
          - 10.1.1.1
          - 10.1.1.1

      - name: configure snmp host inform
        arubaoss_snmp:
          community_name: test
          host_ip: 10.1.1.1
          informs: "{{item}}"
        with_items:
          - True
          - True
          - False

      - name: configure snmp host inform retry timeout
        arubaoss_snmp:
          community_name: test
          host_ip: 10.1.1.1
          informs: True
          inform_retries: "{{item.retry}}"
          inform_timeout: "{{item.timeout}}"
        with_items:
          - {"retry":10,"timeout":20}
          - {"retry":100,"timeout":200}

      - name: delete snmp host inform retry timeout
        arubaoss_snmp:
          community_name: test
          informs: False

      - name: configure snmp host trap-level
        arubaoss_snmp:
          community_name: test
          host_ip: 10.1.1.1
          trap_level: "{{item}}"
        with_items:
          - STL_ALL
          - STL_CRITICAL
          - STL_NOT_INFO
          - STL_DEBUG
          - STL_NONE

      - name: configure snmp host inform retry timeout traplevel
        arubaoss_snmp:
          community_name: test
          host_ip: 10.1.1.1
          informs: True
          inform_retries: "{{item.retry}}"
          inform_timeout: "{{item.timeout}}"
          trap_level: "{{item.trap}}"
        with_items:
          - {"retry":10,"timeout":20,"trap":"STL_CRITICAL"}
          - {"retry":100,"timeout":200,"trap":"STL_DEBUG"}

      - name: configure snmp host oobm
        arubaoss_snmp:
          community_name: test
          host_ip: 10.1.1.1
          use_oobm: "{{item}}"
        with_items:
          - True
          - True

      - name: delete snmp host
        arubaoss_snmp:
          community_name: test
          state: delete
          host_ip: 10.1.1.1

      - name: configure snmp host
        arubaoss_snmp:
          community_name: test
          host_ip: 10.1.1.1
          state : delete


      - name: delete snmp community
        arubaoss_snmp:
          community_name: test
          state: delete

      - name: delete snmp community
        arubaoss_snmp:
          community_name: test
          state: delete

      - name: snmp contact and location
        arubaoss_snmp:
          location: lab
          contact: test_lab

      - name: delete snmp location
        arubaoss_snmp:
          location: lab
          state: delete

      - name: delete snmp contact
        arubaoss_snmp:
          contact: test_lab
          state: delete

'''


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.arubaoss.arubaoss import run_commands,get_config
from ansible.module_utils.network.arubaoss.arubaoss import arubaoss_argument_spec, arubaoss_required_if


def community(module):

    params = module.params
    url = '/snmp-server/communities'
    check_url = url + '/' + params['community_name']

    if params['state'] == 'create':
        snmp_config = get_config(module, check_url)
        if snmp_config:
            url = check_url
            method = 'PUT'
        else:
            method = 'POST'

        data = {
                'access_type': params['access_type'],
                'community_name': params['community_name'],
                'restricted': params['restricted']
                }

    else:
        url = check_url
        method = 'DELETE'
        data = {}

    result = run_commands(module, url, data, method, check=check_url)

    return result


def host(module):

    params = module.params
    url = '/snmp-server/hosts'

    for key in ['host_ip','version']:
        if not params[key]:
            return {'msg': 'Missing {} in parameter list'.format(key), 'changed': False}

    check_url = url + '/' + params['host_ip'] + '-' + params['community_name']
    if params['state'] == 'create':

        check_host = get_config(module, check_url)
        if check_host:
            method = 'PUT'
            url = check_url
        else:
            method = 'POST'
        data = {
                'host_ip': {
                    'octets': params['host_ip'],
                    'version': params['version']
                    },
                'community': params['community_name'],
                'trap_level': params['trap_level'],
                'informs': params['informs'],
                'use_oobm': params['use_oobm'],
                }

        if params['informs']:
            data.update({
                'informs': params['informs'],
                'inform_timeout': params['inform_timeout'],
                'inform_retries': params['inform_retries']
                })

    else:
        data = {}
        method = 'DELETE'
        url = check_url

    result = run_commands(module, url, data, method, check=check_url)

    return result


def loc_contact(module):

    params = module.params
    url = '/system'
    data = {}

    if params['state'] == 'create':

        if params['location']:
            data['location'] = params['location']

        if params['contact']:
            data['contact'] = params['contact']
    else:
        if params['location']:
            data['location'] = ""

        if params['contact']:
            data['contact'] = ""


    result = run_commands(module, url, data, 'PUT', check=url)

    return result


def run_module():
    module_args = dict(
        state=dict(type='str', required=False, default='create',
            choices=['create','delete']),
        community_name=dict(type='str', required=False),
        access_type=dict(type='str', required=False, default='UT_OPERATOR',
            choices=['UT_OPERATOR','UT_MANAGER']),
        restricted=dict(type='bool', required=False, default=True),
        host_ip=dict(type='str', required=False),
        version=dict(type='str', required=False, default='IAV_IP_V4'),
        trap_level=dict(type='str', required=False, default='STL_NONE',
            choices=['STL_ALL','STL_CRITICAL','STL_NOT_INFO','STL_DEBUG',
                'STL_NONE']),
        informs=dict(type='bool', required=False, default=False),
        inform_timeout=dict(type='int', required=False, default=15),
        inform_retries=dict(type='int', required=False, default=3),
        use_oobm=dict(type='bool', required=False, default=False),
        location=dict(type='str', required=False),
        contact=dict(type='str', required=False),
    )

    module_args.update(arubaoss_argument_spec)

    resuult = dict(changed=False,warnings='Not Supported')

    module = AnsibleModule(
        required_if=arubaoss_required_if,
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    try:
        if module.params['host_ip']:
            result = host(module)
        elif module.params['community_name']:
            result = community(module)
        else:
            result = loc_contact(module)
    except Exception as err:
        return module.fail_json(msg=err)

    module.exit_json(**result)


def main():
    run_module()

if __name__ == '__main__':
    main()
