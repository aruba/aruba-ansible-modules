#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Sacha Boudjema <sachaboudjema@gmail.com>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
author: Sacha Boudjema (@sachaboudjema)
module: arubaos_config
version_added: 2.9.6
extends_documentation_fragment: arubaos
short_description: Queries full or partial configuration of a particular configuration node
description:
    - Queries full or partial configuration of a particular configuration node.
options:
    config_path:
        description:
            - The hierarchy (complete config-node or config-path) from which the information should be retrieved.
            - On a managed device this will be restricted to /mm/mynode.
            - On a stand-alone controller, this will be restricted to /mm and /mm/mynode.
        required: false
        type: str
        default: None
    type:
        description:
            - State of configuration blocks to be retrieved.
            - If the user deletes any configuration which is pending, it is not returned in this API call.
            - Only added or modified configurations are retrieved. To get deleted configuration, use the 'show configuration pending' command.
        required: false
        type: str
        default: None
        choices:
            - pending
            - committed
            - local
            - committed,local
'''

EXAMPLES = r'''
environment:
  ANSIBLE_ARUBAOS_HOST: 192.168.1.1
  ANSIBLE_ARUBAOS_USERNAME: admin
  ANSIBLE_ARUBAOS_PASSWORD: aruba123

tasks:

  - name: Get local configuration of branch1
    arubaos_config:
      config_path: /md/branch1
      type: local
'''

RETURN = r'''
response:
    description: Effective configuration of the specified node.
    returned: always
    type: dict
'''

import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native
from ansible.module_utils.network.arubaos.arubaos import ArubaOsApi, argspec_common, CHOICES_CONFIG_TYPE


def run_module():
    argspec = argspec_common.copy()
    argspec.update(
        config_path=dict(required=False, type='str', default=None),
        type=dict(required=False, type='str', choices=CHOICES_CONFIG_TYPE, default=None)
    )

    module = AnsibleModule(
        argument_spec=argspec,
        supports_check_mode=True
    )

    with ArubaOsApi(module) as api:

        response_json = api.get_config(
            config_path=module.params.get('config_path'),
            config_type=module.params.get('type')
        )

        module.exit_json(
            changed=False,
            msg='Success',
            response=response_json
        )


def main():
    run_module()


if __name__ == '__main__':
    main()
