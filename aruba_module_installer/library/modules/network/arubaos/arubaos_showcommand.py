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
module: arubaos_showcommand
version_added: 2.9.6
extends_documentation_fragment: arubaos
short_description: Executes a C(show) command on the controller and returns structured data when supported
description:
    - Executes a C(show) command on the controller and returns structured data when supported.
options:
    command:
        description:
            - Any show command supported by the controller.
            - The command is executed on the target controller node (i.e. mynode).
            - Invalid commands return empty data.
        required: true
        type: str
'''

EXAMPLES = r'''
environment:
  ANSIBLE_ARUBAOS_HOST: 192.168.1.1
  ANSIBLE_ARUBAOS_USERNAME: admin
  ANSIBLE_ARUBAOS_PASSWORD: aruba123

tasks:

  - name: Get list of managed devices
    arubaos_showcommand:
      command: show switches
'''

RETURNS = r'''
response:
    description: Data set returned by the GET request.
    returned: on success
    type: dict
'''

import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native
from ansible.module_utils.network.arubaos.arubaos import ArubaOsApi, argspec_common


def run_module():
    argspec = argspec_common.copy()
    argspec.update(
        command=dict(required=True, type='str')
    )

    module = AnsibleModule(
        argument_spec=argspec,
        supports_check_mode=True
    )

    with ArubaOsApi(module) as api:

        url = api.get_url(
            '/configuration/showcommand',
            params={'command': module.params.get('command')}
        )
        _, response_json = api.send_request(url, 'GET')

        module.exit_json(
            changed=False,
            msg='Success',
            response=response_json
        )


def main():
    run_module()


if __name__ == '__main__':
    main()
