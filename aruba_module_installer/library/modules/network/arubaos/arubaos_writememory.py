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
module: arubaos_writememory
version_added: 2.9.6
extends_documentation_fragment: arubaos
short_description: Commits the pending configuration on the specified node
description:
    - Commits the pending configuration on the specified node.
    - The task is skipped if there is nothing to commit.
options:
    config_path:
        description:
            - Complete config-node or config-path from which the information should be retrieved.
            - On a managed device this will be restricted to /mm/mynode.
            - On a stand-alone controller, this will be restricted to /mm and /mm/mynode.
        required: false
        type: str
        default: None
'''

EXAMPLES = r'''
environment:
  ANSIBLE_ARUBAOS_HOST: 192.168.1.1
  ANSIBLE_ARUBAOS_USERNAME: admin
  ANSIBLE_ARUBAOS_PASSWORD: aruba123

tasks:

  - name: Commit pending configuration
    arubaos_writememory:
      config_path: /md/branch1/building1
'''

RETURNS = r'''
commited:
    description: Configuration data commited on this operation.
    returned: on success
    type: dict
pending:
    description: Configuration data still pending
    returned: on commit error
    type: dict
'''

import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native
from ansible.errors import AnsibleModuleError
from ansible.module_utils.network.arubaos.arubaos import ArubaOsApi, argspec_common, STATUS_SUCCESS, STATUS_SKIPPED


def run_module():
    argspec = argspec_common.copy()
    argspec.update(
        config_path=dict(required=False, type='str', default=None)
    )
    module = AnsibleModule(
        argument_spec=argspec,
        supports_check_mode=True
    )

    with ArubaOsApi(module) as api:

        if module.check_mode:
            pending_config = api.get_config(config_path=module.params.get('config_path'), config_type='pending')
            if pending_config:
                api.module_result.update(
                    changed=True,
                    msg='Configuration commited.',
                    commited=pending_config
                )
            else:
                api.module_result.update(
                    changed=False,
                    skipped=True,
                    msg='Nothing to commit.'
                )
            module.exit_json(**api.module_result)

        commit_status, commit_data = api.write_memory(config_path=module.params.get('config_path'))

        if commit_status == STATUS_SUCCESS:
            api.module_result.update(
                changed=True,
                msg='Configuration commited.',
                commited=commit_data
            )

        if commit_status == STATUS_SKIPPED:
            api.module_result.update(
                change=False,
                skipped=True,
                msg='Nothing to commit.'
            )

        module.exit_json(**api.module_result)


def main():
    run_module()


if __name__ == '__main__':
    main()
