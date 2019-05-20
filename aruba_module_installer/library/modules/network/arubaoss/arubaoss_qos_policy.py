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
module: arubaoss_qos_policy

short_description: implements rest api for qos configuration

version_added: "2.6"

description:
    - "This implements rest api's which can be used to configure qos
       on device."

options:
    class_name:
        description:
            - traffic class name
        required: false
    class_type:
        description:
            - traffic class type
        required: false
        choices: QCT_IP_V4, QCT_IP_V6
        default: QCT_IP_V4
    policy_name:
        description:
            - qos policy name
        required: true
    policy_type:
        description:
            - Type of qos. Onlye QOS_QPT is supported
        required: false
    action:
        description:
            - Type of qos action to take.
        requried: false
        default: QPAT_RATE_LIMIT
        choices: QPAT_RATE_LIMIT, QPAT_PRIORITY, QPAT_DSCP_VALUE
    action_value:
        description:
            - Value for each action.
        required: false
    sequence_no:
        description:
            - Sequence number for traffic class
        required: false


author:
    - Ashish Pant (@hpe)
'''

EXAMPLES = '''
      - name: create qos policy
        arubaoss_qos_policy:
          policy_name: my_qos

      - name: attach class to qos
        arubaoss_qos_policy:
          policy_name: my_qos
          class_name: my_class
          action: QPAT_RATE_LIMIT
          action_value: 1000
          sequence_no: "{{class_1.sequence_no}}"

      - name: delete qos policy
        arubaoss_qos_policy:
          policy_name: my_qos
          state: delete

'''


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.arubaoss.arubaoss import run_commands,get_config
from ansible.module_utils.network.arubaoss.arubaoss import arubaoss_argument_spec
from ansible.module_utils._text import to_text


def qos(module):

    params = module.params

    url = '/qos/policies'
    policy_id = params['policy_name'] + '~' + params['policy_type']

    check_url = url + '/' + policy_id

    if params['state'] == 'create':

        data = {
                'policy_name': params['policy_name'],
                'policy_type': params['policy_type'],
                }
        method = 'POST'

    else:
        # Check if qos is applied to any port
        qos_url = '/qos/ports-policies'
        qos_config = get_config(module,qos_url)
        if qos_config:
            qos_config = module.from_json(to_text(qos_config))
            for config in qos_config['qos_port_policy_element']:
                if policy_id == config['policy_id']:
                    return {'msg': 'Cannot delete policy {}, active on port {}'.\
                            format(policy_id,config['port_id']),'change':False}

        # Check if qos is applied to any port
        qos_url = '/qos/vlans-policies'
        qos_config = get_config(module,qos_url)
        if qos_config:
            qos_config = module.from_json(to_text(qos_config))
            for config in qos_config['qos_vlan_policy_element']:
                if policy_id == config['policy_id']:
                    return {'msg': 'Cannot delete policy {}, active on vlan {}'.\
                            format(policy_id,config['vlan_id']),'change':False}


        data = {}
        method = 'DELETE'
        url = check_url

    result = run_commands(module, url, data, method, check=check_url)

    return result


def qos_class(module):

    params = module.params
    policy_id = params['policy_name'] + '~' + params['policy_type']
    url = '/qos/policies/' + policy_id + '/policy-actions'

    # Create qos if not to apply actions
    if params['state'] == 'create':
        qos(module)

    method = 'POST'
    if params['sequence_no'] > 0:
        temp = url + '/' + str(params['sequence_no'])
        if get_config(module, temp):
            url = url + '/' + str(params['sequence_no'])
            method = 'PUT'


    if params['state'] == 'create':
        class_id = params['class_name'] + '~' + params['class_type']

        class_url = '/qos/traffic-classes/' + class_id

        if not get_config(module, class_url):
            return {'msg': 'class does not exist', 'changed':False}

        if params['action_value'] == -1 or not params['action']:
            return {'msg':'action and action_type are required','changed':False}

        action = params['action']
        action_value = params['action_value']

        data = {
                'policy_id': policy_id,
                'traffic_class_id': class_id,
                'first_action': {
                    'action_type': action,
                    },
                }
        if params['sequence_no'] > 0:
            data['sequence_no'] = params['sequence_no']

        if action == 'QPAT_RATE_LIMIT':
            data['first_action']['rate_limit_in_kbps'] = action_value
        elif action == 'QPAT_DSCP_VALUE':
            data['first_action']['new_dscp_value'] = action_value
        else:
            data['first_action']['new_priority'] = action_value

        qos_config = get_config(module, url)
        if qos_config:
            check_config = module.from_json(to_text(qos_config))
            if params['sequence_no'] == 0:
                for config in check_config['qos_policy_action_element']:
                    if class_id == config['traffic_class_id']:
                        return config
            elif params['sequence_no'] > 0:
                if check_config.get('traffic_class_id') and class_id == check_config['traffic_class_id']:
                    return check_config

        result = run_commands(module, url, data, method)
    else:
        if params['sequence_no'] ==0:
            return {'msg':'sequence_no is required','changed':False}
        else:
            url = url + '/' + str(params['sequence_no'])

        result = run_commands(module, url, {}, 'DELETE',check=url)

    return result


def run_module():
    module_args = dict(
        class_name=dict(type='str', required=False),
        class_type=dict(type='str', required=False,default='QCT_IP_V4',
            choices=['QCT_IP_V4','QCT_IP_V6']),
        policy_name=dict(type='str', required=True),
        policy_type=dict(type='str', required=False,default='QPT_QOS'),
        state=dict(type='str', required=False, default='create',
            choices=['create','delete']),
        action=dict(type='str', required=False, default='QPAT_RATE_LIMIT',
            choices=['QPAT_PRIORITY','QPAT_DSCP_VALUE','QPAT_RATE_LIMIT']),
        action_value=dict(type='int', reqquired=False, default=-1),
        sequence_no=dict(type='int', required=False, default=0),
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

        if module.params['class_name']:
            result = qos_class(module)
        else:
            result = qos(module)

    except Exception as err:
        return module.fail_json(msg=err)

    module.exit_json(**result)


def main():
    run_module()

if __name__ == '__main__':
    main()
