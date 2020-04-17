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
module: arubaos_set
version_added: 2.9.6
extends_documentation_fragment: arubaos
short_description: Add, modify or delete the configuration
description:
    - Add, modify or delete the configuration
notes:
    - Supports C(--diff).
    - Check-mode is not supported on nodes with pending configuration.
options:
    config_path:
        description:
            - Complete config-node or config-path to which the operation should be applied.
            - On a managed device this will be restricted to /mm/mynode.
            - On a stand-alone controller, this will be restricted to /mm and /mm/mynode.
        required: false
        type: str
        default: None
    data:
        description:
            - One or more objects which needs to be set. Each object type is a keyn of the top level dict.
            - The SET request is best effort and in case of first failure, others in the same block are not even tried.
            - Each object can contain either a single instance (dict) or a list of instances (list of dicts).
            - Every object and sub-object can optionally contain an C(_action) field which describes the action napplied to the configuration.
            - If C(_action) field is not set it implies that the user wants to add/modify the configuration.
            - Toggle objects are set using the C(_present) field, which takes a bool value.
            - Mutually exclusive with C(multipart_data).
        required: false
        type: dict
        default: {}
    multipart_data:
        description:
            - List of configuration data sets to be treated as independent requests.
            - Each item follows the same formating rules as for the C(data) option.
            - In contrary to C(data) option, even if one item (i.e. request) in the list contains errors, the other items will still continue to be processed.
            - Mutually exclusive with C(data).
        required: false
        type: list
        elements: dict
        default: []
    commit:
        description:
            - If set to true, configuration changes will be commited (write memory) on the specified C(config_path).
            - Task will be skipped if any changes are pending prior to the operation.
            - Changes will not be commited if any configuration blocks in the set operation contain errors.
            - Changes will still be staged if commit is skipped due to block errors.
            - Mutually exclusive with C(commit_force) option.
        required: false
        type: bool
        default: false
    commit_force:
        description:
            - If set to true, any changes to the configuration will be commited (write memory) to the specified C(config_path).
            - Task will be skipped if any changes are pending prior to the operation.
            - Commmit will happen even if some configuration blocks in the set operation contain errors.
            - Mutually exclusive with C(commit) option.
        required: false
        type: bool
        default: false
'''

EXAMPLES = r'''
environment:
  ANSIBLE_ARUBAOS_HOST: 192.168.1.1
  ANSIBLE_ARUBAOS_USERNAME: admin
  ANSIBLE_ARUBAOS_PASSWORD: aruba123

tasks:

  - name: Create single instance of single object
    arubaos_set:
      config_path: /md/branch1/building1
      data:
        aaa_prof:
          profile-name: aaa_prof-guest
          mba_server_group:
            srv-group: srv_group-guest

  - name: Create multiple instances of single object
    arubaos_set:
      config_path: /md/branch1/building1
      data:
        aaa_prof:
          - profile-name: aaa_prof-guest
              mba_server_group:
                srv-group: srv_group-guest
          - profile-name: aaa_prof-employee
              dot1x_server_group:
                srv-group: srv_group-guest

  - name: Set & commit (do not of errors)
    arubaos_set:
      config_path: /md/branch1/building1
      data:
        aaa_prof:
          - profile-name: aaa_prof-guest
          - profile-name: aaa_prof-employee
      commit: true

  - name: Create inctances of multiple object types
    arubaos_set:
      config_path: /md/branch1/building1
      data:
        server_group_prof:
          - sg_name: srv_group-guest
          - sg_name: srv_group-employee
        aaa_prof:
          - profile-name: aaa_prof-guest
            mba_server_group:
              srv-group: srv_group-guest
          - profile-name: aaa_prof-employee
            dot1x_server_group:
              srv-group: srv_group-employee

  - name: Multi-part set & commit (commit even if a block fails)
    arubaos_set:
      config_path: /md/branch1/building1
      multipart_data:
        - server_group_prof:
            - sg_name: srv_group-guest
          aaa_prof:
            - profile-name: aaa_prof-guest
              mba_server_group:
                srv-group: srv_group-guest
        - server_group_prof:
            - sg_name: srv_group-employee
          aaa_prof:
            - profile-name: aaa_prof-employee
              dot1x_server_group:
                srv-group: srv_group-employee
      commit_force: true
'''

RETURNS = r'''
response:
    description: Returned payload with additional "_result" fields for each object "_global_result".
    returned: always
    type: dict
pending:
    description: Pending configuraiton of the target node
    returned: on check mode error
    type: dict
'''

import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native
from ansible.module_utils.network.arubaos.arubaos import ArubaOsApi, argspec_common, global_result, STATUS_SUCCESS


def format_json_payload(module):
    data = dict()
    if module.params.get('data'):
        data = module.params.get('data')
    if module.params.get('multipart_data'):
        data = {'_list': module.params.get('multipart_data')}
    return json.dumps(data, separators=(',', ':'))


def commit_requested(module):
    commit = module.params.get('commit')
    commit_force = module.params.get('commit_force')
    commit_requested = commit or commit_force
    return commit_requested


def check_pending_required(module):
    check_pending_required = commit_requested(module) or module.check_mode
    return check_pending_required


def check_pending_config(api, module):
    config_path = module.params.get('config_path')
    check_mode = module.check_mode
    pending_config = api.get_config(config_path=config_path, config_type='pending')

    if pending_config:
        if check_mode:
            api.module_result.update(
                msg='Check mode is not supported on nodes with pending changes. Save or purge then try again.'
            )
        if commit_requested:
            api.module_result.update(
                msg='Commit options are not supported on nodes with pending changes. Save or purge then try again.'
            )
        api.module_result.update(
            skipped=True,
            pending=pending_config
        )
        module.exit_json(**api.module_result)


def commit_config(api, module, errors=False):
    config_path = module.params.get('config_path')
    commit = module.params.get('commit')

    if commit and errors:
        api.module_result.setdefault('warnings', []).append(
            'Pending changes were not commited because one or more blocks returned errors.'
        )
        return api.module_result

    commit_status, commit_data = api.write_memory(config_path=config_path)
    return commit_status, commit_data


def set_operation(api, module):
    config_path = module.params.get('config_path')
    json_payload = format_json_payload(module)

    before = api.get_config(config_path=config_path)

    url = api.get_url('/configuration/object', params={'config_path': config_path})
    _, response_json = api.send_request(url, 'POST', data=json_payload)

    after = api.get_config(config_path=config_path)

    changed = (before != after)
    diff = dict(before=before, after=after)

    return response_json, changed, diff


def run_module():
    argspec = argspec_common.copy()
    argspec.update(
        data=dict(required=False, type='dict', default=dict()),
        multipart_data=dict(required=False, type='list', elements='dict', default=list()),
        config_path=dict(required=False, type='str', default=None),
        commit=dict(required=False, type='bool', default=False),
        commit_force=dict(required=False, type='bool', default=False)
    )

    module = AnsibleModule(
        argument_spec=argspec,
        supports_check_mode=True,
        mutually_exclusive=[
            ['commit', 'commit_force'],
            ['data', 'multipart_data']
        ]
    )

    with ArubaOsApi(module) as api:

        if check_pending_required(module):
            check_pending_config(api, module)

        response_json, changed, diff = set_operation(api, module)

        global_status, global_status_str, _ = global_result(response_json)

        errors = (global_status != STATUS_SUCCESS)

        api.module_result.update(
            changed=changed,
            msg=global_status_str,
            response=response_json,
            diff=diff
        )

        if errors:
            api.module_result.setdefault('warnings', []).append(
                'One or more config blocks returned with errors.'
            )

        if changed and module.check_mode:
            api.purge_pending(module.params.get('config_path'))

        if changed and commit_requested(module):
            commit_status, _ = commit_config(api, module, errors=errors)
            # For the sake of not confusing the end user, we alter the original _pending status if commit was successful
            if commit_status == STATUS_SUCCESS:
                response_json['_global_result']['_pending'] = False

        module.exit_json(**api.module_result)


def main():
    run_module()


if __name__ == '__main__':
    main()
