#!/usr/bin/python
#
# Copyright (c) 2019-2020 Hewlett Packard Enterprise Development LP
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
module: arubaoss_dns

short_description: implements rest api for DNS configuration

version_added: "2.4"

description:
    - "This implements rest apis which can be used to configure DNS"

extends_documentation_fragment:
    - arubaoss_rest
    
options:
    dns_config_mode:
        description: DNS Configuration Mode, default is DCM_DHCP
        choices: DCM_DHCP, DCM_MANUAL, DCM_DISABLED
        required: False
    dns_domain_names:
        description: The first  manually configured DNS server domain name,
          all DNS configurations need to be made in a single module call,
          to remove configuration pass in empty string ""
        type: str
        required: False
    dns_domain_names_2:
        description: The second  manually configured DNS server domain name,
          all DNS configurations need to be made in a single module call,
          to remove configuration pass in empty string ""
        type: str
        required: False
    dns_domain_names_3:
        description: The third  manually configured DNS server domain name,
          all DNS configurations need to be made in a single module call,
          to remove configuration pass in empty string ""
        type: str
        required: False
    dns_domain_names_4:
        description: The fourth  manually configured DNS server domain name,
          all DNS configurations need to be made in a single module call,
          to remove configuration pass in empty string ""
        type: str
        required: False
    dns_domain_names_5:
        description: The fifth  manually configured DNS server domain name,
          all DNS configurations need to be made in a single module call,
          to remove configuration pass in empty string ""
        type: str
        required: False
    server_1:
        description: The first manually configured DNS Server IP address with priority 1,
          all DNS configurations need to be made in a single module call,
          to remove configuration pass in empty string ""
        type: str
        required: False
    version_1:
        description: The ip version of first manually configured DNS Server.
        choices: IAV_IP_V4. (V6 is not supported via REST)
        type: str
        required: False
    server_2:
        description: The second manually configured DNS Server IP address with priority 2,
          all DNS configurations need to be made in a single module call
        type: str
        required: False
    version_2:
        description: The ip version of second manually configured DNS Server.
        choices: IAV_IP_V4. (V6 is not supported via REST)
        type: str
        required: False
    server_3:
        description: The third manually configured DNS Server IP address with priority 3,
          all DNS configurations need to be made in a single module call,
          to remove configuration pass in empty string ""
        type: str
        required: False
    version_3:
        description: The ip version of third manually configured DNS Server.
        choices: IAV_IP_V4. (V6 is not supported via REST)
        type: str
        required: False
    server_4:
        description: The fourth manually configured DNS Server IP address with priority 4,
          all DNS configurations need to be made in a single module call,
          to remove configuration pass in empty string ""
        type: str
        required: False
    version_4:
        description: The ip version of fourth manually configured DNS Server.
        choices: IAV_IP_V4. (V6 is not supported via REST)
        type: str
        required: False

author:
    - Sanju Sadanandan (@hpe)
'''

EXAMPLES = '''
    - name: Configure Maximum DNS Domains and DNS Server
      arubaoss_dns:
        dns_domain_names: "mydomain.com"
        dns_domain_names_2: "myotherdomain.com"
        dns_domain_names_3: myotherotherdomain.com
        dns_domain_names_4: yourdomain.com
        dns_domain_names_5: otherdomain.com
        server_1: "10.2.3.4"
        server_2: "10.2.3.5"
        server_3: "10.2.3.6"
        server_4: "10.2.3.7"

    - name: Configure Remove all DNS Domains and DNS Server 3 and 4
      arubaoss_dns:
        server_1: "10.2.3.4"
        server_2: "10.2.3.5"
        server_3: ""
        server_4: ""

    - name: Configure DNS to be DHCP
      arubaoss_dns:
        dns_config_mode: "DCM_DHCP"

    - name: Disable DNS
      arubaoss_dns:
        dns_config_mode: "DCM_DISABLED"

    - name: Configure DNS Server with priority 4
      arubaoss_dns:
        dns_config_mode: "DCM_MANUAL"
        server_4: "10.2.3.4"

    - name: Configure DNS Server with priority 4 and priority 1
      arubaoss_dns:
        dns_config_mode: "DCM_MANUAL"
        server_1: "10.2.3.1"
        server_4: "10.2.3.4"
'''


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.arubaoss.arubaoss import run_commands
from ansible.module_utils.network.arubaoss.arubaoss import arubaoss_argument_spec, arubaoss_required_if

"""
-------
Name: config

Configures port with system_attributes config

param request: module

Returns
 Configure the switch with params sent
-------
"""
def config(module):

    params = module.params
    dnsList = []
    dnsServerList = []
    idval = 1
    data = {'dns_config_mode': params['dns_config_mode']}

    # Configure the domain names
    for dns in [params['dns_domain_names'], params['dns_domain_names_2'],
          params['dns_domain_names_3'], params['dns_domain_names_4'], params['dns_domain_names_5']]:
        if not dns == "" and dns not in dnsList:
            dnsList.append(dns)
    data['dns_domain_names'] = dnsList

    # Configure the dns servers
    for dnsServer in [params['server_1'], params['server_2'], params['server_3'], params['server_4']]:
        if not dnsServer == "" and dnsServer not in dnsServerList:
            dnsServerList.append(dnsServer)
            server = 'server_' + str(idval)
            version = 'version_' + str(idval)

            # Only IPv4 address supported
            if not params[version] == "IAV_IP_V4":
                return {'msg': 'Only IPv4 address mode is supported',
                    'changed': False, 'failed': False}

            data[server] =  {'version': params[version], 'octets': params[server]}
        idval = idval + 1

    url = '/dns'
    method = 'PUT'

    result = run_commands(module, url, data, method, check=url)
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
        dns_config_mode=dict(type='str', required=False,default="DCM_MANUAL",
              choices=["DCM_DHCP", "DCM_MANUAL", "DCM_DISABLED"]),
        dns_domain_names=dict(type='str', required=False, default=""),
        dns_domain_names_2=dict(type='str', required=False, default=""),
        dns_domain_names_3=dict(type='str', required=False, default=""),
        dns_domain_names_4=dict(type='str', required=False, default=""),
        dns_domain_names_5=dict(type='str', required=False, default=""),
        server_1=dict(type='str', required=False, default=""),
        version_1=dict(type='str', required=False, default="IAV_IP_V4", choices=["IAV_IP_V4"]),
        server_2=dict(type='str', required=False, default=""),
        version_2=dict(type='str', required=False, default="IAV_IP_V4", choices=["IAV_IP_V4"]),
        server_3=dict(type='str', required=False, default=""),
        version_3=dict(type='str', required=False, default="IAV_IP_V4", choices=["IAV_IP_V4"]),
        server_4=dict(type='str', required=False, default=""),
        version_4=dict(type='str', required=False, default="IAV_IP_V4", choices=["IAV_IP_V4"]),
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
        result = config(module)
    except Exception as err:
        return module.fail_json(msg=err)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
