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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['deprecated'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
author: Sacha Boudjema (@sachaboudjema)
module: arubaos_controller_config
version_added: 2.9.6
deprecated: true
extends_documentation_fragment: arubaos
short_description: Configure ArubaOS products like Mobility Master and Mobility Controllers using AOS APIs
description:
    -Configure ArubaOS products like Mobility Master and Mobility Controllers using AOS APIs.
notes:
    - Kept for backward compatibility. Prefer use of C(arubaos_*) modules instead.
    - Check mode supported but systematically skipped.
options:
    method:
        description:
            - HTTP Method to be used for the API call.
        required: true
        type: str
        choices:
            - GET
            - POST
    api_name:
        description:
            - ARUBA MM Rest API Object Name.
        required: true
        type: str
    config_path:
        description:
            - Path in configuration hierarchy to the node the API call is applied to.
        required: false
        type: str
        default: None
    data:
       type: str description:
            - Dictionary data for the API call.
        required: false
        type: str
        default: None
'''

EXAMPLES = r'''
- name: Create a ssid profile with opmode by providing host and credentials.
    arubaos_controller_config:
    host: 192.168.1.1
    username: admin
    password: aruba123
    method: POST
    api_name: ssid_prof
    config_path: /md/branch1/building1
    data: { "profile-name": "test_ssid_profile", "essid" :{"essid":"test_employee_ssid"}, "opmode": {"name": "wpa-aes"}}
    validate_cert: True

- name: Configure a server group profile and add an existing radius server to it
    arubaos_controller_config:
    host: 192.168.1.1
    username: admin
    password: admin123
    method: POST
    api_name: server_group_prof
    config_path: /md/branch1/building1
    data: {"sg_name":"test", "auth_server": {"name": "test_rad_server"}}
'''

RETURN = r'''
status_code:
    description: HTTP status code of the response.
    returned: on success
    type: int
response:
    description: '_data' component of the reponse returned by GET requests.
    returned: on GET success
    type: dict
reason:
    description: Reason of module failure.
    returned: on failure
    type: str
api_call:
    description: Parameters of the request sent to the API.
    returned: on failure
    type: dict
'''

import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native
from ansible.errors import AnsibleModuleError
from ansible.module_utils.network.arubaos.arubaos import ArubaOsApi, argspec_common


def run_module():
    argspec = argspec_common.copy()
    argspec.update(
        api_name=dict(required=True, type='str'),
        method=dict(required=True, type='str', choices=['GET', 'POST']),
        config_path=dict(required=False, type='str', default=None),
        data=dict(required=False, type='dict', default=None)
    )
    module = AnsibleModule(
        argument_spec=argspec,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(
            changed=False,
            skipped=True,
            msg='Check mode is not implemented.'
        )

    method = module.params.get('method')
    path = '/configuration/object/{}'.format(module.params.get('api_name'))
    data = module.params.get('data')
    params = {'config_path': module.params.get('config_path')}
    if data is not None:
        if method == 'GET':
            params.update(data)
            data = None
        if method == 'POST':
            data = json.dumps(data)

    api_call = {
        'host': module.params.get('host'),
        'username': module.params.get('username'),
        'password': module.params.get('password'),
        'api_name': module.params.get('api_name'),
        'method': module.params.get('method'),
        'config_path': module.params.get('config_path'),
        'data': module.params.get('data')
    }

    with ArubaOsApi(module) as api:

        url = api.get_url(path, params=params)
        api_call.update(url=url)
        response, response_json = api.send_request(url, method, data=data)

    try:
        if method == 'GET':
            result = response_json['_data']
            module.exit_json(
                changed=False,
                msg=result,
                status_code=response.getcode(),
                response=response_json
            )
        if method == 'POST':
            result = response_json['_global_result']
            if result['status'] == 0:
                module.exit_json(
                    changed=True,
                    msg=result['status_str'],
                    status_code=response.getcode()
                )
            if result['status'] in [1, 2]:
                module.exit_json(
                    skipped=True,
                    msg=str(result['status_str']),
                    status_code=response.getcode()
                )
        module.fail_json(
            changed=False,
            msg="API Call failed!",
            reason=result['status_str'],
            api_call=api_call
        )
    except Exception as exc:
        module.fail_json(
            changed=False,
            msg='Exception while processing response.',
            exception=to_native(exc)
        )


def main():
    run_module()


if __name__ == '__main__':
    main()
