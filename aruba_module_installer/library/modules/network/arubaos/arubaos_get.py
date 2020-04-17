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
module: arubaos_get
version_added: 2.9.6
extends_documentation_fragment: arubaos
short_description: Executes GET operations on API objects
description:
    - Executes GET operations on API objects.
options:
    object:
        description:
            - Name of the object type which needs to be queried.
        type: str
        required: true
    config_path:
        description:
            - Complete config-node or config-path from which the information should be retrieved.
            - On a managed device this will be restricted to /mm/mynode.
            - On a stand-alone controller, this will be restricted to /mm and /mm/mynode.
        required: false
        type: str
        default: None
    sort:
        description:
            - Sorts the returned object based on specified paramter and order
            - There can only be one sort filter per request.
            - Single string of th form <operator><parama_name>.
            - Operator can be C(+) for ascending or C(-) for descending.
            - Param name is a fully qualified attribute name.
        type: str
        required: false
    offset:
        description:
            - Conveys the index (1 based) from which the returned data set should start.
            - Must be a multiple of I(limit) plus one. In other words, offset % limit = 1.
            - Required together with I(limit).
        type: int
        required: false
        default: None
    limit:
        description:
            - Maximum number of objects returned.
            - Required together with I(offset).
        type: int
        required: false
        default: None
    total:
        description:
            - Expected total count of objects before any pagination applied by I(limit) and I(offset).
            - If the actual total doesnt match this value, returned data set will contain a dirty flag.
            - Can be used to check if objects were created or delted between two paginated requests.
        type: int
        required: false
        default: None
    count:
        description:
            - Requests the API to include a count of specified objects or parameters along with the object data.
            - Elements should be fully qualified names of objects or attributes.
        type: list
        elemets: str
        required: false
        default: []
    data_types:
        description:
            - Filters returned objects based on configuration state.
            - Only applies to top level objects in the query.
            - Mutually exclusive with I(object_filters) and I(data_filters).
        type: list
        required: false
        default: []
        choices: [non-default, default, local, user, system, pending, committed, inherited, meta-n-data, meta-only]
    object_filters:
        description:
            - Filters returned objects based on object type.
            - Mutually exclusive with I(data_types).
        type: list
        elements: dict
        required: false
        default: []
        suboptions:
            oper:
                description:
                    - Operation to be applied on the filter values.
                required: true
                type: str
                choices: [$eq, $neq]
            values:
                description:
                    -  List of fully qualified object names to be matched by the filter.
                required: true
                type: list
                elements: str
    data_filters:
        description:
            - Filters returned objects based on object attributes.
            - Mutually exclusive with I(data_types).
        type: list
        elements: dict
        required: false
        default: []
        suboptions:
            param_name:
                description:
                    - Fully qualified name of the parameter to be looked up by the filter.
                required: true
                type: str
            oper:
                description:
                    - Operation to be applied on the filter values.
                required: true
                type: str
                choices: [$eq, $neq, $gt', $gte, $lt, $lte, $in, $nin]
            values:
                description:
                    -  List of values to be matched by the filter.
                required: true
                type: list
                elements: str
'''

EXAMPLES = r'''
environment:
  ANSIBLE_ARUBAOS_HOST: 192.168.1.1
  ANSIBLE_ARUBAOS_USERNAME: admin
  ANSIBLE_ARUBAOS_PASSWORD: aruba123

tasks:

  - name: Get AAA profiles
    arubaos_get:
      object: aaa_prof
      config_path: /md/branch1/building1

  - name: Get AAA profiles configured locally and in a commited state
    arubaos_get:
      object: aaa_prof
      config_path: /md/branch1/building1
      data_types: [local, commited]

  - name: Get AAA profiles, but only return server_group sub-objects
    arubaos_get:
      object: aaa_prof
      config_path: /md/branch1/building1
      object_filters:
        - oper: $eq
          values: [aaa_prof.server_group]

  - name: Get AAA profiles with profile-name containing 'corp' or 'guest'
    arubaos_get:
      object: aaa_prof
      config_path: /md/branch1/building1
      data_filters:
        - parama_name: aaa_prof.profile-name
          oper: $in
          values: [corp, guest]

  - name: Get the the number of server groups configured on aaa profile named 'guest'
    arubaos_get:
      object: aaa_prof
      config_path: /md/branch1/building1
      data_filters:
        - parama_name: aaa_prof.profile-name
          oper: $eq
          values: [guest]
      count: [aaa_prof.server_group]

  - name: Get the first 10 AAA profiles sorted by profile name
    arubaos_get:
      object: aaa_prof
      config_path: /md/branch1/building1
      limit: 10
      offset: 1
      sort: +aaa_prof.profile-name
'''

RETURN = r'''
response:
    description: Data set returned by the GET request.
    returned: on success
'''

import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native
from ansible.module_utils.network.arubaos.arubaos import ArubaOsApi, argspec_common, CHOICES_OBJECT_OPER, CHOICES_DATA_OPER, CHOICES_DATA_TYPE


def filter_param(object_filters, data_filters):
    filters = []
    for f in object_filters:
        filters.append({'OBJECT': {f['oper']: f['values']}})
    for f in data_filters:
        filters.append({f['param_name']: {f['oper']: f['values']}})
    if filters:
        return json.dumps(filters, separators=(',', ':'))
    return None


def url_params(module):
    params = dict(
        config_path=module.params.get('config_path'),
        sort=module.params.get('sort'),
        limit=module.params.get('limit'),
        offset=module.params.get('offset'),
        total=module.params.get('total')
    )

    if module.params.get('count'):
        count_string = ','.join(module.params.get('count'))
        params.update(count=count_string)

    if module.params.get('data_types'):
        type_string = ','.join(module.params.get('data_types'))
        params.update(type=type_string)

    filter_string = filter_param(
        module.params.get('object_filters'),
        module.params.get('data_filters')
    )
    if filter_string:
        params.update(filter=filter_string)

    return params


def run_module():
    argspec = argspec_common.copy()
    argspec.update(
        object=dict(required=True, type='str'),
        config_path=dict(required=False, type='str', default=None),
        sort=dict(required=False, type='str', default=None),
        offset=dict(required=False, type='int', default=None),
        limit=dict(required=False, type='int', default=None),
        total=dict(required=False, type='int', default=None),
        count=dict(required=False, type='list', default=list(), elements='str'),
        data_types=dict(required=False, type='list', default=list(), elements='str', choices=CHOICES_DATA_TYPE),
        object_filters=dict(required=False, type='list', default=list(), elements='dict', options=dict(
            oper=dict(required=True, type='str', choices=CHOICES_OBJECT_OPER),
            values=dict(required=True, type='list', elements='str')
        )),
        data_filters=dict(required=False, type='list', default=list(), elements='dict', options=dict(
            param_name=dict(required=True, type='str'),
            oper=dict(required=True, type='str', choices=CHOICES_DATA_OPER),
            values=dict(required=True, type='list', element='str')
        ))
    )

    module = AnsibleModule(
        argument_spec=argspec,
        supports_check_mode=True,
        required_together=[['offset', 'limit']],
        mutually_exclusive=[['data_types', 'object_filters'], ['data_types', 'data_filters']]
    )

    path = '/configuration/object/{}'.format(module.params.get('object'))

    with ArubaOsApi(module) as api:

        url = api.get_url(path, params=url_params(module))
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
