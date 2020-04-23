#!/usr/bin/python
# -*- coding: utf-8 -*-

# (C) Copyright 2020 Hewlett Packard Enterprise Development LP.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: arubaoss_config
version_added: "2.9"
short_description: Logs in and executes configuration commands on AOS-Switch device via SSH connection
description:
  - This module allows configuration of running-configs on AOS-Switch devices via SSH connection
author: Aruba Networks (@ArubaNetworks)
options:
  lines:
    description:
      - List of configuration commands to be executed. If "parents" is specified, these
        are the child lines contained under/within the parent entry. If "parents" is not 
        specified, these lines will be checked and/or placed under the global config level. 
        These commands must correspond with what would be found in the device's running-config.
    required: False
    type: list
  parents:
    description:
      - Parent lines that identify the configuration section or context under which the
        "lines" lines should be checked and/or placed. 
    required: False
    type: list
  src:
    description:
      - Path to the file containing the configuration to load into the device.  The path can 
        be either a full system path to the configuration file if the value starts with "/"
        or a path relative to the directory containing the playbook. This argument is mutually 
        exclusive with the "lines" and "parents" arguments. This src file must have same 
        indentation as a live switch config. The operation is purely additive, as it doesn't remove
        any lines that are present in the existing running-config, but not in the source config.
    required: False
    type: str
  before:
    description:
      - Commands to be executed prior to execution of the parent and child lines. This option
        can be used to guarantee idempotency.
    required: False
    type: list
  after:
    description:
      - Commands to be executed following the execution of the parent and child lines. This 
        option can be used to guarantee idempotency.
    required: False
    type: list
  match:
    description:
      - Specifies the method of matching. Matching is the comparison against the existing 
        running-config to determine whether changes need to be applied.
        If "match" is set to "line," commands are matched line by line.  
        If "match" is set to "strict," command lines are matched with respect to position.  
        If "match" is set to "exact," command lines must be an equal match.  
        If "match" is set to "none," the module will not attempt to compare the source 
        configuration with the running-config on the remote device.
    default: line
    choices: ['line', 'strict', 'exact', 'none']
    required: False
    type: str
  replace:
    description:
      - Specifies the approach the module will take when performing configuration on the 
        device. 
        If "replace" is set to "line," then only the differing and missing configuration lines 
        are pushed to the device. 
        If "replace" is set to "block," then the entire command block is pushed to the device 
        if there is any differing or missing line at all.
    default: line
    choices: ['line', 'block']
    required: False
    type: str
  backup:
    description:
      - Specifies whether a full backup of the existing running-config on the device will be 
        performed before any changes are potentially made. If the "backup_options" value is not 
        specified, the backup file is written to the "backup" folder in the playbook root 
        directory. If the directory does not exist, it is created.
    required: False
    type: bool
    default: False
  backup_options:
    description:
      - File path and name options for backing up the existing running-config. 
        To be used with "backup."
    suboptions:
      filename:
        description:
          - Name of file in which the running-config will be saved.
        required: False
        type: str
      dir_path:
        description:
          - Path to directory in which the backup file should reside.
        required: False
        type: str
    type: dict
  running_config:
    description:
      - Specifies an alternative running-config to be used as the base config for matching. The 
        module, by default, will connect to the device and retrieve the current running-config 
        to use as the basis for comparison against the source.  This argument is handy for times 
        when it is not desirable to have the task get the current running-config, and instead use
        another config for matching. 
    aliases: ['config']
    required: False
    type: str
  save_when:
    description:
      - Specifies when to copy the running-config to the startup-config. When changes are made to 
        the device running-configuration, the changes are not copied to non-volatile storage by default.  
        If "save_when" is set to "always," the running-config will unconditionally be copied to 
        startup-config.
        If "save_when" is set to "never," the running-config will never be copied to startup-config.
        If "save_when" is set to "modified," the running-config will be copied to startup-config 
        if the two differ.
        If "save_when" is set to "changed," the running-config will be copied to startup-config 
        if the task modified the running-config.
    default: never
    choices: ['always', 'never', 'modified', 'changed']
    required: False
    type: str
  diff_against:
    description:
      - When using the "ansible-playbook --diff" command line argument this module can generate 
        diffs against different sources. This argument specifies the particular config against 
        which a diff of the running-config will be performed. 
        If "diff_against" is set to "startup," the module will return the diff of the running-config 
        against the startup configuration.
        If "diff_against" is set to "intended," the module will return the diff of the running-config 
        against the configuration provided in the "intended_config" argument.
        If "diff_against" is set to "running," the module will return before and after diff of the 
        running-config with respect to any changes made to the device configuration.
    choices: ['startup', 'intended', 'running']
    required: False
    type: str
  diff_ignore_lines:
    description:
      - Specifies one or more lines that should be ignored during the diff. This is used to 
        ignore lines in the configuration that are automatically updated by the system. This 
        argument takes a list of regular expressions or exact commands.
    required: False
    type: list
  intended_config:
    description:
      - Path to file containing the intended configuration that the device should conform to, and 
        that is used to check the final running-config against. To be used with "diff_against," 
        which should be set to "intended."
    required: False
    type: str
'''  # NOQA

EXAMPLES = '''
- name: First delete VLAN 44, then configure VLAN 45, and lastly create VLAN 46
  arubaoss_config:
    before: 
      - no vlan 44
    parents: 
      - vlan 45
    lines:
      - name testvlan
      - untagged 1-6
    after: 
      - vlan 46
- name: Back up running-config, then configure TACACS, and save running-config to startup-config if change was made
  arubaoss_config:
    backup: True
    lines: 
      - tacacs-server host 192.168.8.1 key "ArubaR0Cks!"
      - tacacs-server host 192.168.8.1 oobm
    backup_options:
      filename: backup.cfg
      dir_path: /users/Home/
    save_when: changed
- name: Compare running-config with saved config
  arubaoss_config:
    diff_against: intended
    intended_config: /users/Home/backup.cfg
- name: Configure VLAN 2345 and compare resulting running-config with previous running-config
  arubaoss_config:
    lines: 
      - vlan 2345
    diff_against: running
- name: Upload a config from local system file onto device
  arubaoss_config:
    src:  /users/Home/golden.cfg
- name: Update vlan 46, matching only if both "parents" and "lines" are present
  arubaoss_config:
    lines:
      - ip address 4.4.4.5/24
    parents: vlan 46
    match: strict
'''  # NOQA

RETURN = r''' # '''

from ansible.module_utils.network.arubaoss.arubaoss import load_config
from ansible.module_utils.network.arubaoss.arubaoss import run_cli_commands as run_commands  # NOQA
from ansible.module_utils.network.arubaoss.arubaoss import arubaoss_argument_spec  # NOQA
from ansible.module_utils.network.arubaoss.arubaoss import get_cli_config as get_config  # NOQA
from ansible.module_utils.network.arubaoss.arubaoss import check_args as arubaoss_check_args  # NOQA
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.common.config import NetworkConfig, dumps


def get_running_config(module, config=None):
    '''
    Gets the running-config from the switch
    '''
    contents = module.params['running_config']
    if not contents:
        if config:
            contents = config
        else:
            contents = get_config(module)
    return NetworkConfig(contents=contents)


def get_candidate(module):
    '''
    Gets config candidate
    '''
    candidate = NetworkConfig()

    if module.params['src']:
        candidate.loadfp(module.params['src'])
    elif module.params['lines']:
        parents = module.params['parents'] or list()
        candidate.add(module.params['lines'], parents=parents)
    return candidate


def save_config(module, result):
    '''
    Saves config to memory
    '''
    result['changed'] = True
    if not module.check_mode:
        run_commands(module, 'write memory')
    else:
        module.warn('Skipping command `write memory` '
                    'due to check_mode.  Configuration not copied to '
                    'non-volatile storage')


def main():
    """ main entry point for module execution
    """
    backup_spec = dict(
        filename=dict(),
        dir_path=dict(type='path')
    )
    argument_spec = dict(
        src=dict(type='path'),

        lines=dict(aliases=['commands'], type='list'),
        parents=dict(type='list'),

        before=dict(type='list'),
        after=dict(type='list'),

        match=dict(default='line',
                   choices=['line', 'strict', 'exact', 'none']),
        replace=dict(default='line', choices=['line', 'block']),

        running_config=dict(aliases=['config']),
        intended_config=dict(),

        backup=dict(type='bool', default=False),
        backup_options=dict(type='dict', options=backup_spec),

        save_when=dict(choices=['always', 'never', 'modified', 'changed'],
                       default='never'),

        diff_against=dict(choices=['running', 'startup', 'intended']),
        diff_ignore_lines=dict(type='list'),
    )

    argument_spec.update(arubaoss_argument_spec)

    mutually_exclusive = [('lines', 'src'),
                          ('parents', 'src')]

    required_if = [('match', 'strict', ['lines']),
                   ('match', 'exact', ['lines']),
                   ('replace', 'block', ['lines']),
                   ('diff_against', 'intended', ['intended_config'])]

    module = AnsibleModule(argument_spec=argument_spec,
                           mutually_exclusive=mutually_exclusive,
                           required_if=required_if,
                           supports_check_mode=True)

    warnings = list()
    arubaoss_check_args(module, warnings)
    result = {'changed': False, 'warnings': warnings}

    config = None

    if module.params['diff_against'] is not None:
        module._diff = True

    if module.params['backup'] or (module._diff and
                                   module.params['diff_against'] == 'running'):
        contents = get_config(module)
        config = NetworkConfig(contents=contents)
        if module.params['backup']:
            result['__backup__'] = contents
            result['backup_options'] = module.params['backup_options']
            if module.params['backup_options']:
                if 'dir_path' in module.params['backup_options']:
                    dir_path = module.params['backup_options']['dir_path']
                else:
                    dir_path = ""
                if 'filename' in module.params['backup_options']:
                    filename = module.params['backup_options']['filename']
                else:
                    filename = "backup.cfg"

                with open(dir_path+'/'+filename, 'w') as backupfile:
                    backupfile.write(contents)
                    backupfile.write("\n")

    if any((module.params['src'], module.params['lines'])):
        match = module.params['match']
        replace = module.params['replace']

        candidate = get_candidate(module)

        if match != 'none':
            config = get_running_config(module, config)
            path = module.params['parents']
            configobjs = candidate.difference(
                config, match=match, replace=replace, path=path)
        else:
            configobjs = candidate.items

        if configobjs:
            commands = dumps(configobjs, 'commands').split('\n')

            if module.params['before']:
                commands[:0] = module.params['before']

            if module.params['after']:
                commands.extend(module.params['after'])

            result['commands'] = commands
            result['updates'] = commands

            if not module.check_mode:
                load_config(module, commands)

            result['changed'] = True

    running_config = None
    startup_config = None

    diff_ignore_lines = module.params['diff_ignore_lines']
    if diff_ignore_lines is None:
        diff_ignore_lines = []

    diff_ignore_lines.append("Current configuration:")
    diff_ignore_lines.append("Startup configuration:")

    if module.params['save_when'] == 'always':
        save_config(module, result)
    elif module.params['save_when'] == 'modified':
        output = run_commands(module,
                              ['show running-config', 'show config config'])

        running_config = NetworkConfig(
            contents=output[0], ignore_lines=diff_ignore_lines)
        startup_config = NetworkConfig(
            contents=output[1], ignore_lines=diff_ignore_lines)

        if running_config.sha1 != startup_config.sha1:
            save_config(module, result)
    elif module.params['save_when'] == 'changed':
        if result['changed']:
            save_config(module, result)

    if module._diff:
        if not running_config:
            output = run_commands(module, 'show running-config')
            contents = output[0]
        else:
            contents = running_config.config_text

        # recreate the object in order to process diff_ignore_lines
        running_config = NetworkConfig(
            contents=contents, ignore_lines=diff_ignore_lines)

        if module.params['diff_against'] == 'running':
            if module.check_mode:
                module.warn("unable to perform diff against "
                            "running-config due to check mode")
                contents = None
            else:
                contents = config.config_text

        elif module.params['diff_against'] == 'startup':
            if not startup_config:
                output = run_commands(module, 'show config config')
                contents = output[0]
            else:
                contents = startup_config.config_text

        elif module.params['diff_against'] == 'intended':
            with open(module.params['intended_config'], 'r') as intended_file:
                contents = intended_file.read()
        if contents is not None:
            base_config = NetworkConfig(
                contents=contents, ignore_lines=diff_ignore_lines)

            if running_config.sha1 != base_config.sha1:
                result.update({
                    'changed': True,
                    'diff': {'before': str(base_config),
                             'after': str(running_config)}
                })

    module.exit_json(**result)


if __name__ == '__main__':
    main()
