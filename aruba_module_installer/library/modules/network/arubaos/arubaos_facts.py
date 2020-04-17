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
---
author: Sacha Boudjema (@sachaboudjema)
module: arubaos_facts
version_added: 2.9.6
extends_documentation_fragment: arubaos
short_description: Populates ansible_facts with C(sys_info) details about the system to which the query is being sent
desciription:
    - Populates ansible_facts with C(sys_info) details about the system to which the query is being sent.
    - For a full list of retrieved facts, see API documentation.
options: {}
'''

EXAMPLES = r'''
environment:
  ANSIBLE_ARUBAOS_HOST: 192.168.1.1
  ANSIBLE_ARUBAOS_USERNAME: admin
  ANSIBLE_ARUBAOS_PASSWORD: aruba123

tasks:

  - name: Gather controller system facts
    arubaos_facts:
'''

RETURN = r'''
ansible_facts:
    description: Facts to be merged to the current play context.
    type: dict
    contains:
        arubaos:
            description: Details about the system to which the query is being sent.
            type: dict
'''

import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native
from ansible.module_utils.network.arubaos.arubaos import ArubaOsApi, argspec_common


def run_module():
    argspec = argspec_common.copy()

    module = AnsibleModule(
        argument_spec=argspec,
        supports_check_mode=True
    )

    with ArubaOsApi(module) as api:

        _, response_json = api.send_request(api.get_url('/configuration/object/sys_info'), 'GET')

        module.exit_json(
            changed=False,
            ansible_facts={'arubaos': response_json}
        )


def main():
    run_module()

if __name__ == '__main__':
    main()
