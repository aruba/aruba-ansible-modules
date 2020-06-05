# (c) 2018 Red Hat Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
#
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


from ansible import constants as C
from ansible.plugins.action.normal import ActionModule as _ActionModule
from ansible.module_utils.network.arubaoss.arubaoss import arubaoss_provider_spec
from ansible.module_utils.network.common.utils import load_provider

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()


class ActionModule(_ActionModule):

    def run(self, tmp=None, task_vars=None):
        del tmp  # tmp no longer has any effect

        socket_path = None

        if self._play_context.connection == 'local' or self._play_context.connection == 'network_cli':
            provider = load_provider(arubaoss_provider_spec, self._task.args)
            transport = provider['transport'] or 'aossapi'

            display.vvvv('connection transport is %s for %s' % (transport, self._play_context.remote_addr))
            if not provider.get('api_version') is None:
                api = provider.get('api_version')
                if api not in ['v1.0','v2.0','v2.1','v2.2','v3.0','v3.1','v4.0','v5.0']:
                    provider['api_version'] = None
                    display.vvvv('%s is not valid api version. using aossapi v6.0 instead' % api)
                else:
                    display.vvvv('%s is not latest version (v6.0), arubaoss module may not work as intended' % api)


            if transport == 'cli':
                return dict(
                        failed=True,
                        msg='invalid connection specified, expected connection=local, '
                        'got %s' % self._play_context.connection)
            else:
                self._task.args['provider'] = ActionModule.aossapi_implementation(provider, self._play_context)

        result = super(ActionModule, self).run(task_vars=task_vars)
        return result

    @staticmethod
    def aossapi_implementation(provider, play_context):
        provider['transport'] = 'aossapi'
        if provider.get('host') is None:
            provider['host'] = play_context.remote_addr

        if provider.get('port') is None:
            if provider.get('use_ssl'):
                provider['port'] = 443
            else:
                provider['port'] = 80

        if provider.get('timeout') is None:
            provider['timeout'] = C.PERSISTENT_COMMAND_TIMEOUT

        if provider.get('username') is None:
            if play_context.connection == 'network_cli':
                provider['username'] = play_context.remote_user
            else:
                provider['username'] = play_context.connection_user

        if provider.get('password') is None:
            provider['password'] = play_context.password

        if provider.get('use_ssl') is None:
            provider['use_ssl'] = False

        if provider.get('validate_certs') is None:
            provider['validate_certs'] = True

        return provider
