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


import json
from io import BytesIO
from contextlib import contextmanager
from ansible.module_utils.basic import env_fallback
from ansible.module_utils._text import to_native
from ansible.module_utils.urls import open_url
from ansible.module_utils.six.moves.urllib.error import HTTPError
from ansible.module_utils.six.moves.urllib.parse import urlencode, urlparse, urlunparse, parse_qs
from ansible.errors import AnsibleError, AnsibleAuthenticationFailure

VERSION = 1
HTTP_AGENT = 'ansible-httpget'
FOLLOW_REDIRECTS = 'urllib2'
DEFAULT_HEADERS = {
    'GET': {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    'POST': {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
}

CHOICES_OBJECT_OPER = ['$eq', '$neq']
CHOICES_DATA_OPER = ['$eq', '$neq', '$gt', '$gte', '$lt', '$lte', '$in', '$nin']
CHOICES_DATA_TYPE = ['non-default', 'default', 'local', 'user', 'system', 'pending', 'committed', 'inherited', 'meta-n-data', 'meta-only']
CHOICES_CONFIG_TYPE = ['pending', 'committed', 'local', 'committed,local']

STATUS_SUCCESS = 0
STATUS_FAILED = 1
STATUS_SKIPPED = 2

argspec_common = dict(
    host=dict(required=True, type='str', fallback=(env_fallback, ['ANSIBLE_ARUBAOS_HOST'])),
    username=dict(required=True, type='str', fallback=(env_fallback, ['ANSIBLE_ARUBAOS_USERNAME'])),
    password=dict(required=True, type='str', no_log=True, fallback=(env_fallback, ['ANSIBLE_ARUBAOS_PASSWORD'])),
    validate_certs=dict(required=False, type="bool", default=False),
    client_cert=dict(required=False, type="str", default=None),
    client_key=dict(required=False, type="str", default=None)
)


def update_url_query(url, **kwargs):
    parse_result = urlparse(url)
    query = parse_qs(parse_result.query)
    query.update({k: v for k, v in kwargs.items() if v is not None})
    query_string = urlencode(query, doseq=True)
    parse_result = parse_result._replace(query=query_string)
    return urlunparse(parse_result)


def global_result(response_json):
    result = response_json['_global_result']
    return result['status'], result['status_str'], result['_pending']


class ArubaOsApi:

    def __init__(self, module, module_result=dict(changed=False)):
        self.module_result = module_result.copy()
        self._module = module
        self._credentials = {
            'username': module.params.get('username'),
            'password': module.params.get('password')
        }
        self._uidaruba = None

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.logout()
        if exc_type:
            self.module_result.update(
                msg='{} encountered while requesting API: {}'.format(exc_type, exc_value),
                exception=exc_value
            )
            self._module.fail_json(**self.module_result)

    @property
    def authenticated(self):
        if self._uidaruba is not None:
            return True
        return False

    @property
    def host(self):
        return self._module.params.get('host')

    @property
    def validate_certs(self):
        return self._module.params.get('validate_certs')

    @property
    def client_cert(self):
        return self._module.params.get('client_cert')

    @property
    def client_key(self):
        return self._module.params.get('client_key')

    @property
    def root_url(self):
        return 'https://{}:4343/v{}'.format(self.host, VERSION)

    @property
    def login_url(self):
        return '{}/api/login'.format(self.root_url)

    @property
    def logout_url(self):
        return '{}/api/logout'.format(self.root_url)

    def get_url(self, path, params=None):
        url = '{}{}'.format(self.root_url, path)
        if params:
            url = update_url_query(url, **params)
        return url

    def send_request(self, url, method, data=None, headers=None):
        if headers is None:
            headers = DEFAULT_HEADERS[method]
        if self.authenticated:
            url = update_url_query(url, UIDARUBA=self._uidaruba)
            headers.update({'Cookie': 'SESSION={}'.format(self._uidaruba)})
        try:
            response = open_url(
                url, method=method, headers=headers, data=data,
                client_cert=self.client_cert,
                client_key=self.client_key,
                validate_certs=self.validate_certs,
                follow_redirects=FOLLOW_REDIRECTS,
                http_agent=HTTP_AGENT
            )
        except HTTPError as exc:
            response = self.handle_httperror(exc)
        except Exception as exc:
            raise AnsibleError('Exception while sending request: {}'.format(to_native(exc)))

        response_buffer = BytesIO()
        response_buffer.write(response.read())
        response_buffer.seek(0)

        return self.handle_response(response, response_buffer)

    def handle_httperror(self, exc):
        handled = False
        if exc.getcode() == 404:
            handled = True
        if handled:
            return exc
        raise AnsibleError('Request returned HTTP error {} {}'.format(exc.getcode(), exc.getinfo()))

    def handle_response(self, response, response_data):
        data = response_data.read()
        try:
            repsonse_json = json.loads(data)
        except ValueError:
            raise AnsibleError('Failed to parse JSON from response: {}'.format(data))
        return response, repsonse_json

    def login(self):
        _, repsonse_json = self.send_request(
            self.login_url, 'POST',
            data=urlencode(self._credentials),
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        try:
            self._uidaruba = repsonse_json['_global_result']['UIDARUBA']
        except KeyError:
            raise AnsibleAuthenticationFailure('Failed to acquire UIDARUBA token from login response.')

    def logout(self):
        self.send_request(self.logout_url, 'GET')
        self._uidaruba = None

    def get_config(self, config_path=None, config_type=None):
        _, repsonse_json = self.send_request(
            self.get_url(
                '/configuration/object/config',
                params={
                    'config_path': config_path,
                    'type': config_type
                }
            ),
            'GET',
        )
        return repsonse_json

    def purge_pending(self, config_path):
        """
        Purge the pending configuration on the specified config path

        Returns
        -------
        purge_status: int
            Status code similar in meaning to ArubaOS _global_result
            0: Success, configuration was purged
            1: Failed, there was an error while purging
            2: Skipped, there was no configuration to purge
        purge_data:
            Data to be passed along with the status code
            On success, returns the data purged
            On error, returns the response status string

        Raises
        ------
        ArubaOsApiError
            If the response returns any status code other than 0 (success)
        """
        pending = self.get_config(config_path=config_path, config_type='pending')

        if not pending:
            return STATUS_SKIPPED, pending

        _, response_json = self.send_request(
            self.get_url(
                '/configuration/object/configuration_purge_pending', 
                params={'config_path': config_path}
            ),
            'POST',
            data={}
        )
        status, status_str, _ = global_result(response_json)

        if status != STATUS_SUCCESS:
            raise ArubaOsApiError(status_str, pending)

        return STATUS_SUCCESS, pending

    def write_memory(self, config_path=None):
        """
        Commits the pending configuration on the specified config path

        Returns
        -------
        commit_status: int
            Status code similar in meaning to ArubaOS _global_result
            0: Success, configuration was commited
            1: Failed, there was an error while commiting
            2: Skipped, there was no configuration to commit
        commit_data:
            Data to be passed along with the status code
            On success, returns the data commited
            On error, returns the response status string

        Raises
        ------
        ArubaOsApiError
            If the response returns any status code other than 0 (success)
        """
        pending = self.get_config(config_path=config_path, config_type='pending')

        if not pending:
            return STATUS_SKIPPED, pending

        url = self.get_url('/configuration/object/write_memory', params={'config_path': config_path})
        _, response_json = self.send_request(url, 'POST', data='{}')
        status, status_str, _ = global_result(response_json)

        if status != STATUS_SUCCESS:
            raise ArubaOsApiError(status_str, pending)

        return STATUS_SUCCESS, pending


class ArubaOsApiError(Exception):
    def __init__(self, message, data):
        super(ArubaOsApiError, self).__init__(message)
        self.data = data
