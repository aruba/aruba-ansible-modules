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
module: arubaoss_command
version_added: "2.9"
short_description: Logs in and executes CLI commands on AOS-Switch device via SSH connection
description:
  - This module allows execution of CLI commands on AOS-Switch devices via SSH connection
author: Aruba Networks (@ArubaNetworks)
options:
  commands:
    description: List of commands to be executed in sequence on the switch. Every command
      will attempt to be executed regardless of the success or failure of the previous 
      command in the list. To execute commands in the 'configure' context, you must include 
      the 'configure terminal' command or one of its variations before the configuration commands. 
      'Show' commands are valid and their output will be printed to the screen, returned by the 
      module, and optionally saved to a file. The default module timeout is 30 seconds. To change the 
      command timeout, set the variable 'ansible_command_timeout' to the desired time in seconds.
    required: True
    type: list
  wait_for:
    description: A list of conditions to wait to be satisfied before continuing execution.
      Each condition must include a test of the 'result' variable, which contains the output 
      results of each already-executed command in the 'commands' list. 'result' is a list
      such that result[0] contains the output from commands[0], results[1] contains the output 
      from commands[1], and so on.  
    required: False
    type: list
    
  match:
    description: Specifies whether all conditions in 'wait_for' must be satisfied or if just 
      any one condition can be satisfied. To be used with 'wait_for'.
    default: 'all'
    choice: ['any', 'all']
    required: False
    type: str
        
  retries:
    description: Maximum number of retries to check for the expected prompt.
    default: 10
    required: False
    type: int
  interval:
    description: Interval between retries, in seconds.
    default: 1
    required: False
    type: int
  output_file:
    description: Full path of the local system file to which commands' results will be output.
    The directory must exist, but if the file doesn't exist, it will be created.
    required: False
    type: str
'''  # NOQA

EXAMPLES = '''
- name: Execute show commands and configure commands, and output results to file
  arubaoss_command:
    commands: ['show run',
      'show interface 24',
      'config',
      'vlan 2',
        'ip address 10.10.10.10/24',
      'end']
    output_file: /users/Home/configure.cfg
- name: Show running-config and show version, and pass only if all (both) results match
  arubaoss_command:
    commands:
      - 'show run'
      - 'show version'
    wait_for:
      - result[0] contains "vlan 2"
      - result[1] contains "WC.16.09.0010G"
    match: all
    retries: 5
    interval: 5
- name: Show running-config, show version commands output to a file 
  arubaoss_command:
    commands: ['show run', 'show version']
    output_file: /users/Home/config_list.cfg
- name: Run ping command with increased command timeout
  vars:
    - ansible_command_timeout: 60
  arubaoss_command:    
    commands:
      - ping 10.100.0.12 repetitions 100
    output_file: /users/Home/ping.cfg
'''  # NOQA

RETURN = r''' # '''

import time
from ansible.module_utils._text import to_text
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.common.parsing import Conditional
from ansible.module_utils.network.common.utils import to_lines, ComplexList
from ansible.module_utils.network.arubaoss.arubaoss import run_cli_commands as run_commands  # NOQA
from ansible.module_utils.network.arubaoss.arubaoss import arubaoss_argument_spec  # NOQA


def transform_commands(module):
    '''
    Transform the command to a complex list
    '''
    transform = ComplexList(dict(
        command=dict(key=True),
        prompt=dict(type='list'),
        answer=dict(type='list'),
        newline=dict(type='bool', default=True),
        sendonly=dict(type='bool', default=False),
        check_all=dict(type='bool', default=False),
    ), module)

    return transform(module.params['commands'])


def parse_commands(module, warnings):
    '''
    Parse the command
    '''
    commands = transform_commands(module)

    return commands


def main():
    '''
    Main entry point to the module
    '''

    argument_spec = dict(
        commands=dict(type='list', required=True),
        wait_for=dict(type='list', aliases=['waitfor']),
        match=dict(default='all', choices=['all', 'any']),
        retries=dict(default=10, type='int'),
        interval=dict(default=1, type='int'),
        output_file=dict(type='str', default=None),
    )

    argument_spec.update(arubaoss_argument_spec)

    warnings = list()

    result = {'changed': False, 'warnings': warnings}
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
        )

    commands = parse_commands(module, warnings)
    wait_for = module.params['wait_for'] or list()

    try:
        conditionals = [Conditional(c) for c in wait_for]
    except AttributeError as exc:
        module.fail_json(msg=to_text(exc))

    retries = module.params['retries']
    interval = module.params['interval']
    match = module.params['match']

    while retries >= 0:
        responses = run_commands(module, commands)

        for item in list(conditionals):
            if item(responses):
                if match == 'any':
                    conditionals = list()
                    break
                conditionals.remove(item)

        if not conditionals:
            break

        time.sleep(interval)
        retries -= 1

    if conditionals:
        failed_conditions = [item.raw for item in conditionals]
        msg = 'One or more conditional statements have not been satisfied'
        module.fail_json(msg=msg, failed_conditions=failed_conditions)

    commands_list = []
    for command in commands:
        commands_list.append(command['command'])

    if module.params['output_file'] is not None:
        output_file = str(module.params['output_file'])
        with open(output_file, 'w') as output:
            for i, command in enumerate(commands_list):
                output.write("command: ")
                output.write(command)
                output.write("\n")
                output.write("response: ")
                output.write(str(responses[i]))
                output.write("\n")
                output.write("------------------------------------------")
                output.write("\n")

    result.update({
        'stdout': responses,
        'stdout_lines': list(to_lines(responses))
    })
    module.exit_json(**result)


if __name__ == '__main__':
    main()
