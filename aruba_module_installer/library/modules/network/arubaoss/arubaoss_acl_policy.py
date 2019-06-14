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
module: arubaoss_acl_policy

short_description: implements rest api for global acl configuration

version_added: "2.6"

description:
    - "This implements rest api's which will configure acl policies
       standard and extended onto device"

options:
    acl_name:
        description:
            - Name for acl policy being configured.
        required: true
    acl_type:
        description:
            - Type of acl policy to be configured.
        required: false
        default: AT_STANDARD_IPV4
        choices: AT_STANDARD_IPV4, AT_EXTENDED_IPV4,
                 AT_CONNECTOIN_RATE_FILTER
    acl_action:
        description:
            - Type of action acl will take.
        required: false
        choices: AA_DENY, AA_PERMIT
    remark:
        description:
            - Description for acl policy
        required: false
    acl_source_address:
        description:
            - source ip address for acl policy type standard.
        required: false
    acl_source_mask:
        description:
            - net mask for source acl_source_address
        required: false
    is_log:
        description:
            - Enable/disable acl logging.
        required: false
    protocol_type:
        description:
            - Protocol type for acl filter. Applicable for extended acl.
        required: false
        choices: 'PT_GRE','PT_ESP','PT_AH','PT_OSPF','PT_PIM','PT_VRRP',
                 'PT_ICMP','PTIGMP','PT_IP','PT_SCTP','PT_TCP','PT_UDP'
    icmp_type:
        description:
            - Applies to icmp type matching this field. Only PT_ICMP
              protocol_type support icmp_code
        required: false
    icmp_code:
        description:
            - Applies to icmp code matching this field. Only PT_ICMP
              protocol_type support icmp_code
        required: false
    igmp_type:
        description:
            - Applies to igmp type matching this field. Only PT_IGMP
              protocol_type support igmp_type
        required: false
    is_connection_established:
        description:
            - is_connection_established. Only PT_TCP  protocol_type
              support is_connection_established
        required: false
    match_bit:
        description:
            - The set of tcp match bits . Only PT_TCP  protocol_type
              support match_bit
        required: false
    source_port:
        description:
            - Applies to source port matching this filter. Only PT_SCTP,
              PT_TCP and PT_UDP Protocol types support source_port
        required: false
    destination_port:
        description:
            - Applies to destination port matching this filter. Only
              PT_SCTP,PT_TCP and PT_UDP Protocol types support destination_port
        required: false
    source_ip_address:
        description:
            - Applies to source IP Address/Subnet matching this extended acl filter
        required: false
    source_ip_mask:
        description:
            - Net mask source_ip_address
        required: false
    destination_ip_address:
        description:
            - Applies to destination IP Address/Subnet matching this extended acl filter
        required: false
    device_type:
        description:
            - Applies to device type matching this extended acl filter
        required: false
    application_type:
        description:
            - Applies to application matching this extended acl filter
        required: fasle
    precedence:
        description:
            - IP precedence flag
        required: false
        choices: 0, 1, 2, 3, 4, 5, 6, 7
    tos:
        description:
            - Tos value
        required: false
        choices: 0, 2, 4, 8
    sequece_no:
        description:
            - Sequence number for the acl policy configured
        required: false
    state:
        description:
            - Create or deletes acl policy.
        required: false
        default: create
        choices: create, delete


author:
    - Ashish Pant (@hpe)
'''

EXAMPLES = '''
      - name: add extended acl
        arubaoss_acl_policy:
          acl_name: test1
          icmp_code: 1
          icmp_type: 1
          source_ip_address: 0.0.0.0
          source_ip_mask: 255.255.255.255
          destination_ip_address: 0.0.0.0
          destination_ip_mask: 255.255.255.255
          protocol_type: "PT_ICMP"
          acl_action: AA_PERMIT

      - name: add extended acl
        arubaoss_acl_policy:
          acl_name: test
          icmp_code: 1
          icmp_type: 1
          source_ip_address: 0.0.0.0
          source_ip_mask: 255.255.255.255
          destination_ip_address: 0.0.0.0
          destination_ip_mask: 255.255.255.255
          protocol_type: "PT_ICMP"
          acl_action: AA_PERMIT
          acl_type: AT_EXTENDED_IPV4


      - name: add standard acl
        arubaoss_acl_policy:
          acl_name: "{{item.acl}}"
          source_ip_address: "{{item.ip}}"
          acl_action: "{{item.action}}"
          is_log: "{{item.log}}"
          remark: testing
        with_items:
          - {"acl":"test2","action":"AA_PERMIT","ip":"any","log":False}
          - {"acl":"test3","action":"AA_PERMIT","ip":"any","log":True}

      - name: delte acl policy
        arubaoss_acl_policy:
          acl_name: "{{item}}"
          state: delete
        with_items:
          - test2
          - test3

'''

RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
message:
    description: The output message that the sample module generates
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.arubaoss.arubaoss import run_commands,get_config
from ansible.module_utils.network.arubaoss.arubaoss import arubaoss_argument_spec
from ansible.module_utils._text import to_text


def acl(module):

    params = module.params

    url = '/acls'
    acl_id = params['acl_name'] + '~' + params['acl_type']

    check_url = url + '/' + acl_id

    if params['state'] == 'create':

        data = {
                'acl_name': params['acl_name'],
                'acl_type': params['acl_type'],
                }

        check_list = set(['AT_EXTENDED_IPV4','AT_STANDARD_IPV4','AT_CONNECTION_RATE_FILTER'])\
                - set([params['acl_type']])
        for temp in check_list:
            temp_url = url + '/' + params['acl_name'] + '~' + temp
            check_acl = get_config(module, temp_url)
            if check_acl:
                result = {'msg': '{} already exists for type {}.'.format(params['acl_name'],
                    temp),'changed':False}
                module.exit_json(**result)
        method = 'POST'

    else:
        # Check if acl is applied to any port
        port_url = '/ports-access-groups'
    	port_acl = get_config(module, port_url)
        if port_acl:
            check_config = module.from_json(to_text(port_acl))

            for ele in check_config['acl_port_policy_element']:
                if ele['acl_id'] == acl_id:
                    return {'msg': 'ACL {} applied to port {}'.format(params['acl_name'],
                        ele['port_id']),'changed':False}

        # Check if acl is applied to any vlan
        vlan_url = '/vlans-access-groups'
        vlan_acl = get_config(module, vlan_url)
        if vlan_acl:
            check_config = module.from_json(to_text(vlan_acl))

            for ele in check_config['acl_vlan_policy_element']:
                if ele['acl_id'] == acl_id:
                    result = {'msg': 'ACL {} applied to vlan {}'.format(params['acl_name'],
                        ele['vlan_id']),'changed':False}
                    module.exit_json(**result)


        data = {}
        method = 'DELETE'
        url = check_url

    result = run_commands(module, url, data, method, check=check_url)

    return result

def check_acl_rule_exists(module):
    result = False
    params = module.params
    acl_id = params['acl_name'] + '~' + params['acl_type']
    url = '/acls/' + acl_id + '/rules'

    acl_rule = get_config(module, url)
    if acl_rule:
        check_config = module.from_json(to_text(acl_rule))

        if check_config['collection_result']['total_elements_count'] == 0:
            return result

        for ele in check_config['acl_rule_element']:
            if ele['acl_action'] != params['acl_action']:
                continue
            if params['acl_type'] == 'AT_EXTENDED_IPV4':
		print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                protocol_type = ele['traffic_match']['protocol_type']
                source_ip_address = ele['traffic_match']['source_ip_address']['octets']
                source_ip_mask = ele['traffic_match']['source_ip_mask']['octets']
                destination_ip_address = ele['traffic_match']['destination_ip_address']['octets']
                destination_ip_mask = ele['traffic_match']['destination_ip_mask']['octets']

                if protocol_type != params['protocol_type'] or \
                    source_ip_address != params['source_ip_address'] or \
                    source_ip_mask != params['source_ip_mask'] or \
                    destination_ip_address != params['destination_ip_address'] or \
                    destination_ip_mask != params['destination_ip_mask']:
                        continue

                if params['protocol_type'] == 'PT_ICMP':
                    if params['icmp_type'] > -1 and ele['traffic_match']['icmp_type']:
                        if ele['traffic_match']['icmp_type'] != params['icmp_type']:
                            continue
                    if params['icmp_code'] > -1 and ele['traffic_match']['icmp_code']:
                        if ele['traffic_match']['icmp_code'] != params['icmp_code']:
                            continue
                elif params['protocol_type'] == 'PT_IGMP':
                    if params['igmp_type'] and ele['traffic_match']['igmp_type']:
                        if ele['traffic_match']['igmp_type'] != params['igmp_type']:
                            continue
                elif params['protocol_type'] == 'PT_TCP':
                    if params['is_connection_established'] and ele['traffic_match']['is_connection_established']:
                        if ele['traffic_match']['is_connection_established'] != params['is_connection_established']:
                            continue
                    if params['match_bit'] and ele['traffic_match']['match_bit']:
                        if ele['traffic_match']['match_bit'] != params['match_bit']:
                            continue
                elif params['protocol_type'] in ('PT_SCTP','PT_TCP','PT_UDP'):
                    if params['source_port'] and ele['traffic_match']['source_port']:
                        if ele['traffic_match']['source_port'] != params['source_port']:
                            continue
                    if params['destination_port'] and ele['traffic_match']['destination_port']:
                        if ele['traffic_match']['destination_port'] != params['destination_port']:
                            continue
                if params['precedence'] and ele['traffic_match']['precedence']:
                    if ele['traffic_match']['precedence'] != params['precedence']:
                        continue

                if params['tos'] and ele['traffic_match']['tos']:
                    if ele['traffic_match']['tos'] != params['tos']:
                        continue
                if params['is_log'] is not None and ele['is_log']:
                    if ele['is_log'] != params['is_log']:
                        continue

            else:

                if params['acl_source_address'] == 'host':
                    source_ip_mask = '255.255.255.255'
                    source_ip_address = '0.0.0.0'
                else:
                    source_ip_address = params['acl_source_address']
                    source_ip_mask = params['acl_source_mask']

                if source_ip_address != ele['std_source_address']['source_ip_address']['octets']:
                    continue
                if source_ip_mask != ele['std_source_address']['source_ip_mask']['octets']:
                    continue

            #Return True as we checked all values found to be matching.
            return True

    #End of for loop, Searched all entries no match found.
    return result

def acl_rule(module):

    params = module.params
    acl_id = params['acl_name'] + '~' + params['acl_type']
    url = '/acls/' + acl_id + '/rules'
    # Create acl if not to apply actions
    if params['state'] == 'create':
        acl(module)

    data = {}

    if params['state'] == 'create':

        data.update({
            'acl_id': acl_id,
            'acl_action': params['acl_action'],
            })

        if params['remark']:
            data['remark'] = params['remark']

        if params['is_log'] != None:
            data['is_log'] = params['is_log']

        if params['acl_type'] == 'AT_EXTENDED_IPV4':
            for key in ['source_ip_address','source_ip_mask','destination_ip_address',
                    'destination_ip_mask']:
                if params.get(key) == None:
                    return {'msg':'{} is required for extended acl policy'.format(key),
                            'changed':False}

            protocol = params.get('protocol_type')
            if not protocol:
                return {'msg': 'protocol_type is required','changed':False}

            version = 'IAV_IP_V4'

            data.update({
                "traffic_match": {
                    "protocol_type": params['protocol_type'],
                    "source_ip_address": {
                        "version": version,
                        "octets": params['source_ip_address']
                        },
                    "source_ip_mask": {
                        "version": version,
                        "octets": params['source_ip_mask']
                        },
                    "destination_ip_address": {
                        "version": version,
                        "octets": params['destination_ip_address']
                        },
                    "destination_ip_mask": {
                        "version": version,
                        "octets": params['destination_ip_mask']
                        }
                    }
                })

            if protocol == 'PT_ICMP':
                if params['icmp_type'] > -1:
                    data['traffic_match']['icmp_type'] = params['icmp_type']
                if params['icmp_code'] > -1:
                    data['traffic_match']['icmp_code'] = params['icmp_code']

            if protocol == 'PT_IGMP':
                if params['igmp_type']:
                    data['traffic_match']['igmp_type'] = params['igmp_type']

            if protocol == 'PT_TCP':
                if params['is_connection_established']:
                    data['traffic_match']['is_connection_established'] = params['is_connection_established']

                if params['match_bit']:
                    data['traffic_match']['match_bit'] = params['match_bit']

            if protocol in ('PT_SCTP','PT_TCP','PT_UDP'):
                if params['source_port']:
                    data['traffic_match']['source_port'] = params['source_port']

                if params['destination_port']:
                    data['traffic_match']['destination_port'] = params['destination_port']

            if params['precedence']:
                data['traffic_match']['precedence'] = params['precedence']

            if params['tos']:
                data['traffic_match']['tos'] = params['tos']

            if params['is_log'] != None:
                data['is_log'] = params['is_log']

        else:

            if params['acl_source_address'] == 'host':
                source_mask = '255.255.255.255'
                source_ip = '0.0.0.0'
            else:
                source_ip = params['acl_source_address']
                source_mask = params['acl_source_mask']


            data.update({
                'std_source_address': {
                    'source_ip_address': {
                        'version': 'IAV_IP_V4',
                        'octets': source_ip,
                        },
                    'source_ip_mask': {
                        'version': 'IAV_IP_V4',
                        'octets': source_mask,
                        }
                    }
                })

        #Check idempotency for duplicate ip values
        if check_acl_rule_exists(module) == True:
            return {'msg':'ACL Rule entry already present','changed':False}

        # Without sequence_no configuration
        if params['sequence_no'] == 0:
            result = run_commands(module, url, data, 'POST')
            return result

        # With sequence_no configuration
        else:
            get_url = url + '/' + str(params['sequence_no'])
            acl_rule_config = get_config(module, get_url)
            if acl_rule_config:
                check_config = module.from_json(to_text(acl_rule_config))
                if params['sequence_no'] == check_config['sequence_no']:
                    result = run_commands(module, get_url, data, 'PUT', check=get_url)
                    return result
            else:
                data.update({ 'sequence_no': params['sequence_no']})
                result = run_commands(module, url, data, 'POST')
                return result

    else:
        if params['sequence_no'] == 0:
            return {'msg':'sequence_no is required','changed':False}

        url = url + '/' + str(params['sequence_no'])
        result = run_commands(module, url, {}, 'DELETE',check=url)

    return result


def run_module():
    module_args = dict(
        acl_name=dict(type='str', required=True),
        acl_type=dict(type='str', required=False,default='AT_STANDARD_IPV4',
            choices=['AT_EXTENDED_IPV4','AT_STANDARD_IPV4','AT_CONNECTION_RATE_FILTER']),
        state=dict(type='str', required=False, default='create',
            choices=['create','delete']),
        acl_action=dict(type='str', required=False, choices=['AA_DENY','AA_PERMIT']),
        remark=dict(type='str', required=False),
        acl_source_address=dict(type='str', required=False,default='0.0.0.0'),
        acl_source_mask=dict(type='str', required=False, default='255.255.255.255'),
        is_log=dict(type='bool', required=False),
        protocol_type=dict(type='str', required=False, choices=['PT_GRE','PT_ESP',
            'PT_AH','PT_OSPF','PT_PIM','PT_VRRP','PT_ICMP','PTIGMP','PT_IP','PT_SCTP',
            'PT_TCP','PT_UDP']),
        icmp_type=dict(type='int', required=False, default=-1),
        icmp_code=dict(type='int', required=False, default=-1),
        igmp_type=dict(type='str', required=False, choices=['IT_HOST_QUERY',
            'IT_HOST_REPORT','IT_DVMRP','IT_PIM','IT_TRACE','IT_V2_HOST_REPORT',
            'IT_V2_HOST_LEAVE','IT_MTRACE_REPLY','IT_MTRACE_REQUEST','IT_V3_HOST_REPORT',
            'IT_MROUTER_ADVERTISEMENT','IT_MROUTER_SOLICITATION','IT_MROUTER_TERMINATION']),
        is_connection_established=dict(type='bool', required=False),
        match_bit=dict(type='list', required=False, choices=['MB_ACK','MB_FIN',
            'MB_RST','MB_SYN']),
        source_port=dict(type='dict', required=False),
        destination_port=dict(type='dict', required=False),
        source_ip_address=dict(type='str', required=False),
        source_ip_mask=dict(type='str', required=False),
        destination_ip_address=dict(type='str', required=False),
        destination_ip_mask=dict(type='str', required=False),
        device_type=dict(type='str', required=False,),
        application_type=dict(type='str', required=False),
        precedence=dict(type='int', required=False, choices=[0,1,2,3,4,5,6,7]),
        tos=dict(type='int', required=False,choices=[0,2,4,8]),
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

        if module.params['acl_action']:
            result = acl_rule(module)
        else:
            result = acl(module)

    except Exception as err:
        return module.fail_json(msg=err)

    module.exit_json(**result)


def main():
    run_module()

if __name__ == '__main__':
    main()
