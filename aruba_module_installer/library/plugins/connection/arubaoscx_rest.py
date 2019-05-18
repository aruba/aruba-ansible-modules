# (c) 2018 Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
author: Ansible Networking Team
connection: httpapi
short_description: Use httpapi to run command on network appliances
description:
  - This connection plugin provides a connection to remote devices over a
    HTTP(S)-based api.
version_added: "2.6"
options:
  host:
    description:
      - Specifies the remote device FQDN or IP address to establish the HTTP(S)
        connection to.
    default: inventory_hostname
    vars:
      - name: ansible_host
  port:
    type: int
    description:
      - Specifies the port on the remote device to listening for connections
        when establishing the HTTP(S) connection.
        When unspecified, will pick 80 or 443 based on the value of use_ssl
    ini:
      - section: defaults
        key: remote_port
    env:
      - name: ANSIBLE_REMOTE_PORT
    vars:
      - name: ansible_port
      - name: ansible_httpapi_port
  network_os:
    description:
      - Configures the device platform network operating system.  This value is
        used to load the correct httpapi and cliconf plugins to communicate
        with the remote device
    vars:
      - name: ansible_network_os
  remote_user:
    description:
      - The username used to authenticate to the remote device when the API
        connection is first established.  If the remote_user is not specified,
        the connection will use the username of the logged in user.
      - Can be configured form the CLI via the C(--user) or C(-u) options
    ini:
      - section: defaults
        key: remote_user
    env:
      - name: ANSIBLE_REMOTE_USER
    vars:
      - name: ansible_user
  password:
    description:
      - Secret used to authenticate
    vars:
      - name: ansible_password
      - name: ansible_httpapi_pass
  use_ssl:
    description:
      - Whether to connect using SSL (HTTPS) or not (HTTP)
    default: False
    vars:
      - name: ansible_httpapi_use_ssl
  timeout:
    type: int
    description:
      - Sets the connection time, in seconds, for the communicating with the
        remote device.  This timeout is used as the default timeout value for
        commands when issuing a command to the network CLI.  If the command
        does not return in timeout seconds, the an error is generated.
    default: 120
  become:
    type: boolean
    description:
      - The become option will instruct the CLI session to attempt privilege
        escalation on platforms that support it.  Normally this means
        transitioning from user mode to C(enable) mode in the CLI session.
        If become is set to True and the remote device does not support
        privilege escalation or the privilege has already been elevated, then
        this option is silently ignored
      - Can be configured form the CLI via the C(--become) or C(-b) options
    default: False
    ini:
      section: privilege_escalation
      key: become
    env:
      - name: ANSIBLE_BECOME
    vars:
      - name: ansible_become
  become_method:
    description:
      - This option allows the become method to be specified in for handling
        privilege escalation.  Typically the become_method value is set to
        C(enable) but could be defined as other values.
    default: sudo
    ini:
      section: privilege_escalation
      key: become_method
    env:
      - name: ANSIBLE_BECOME_METHOD
    vars:
      - name: ansible_become_method
  persistent_connect_timeout:
    type: int
    description:
      - Configures, in seconds, the amount of time to wait when trying to
        initially establish a persistent connection.  If this value expires
        before the connection to the remote device is completed, the connection
        will fail
    default: 30
    ini:
      - section: persistent_connection
        key: connect_timeout
    env:
      - name: ANSIBLE_PERSISTENT_CONNECT_TIMEOUT
  persistent_command_timeout:
    type: int
    description:
      - Configures, in seconds, the amount of time to wait for a command to
        return from the remote device.  If this timer is exceeded before the
        command returns, the connection plugin will raise an exception and
        close
    default: 10
    ini:
      - section: persistent_connection
        key: command_timeout
    env:
      - name: ANSIBLE_PERSISTENT_COMMAND_TIMEOUT
"""

import os
import requests
from ansible import constants as c
from ansible.module_utils._text import to_bytes
from ansible.module_utils.six import PY3
from ansible.module_utils.six.moves import cPickle
from ansible.playbook.play_context import PlayContext
from ansible.plugins.loader import connection_loader
from ansible.plugins.connection import ConnectionBase
from ansible.utils.path import unfrackpath

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()


class Connection(ConnectionBase):
    '''Network API connection'''

    transport = 'httpapi'
    has_pipelining = True
    force_persistence = True
    # Do not use _remote_is_local in other connections
    _remote_is_local = True

    def __init__(self, play_context, new_stdin, *args, **kwargs):
        super(Connection, self).__init__(play_context, new_stdin, *args, **kwargs)

        self._is_http = True
        self._history = list()

        self._local = connection_loader.get('local', self._play_context, '/dev/null')
        self._local.set_options()

        self._ansible_playbook_pid = kwargs.get('ansible_playbook_pid')

        # For making connection to the switch
        self._password = self._play_context.password
        self._username = self._play_context.remote_user
        self._remote_host = self._play_context.remote_addr
        self._protocol = 'https'

        # Construct URLs for interacting with the switch
        self._construct_urls()

        # reconstruct the socket_path and set instance values accordingly
        self._update_connection_state()

    def __getattr__(self, name):
        try:
            return self.__dict__[name]
        except KeyError:
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, name))

    def _construct_urls(self):
        login_string = '/rest/v1/login'
        logout_string = '/rest/v1/logout'
        run_config_string = '/rest/v1/fullconfigs/running-config'
        self._login_url = '%s://%s%s' % (self._protocol, self._remote_host, login_string)
        self._logout_url = '%s://%s%s' % (self._protocol, self._remote_host, logout_string)
        self._run_config_url = '%s://%s%s' % (self._protocol, self._remote_host, run_config_string)

    def exec_command(self, cmd, in_data=None, sudoable=True):
        return self._local.exec_command(cmd, in_data, sudoable)

    def put_file(self, in_path, out_path):
        return self._local.put_file(in_path, out_path)

    def fetch_file(self, in_path, out_path):
        return self._local.fetch_file(in_path, out_path)

    def update_play_context(self, pc_data):
        """Updates the play context information for the connection"""
        pc_data = to_bytes(pc_data)
        if PY3:
            pc_data = cPickle.loads(pc_data, encoding='bytes')
        else:
            pc_data = cPickle.loads(pc_data)
        play_context = PlayContext()
        play_context.deserialize(pc_data)

        messages = ['updating play_context for connection']
        if self._play_context.become ^ play_context.become:
            self._httpapi.set_become(play_context)

        self._play_context = play_context
        return messages

    def _connect(self):
        if self._connected:
            return
        display.vvvv("Opening the rest session now")
        payload = {'action': 'login', 'username': self._username, 'password': self._password}
        self._http_session_handle = requests.session()
        self._http_session_handle.trust_env = False
        response = self._http_session_handle.post(self._login_url, data=payload, verify=False)
        display.vvvv("Login response")
        display.vvvv(response.text)
        display.vvvv("The session object is")
        display.vvvv("=== ======= ====== ==")
        display.vvvv(str(self._http_session_handle))
        self._connected = True

    def _update_connection_state(self):
        '''
        Reconstruct the connection socket_path and check if it exists
        If the socket path exists then the connection is active and set
        both the _socket_path value to the path and the _connected value
        to True.  If the socket path doesn't exist, leave the socket path
        value to None and the _connected value to False
        '''
        ssh = connection_loader.get('ssh', class_only=True)
        cp = ssh._create_control_path(
            self._play_context.remote_addr, self._play_context.port,
            self._play_context.remote_user, self._play_context.connection,
            self._ansible_playbook_pid
        )

        tmp_path = unfrackpath(c.PERSISTENT_CONTROL_PATH_DIR)
        socket_path = unfrackpath(cp % dict(directory=tmp_path))

        if os.path.exists(socket_path):
            self._connected = True
            self._socket_path = socket_path

    def reset(self):
        '''
        Reset the connection
        '''
        if self._socket_path:
            display.vvvv('resetting persistent connection for socket_path %s' % self._socket_path, host=self.host)
            self.close()
        display.vvvv('reset call on connection instance', host=self.host)

    def close(self):
        if self._connected:
            response = self._http_session_handle.post(self._logout_url, verify=False)
            display.debug("Hi! Closing the http connection now")
            display.vvvv(response.text)
            display.display("Closed the http connection!")
            self._connected = False

    def get_running_config(self):
        if self._connected and self._http_session_handle:
            response = self._http_session_handle.get(self._run_config_url, verify=False)
            return response.text

    def put_running_config(self, updated_config):
        if self._connected and self._http_session_handle:
            response = self._http_session_handle.put(self._run_config_url, data=updated_config, verify=False)
            return response.text
