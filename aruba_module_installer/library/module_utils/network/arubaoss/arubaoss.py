# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# (c) 2018 Red Hat Inc.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import re

from ansible.module_utils._text import to_text
from ansible.module_utils.basic import env_fallback
from ansible.module_utils.network.common.utils import to_list, ComplexList
from ansible.module_utils.connection import exec_command
from ansible.module_utils.six import iteritems
from ansible.module_utils.urls import fetch_url
from time import sleep
import json

_DEVICE_CONNECTION = None

arubaoss_provider_spec = {
    'host': dict(),
    'port': dict(type='int'),
    'username': dict(fallback=(env_fallback, ['ANSIBLE_NET_USERNAME'])),
    'password': dict(fallback=(env_fallback, ['ANSIBLE_NET_PASSWORD']), no_log=True),
    'ssh_keyfile': dict(fallback=(env_fallback, ['ANSIBLE_NET_SSH_KEYFILE']), type='path'),
    'use_ssl': dict(type='bool'),
    'use_proxy': dict(default=False, type='bool'),
    'validate_certs': dict(default=False, type='bool'),
    'transport': dict(default='aossapi'),
    'timeout': dict(type='int'),
    'validate_certs': dict(type='bool',default=False),
    'api_version': dict(type='str',default='None'),
}
arubaoss_argument_spec = {
    'provider': dict(type='dict', options=arubaoss_provider_spec)
}

arubaoss_top_spec = {
    'host': dict(removed_in_version=2.9),
    'port': dict(removed_in_version=2.9, type='int'),
    'username': dict(removed_in_version=2.9),
    'password': dict(removed_in_version=2.9, no_log=True),
    'ssh_keyfile': dict(removed_in_version=2.9, type='path'),
    'timeout': dict(removed_in_version=2.9, type='int'),
    'use_ssl': dict(type='bool'),
    'validate_certs': dict(type='bool',default=False),
    'api_version': dict(type='str',default='None'),
}

arubaoss_argument_spec.update(arubaoss_top_spec)


def get_provider_argspec():
    return arubaoss_provider_spec


def check_args(module, warnings):
    pass


def get_version(module):
    host = module.params['host']
    port = module.params['port']
    if module.params['use_ssl']:
        proto = 'https'
        port = port or 443
    else:
        proto = 'http'
        port = port or 80
    check_url = "{}://{}:{}/rest".format(proto,host,port)
    uri = '/version'
    headers = {'Content-Type': 'application/json'}
    method = 'GET'
    body = ""
    url= check_url+uri
    response, headers = fetch_url( module,
        url, data=body, headers=headers,
        method=method, use_proxy=False
    )
    if headers['status'] == 200:
        body = response.read()
        body=json.loads(body)
        api=body['version_element'][len(body['version_element'])-1]['version']
        module.params['api_version'] = api
    else:
        module.fail_json(**headers)

def load_params(module):
    provider = module.params.get('provider') or dict()
    for key, value in iteritems(provider):
        if key in arubaoss_argument_spec:
            if module.params.get(key) is None and value is not None:
                module.params[key] = value
    if module.params['api_version'] is 'None':
        get_version(module)


def get_connection(module):
    global _DEVICE_CONNECTION
    if not _DEVICE_CONNECTION:
        load_params(module)
        conn = Aossapi(module)
        _DEVICE_CONNECTION = conn
    return _DEVICE_CONNECTION


class Aossapi:
    '''
    This create instance for arubaoss api. The supported version of
    api is v5.0. Previous version can be used to configure but does
    not gurantee module will work as intended or may have failure
    in cases.
    '''

    def __init__(self, module):
        self._module = module
        self._cookie = None

        host = self._module.params['host']
        port = self._module.params['port']

        if self._module.params['use_ssl']:
            proto = 'https'
            port = port or 443
        else:
            proto = 'http'
            port = port or 80

        api = self._module.params['api_version']

        self._url = "{}://{}:{}/rest/{}".format(proto,host,port,api)

    def _send(self, url, method='POST', body={}):
        '''Sends command to device '''

        headers = {'Content-Type': 'application/json'}

        data = self._module.jsonify(body)
        if self._cookie:
            headers['Cookie'] = self._cookie
        response, headers = fetch_url(
            self._module, url, data=body, headers=headers,
            method=method, use_proxy=False
        )
        return response, headers


    def login(self):
        ''' Created login uri and saves cookie'''

        password = self._module.params['password']
        username = self._module.params['username']

        url = self._url + "/login-sessions"
        data = {"userName":username ,"password": password}
        data = self._module.jsonify(data)

        response, headers = self._send(url, body=data)

        if headers['status'] == 201:
            self._cookie = headers.get('set-cookie')
        else:
            self._module.fail_json(**headers)

    def logout(self):
        ''' Logout from device '''
        url = self._url + "/login-sessions"

        response, headers = self._send(url, body="", method='DELETE')
        self._cookie = None

        if headers['status'] != 204:
            self._module.fail_json(**headers)

    def run_commands(self, uri, payload={}, method="POST", check=None,wait_after_send=0):

        '''
        Validate that the configuration is present on the device. If not then send command
        to device for processing. Otherwise return data to module.
        '''
        reboot = None
        response = None
        if method == 'reboot':
            reboot = True
            method = 'POST'

        try:
            self.login()

            if check:
                response = self._validate_request(method, payload, check)
                if response:
                    self.logout()
                    # Configuration change not required
                    return response

            data = self._module.jsonify(payload)

            url = self._url + uri

            response, headers = self._send(url, body=data, method=method)
            sleep(wait_after_send)

            if not reboot:
                self.logout()

            if headers['status'] == 204:
                return {'msg': 'Successful','changed':True}

            try:
                if response:
                    data = response.read()
                    response = self._module.from_json(to_text(data, errors='surrogate_then_replace'))
                    response['header'] = headers
                    response['changed'] = True
                else:
                    if headers['status'] not in (200, 201, 202, 204):
                        headers['failed'] = True
                        return headers

            except ValueError:
                self._module.fail_json(msg='unable to load response from device', data=data)

            return response
        except Exception as err:
            self._module.fail_json(msg='Failed : {}'.format(err),failed=True)

    def get_config(self, uri, check_login=True):
        ''' Execute a GET operation of device for uri'''
        url = self._url +  uri
        headers = {'Content-Type': 'application/json'}

        no_login=False
        if not self._cookie and check_login:
            no_login=True
            self.login()

        if check_login:
            headers['Cookie'] = self._cookie

        response, headers = fetch_url(self._module, url, headers=headers,
                method='GET', use_proxy=False)

        if no_login:
            self.logout()

        if headers['status'] == 200:
            return response.read()

        return None

    def _validate_request(self, method, payload, check):
        '''Compares value being applied to the configuration present on the device'''
        check_presence = self.get_config(check)
        if method == 'DELETE':
            if not check_presence:
                response = {'changed': False,
                            'failed': False,
                            'msg': 'Not present'}
                return response
        elif method != 'GET':
            if check_presence:
                diffkeys = False
                data = self._module.from_json(to_text(check_presence))
                for key in payload:
                    if key in data:
                        if payload[key] != data[key]:
                            diffkeys = True
                            break

                if not diffkeys:
                    data['changed'] = False
                    data['failed'] = False
                    return data


        return None

def get_config(module, *args, **kwargs):
    conn = get_connection(module)
    return conn.get_config(*args, **kwargs)


def run_commands(module, commands, *args, **kwargs):
    conn = get_connection(module)
    return conn.run_commands(commands, *args, **kwargs)

