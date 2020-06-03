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
module: arubaoss_captive_portal

short_description: Implements Ansible module for captive portal configuration.

version_added: "2.6"

description:
    - "This implement rest api's which can be used to configure captive portal
       on devices"

extends_documentation_fragment:
    - arubaoss_rest
    
options:
    profile_name:
        description:
            - captive portal profile name
        required: false
    server_url:
        description:
            - url for captive portal server
        required: false
    enable_captive_portal:
        description:
            - enable/disable captive portal on device
        required: false
    url_hash_key:
        description:
            - Hash key to verify integrity of the captive url
        required: false
    state:
        description:
            - Update or read captive protal data
        required: false


author:
    - Ashish Pant (@hpe)
'''

EXAMPLES = '''
      - name: enable/disable captive portal
        arubaoss_captive_portal:
          enable_captive_portal: "{{item}}"
        with_items:
          - False
          - True

      - name: add custom captive portal
        arubaoss_captive_portal:
          profile_name: "{{item}}"
          server_url: "http://hpe.com"
        with_items:
          - test1
          - test2

      - name: add/remove url_has
        arubaoss_captive_portal:
          url_hash_key: "{{item}}"
        with_items:
          - ""
          - test1

'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.arubaoss.arubaoss import run_commands,get_config
from ansible.module_utils.network.arubaoss.arubaoss import arubaoss_argument_spec, arubaoss_required_if
from ansible.module_utils._text import to_text


def config_captive_portal(module):

    params = module.params

    url = '/captive_portal'

    if params['state'] == 'create':
        data = {'is_captive_portal_enabled': params['enable_captive_portal']}

        if params.get('url_hash_key') != None:
            data['url_hash_key'] = params['url_hash_key']

        if params['profile_name']:
            data['custom_profile'] = {
                    'profile': params['profile_name'],
                    'url': params['server_url']
                    }

        result = run_commands(module, url,data, 'PUT', url)

    else:
        result = get_config(module, url)

    return result


def run_module():
    module_args = dict(
        profile_name=dict(type='str', required=False),
        server_url=dict(type='str', required=False, default=""),
        enable_captive_portal=dict(type='bool', required=False, default=True),
        url_hash_key=dict(type='str', required=False),
        state=dict(type='str', required=False, default='create'),
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

    else:
        try:
            result = config_captive_portal(module)
        except Exception as err:
            return module.fail_json(msg=err)

    module.exit_json(**result)


def main():
    run_module()

if __name__ == '__main__':
    main()
